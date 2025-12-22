import asyncio
import io
import sys
import textwrap
import traceback
import zlib
from collections import defaultdict
from typing import *

import enet

from shared import packet as packets
from shared import glm
from aoslib import world
from shared.bytes import ByteReader, ByteWriter
from shared.constants import *
from server import base, protocol, types, weapons, util
from shared.constants import CLASS_SPRINT_MULTIPLIER
from server.loaders import *
from server.util import lzf_decompress, lzf_compress


_loader_handlers: Dict[int, Callable[['ServerConnection', packets.Loader], None]] = {}
def on_loader_receive(*loaders):
    def decorator(func):
        _loader_handlers.update({loader.id: func for loader in loaders})
        return func
    return decorator


class ServerConnection(base.BaseConnection):
    def __init__(self, protocol: 'protocol.ServerProtocol', peer: enet.Peer):
        self.protocol = protocol
        self.peer = peer
        self.steam_key: bytes = None
        self.steam_id: int = None

        self.id: int = None
        self.name = "Deuce"
        self.hp = 100
        self.team: types.Team = None

        self.ping_stime = 0
        self.pong_stime = 0

        self.input_flags = 0

        self.action_flags = 0

        # Current values
        self.class_id = 0
        self.loadout = []
        self.prefabs = []
        self.ugc_tools = []


        # Next values
        self.loadout_next = []
        self.prefabs_next = []
        self.ugc_tools_next = []
        self.class_id_next = 0


        self._score = 0
        self.wo: world.Player = None

        self.weapon = weapons.Weapon(self)
        self.block = weapons.Block(self)
        self.spade = weapons.Spade(self)
        self.grenade = weapons.Grenade(self)
        self.rpg = weapons.RPG(self)
        self.mg = weapons.MG(self)
        self.sniper = weapons.Sniper(self)
        self.tool_type = WEAPON.PICKAXE_TOOL

        self.mounted_entity: types.MountableEntity = None
        self.store = {}

        self._listeners: Dict[int, List[asyncio.Future]] = defaultdict(list)

    def on_connect(self, data: int):
        if data != PROTOCOL_VERSION:
            return self.disconnect(DISCONNECT.ERROR_SERVER_OUT_OF_DATE)

        try:
            self.id = self.protocol.player_ids.pop()
        except KeyError:
            return self.disconnect(DISCONNECT.ERROR_FULL)


    def on_disconnect(self):
        if self.id is not None:
            self.protocol.loop.create_task(self.on_player_leave(self))

    def decrypt(self, data: bytes) -> bytes:
        if not self.steam_key:
            return data
        
        return bytes(b ^ self.steam_key[i % len(self.steam_key)]
                     for i, b in enumerate(data))
    

    def on_receive(self, packet: enet.Packet):

        if packet.dataLength < 2:
            return

        # Get the packet bytes.
        data = bytes(packet.data)

        # Handle "compressed" packets:
        # If the first byte is 0x31 then the remainder is LZF-compressed.
        if data[0] == 0x31:
            data = lzf_decompress(data[1:])
        else:
            # Otherwise, skip the first byte (which might be a header byte)
            data = data[1:]

        data = self.decrypt(data)
        self.last_raw_packet = data

        raw_hex = ' '.join(f"{b:02X}" for b in data)
        dismiss_packets = ["04", "00"]
        if raw_hex[:2] not in dismiss_packets:
            print(f"Received packet {raw_hex}")
            pass

        try:
            reader: ByteReader = ByteReader(data)
            packet_id: int = reader.read_byte()
            loader: packets.Loader = packets.CLIENT_LOADERS[packet_id](reader)
        except:
            print(f"Malformed packet from player #{self.id}, disconnecting.", file=sys.stderr)
            traceback.print_exc()
            return # self.disconnect()
        
        self.received_loader(loader)

    def _send_loader(self, writer: ByteWriter, flags=enet.PACKET_FLAG_RELIABLE, no_log=False, loader: packets.Loader=None, jprefix=0x30, no_send=False):

        data = str(writer).encode('cp437')

        if not no_log:
            print(f"\n=== Packet Debug ===")
            print(f"Packet Type: {loader.__class__.__name__}")
            print(f"Raw Data: {repr(data)}")
            print(f"Hex Data: {' '.join(f'{b:02X}' for b in data)}")

        data = bytes([jprefix]) + lzf_compress(data)

        if not no_log:
            print(f"Compressed Hex Data: {' '.join(f'{b:02X}' for b in data)}")

        if no_send:
            return
        packet: enet.Packet = enet.Packet(data, flags)


        
        self.peer.send(0, packet)

    def send_loader(self, loader: packets.Loader, flags=enet.PACKET_FLAG_RELIABLE, no_log=False, jprefix=0x30, no_send=False):
        return self._send_loader(loader.generate(), flags, no_log, loader, jprefix, no_send)

    def disconnect(self, reason: DISCONNECT=DISCONNECT.ERROR_UNDEFINED):
        self.peer.disconnect(reason)

    def reset(self):
        self.wo = None
        respawn_task = self.store["respawn_task"]
        if respawn_task is not None:
            respawn_task.cancel()

    def received_loader(self, loader: packets.Loader):
        if self.id is None:
            print(loader)
            return self.disconnect()

        listeners = self._listeners.pop(loader.id, ())
        for fut in listeners:
            if fut.done():
                continue
            fut.set_result(loader)

        handler = _loader_handlers.get(loader.id)
        if not handler:
            if not listeners:
                print(f"Warning: unhandled packet {loader.id}:{loader} from player #{self.id}")
        else:
            # print(f"Received {loader.id}:{loader} from player #{self.player_id}")
            handler(self, loader)

    def wait_for(self, loader: Type[packets.Loader], timeout=None) -> Coroutine[Any, Any, packets.Loader]:
        fut = self.protocol.loop.create_future()
        self._listeners[loader.id].append(fut)
        return asyncio.wait_for(fut, timeout)

    async def send_connection_data(self):
        self.send_info()
        await self.send_packs()
        await self.send_map()
        self.send_state()
        self.send_skybox()
        self.send_players()
        await self.on_player_connect(self)

    def send_info(self):
        import struct
        # Cast unsigned IP to signed int for C compatibility
        signed_ip = struct.unpack('i', struct.pack('I', self.protocol.host_id))[0]
        initial_info.server_ip = signed_ip
        initial_info.server_port = self.protocol.port
        
        # Add game mode information
        initial_info.server_name = self.protocol.server_name
        initial_info.map_name = self.protocol.config["map"]
        initial_info.filename = "London" # Hard coded, why the fuck check the client map when the server sends it over the air any fucking way?
        initial_info.checksum = 592649088 # For same reason as above
        initial_info.mode_key = self.protocol.mode.id
        initial_info.ugc_mode = self.protocol.mode.id
        initial_info.mode_name = self.protocol.mode.title
        initial_info.mode_description = self.protocol.mode.description_key
        initial_info.mode_infographic_text1 = self.protocol.mode.info_text1
        initial_info.mode_infographic_text2 = self.protocol.mode.info_text2
        try:
            initial_info.mode_infographic_text3 = self.protocol.mode.info_text3
        except AttributeError:
            initial_info.mode_infographic_text3 = ""
            
        initial_info.movement_speed_multipliers = list(CLASS_SPRINT_MULTIPLIER.values())
        
        self.send_loader(initial_info)



    async def send_packs(self):
        print("Sending packs")
        for data, length, crc32 in self.protocol.packs:
            pack_start.checksum = crc32
            pack_start.size = length
            self.send_loader(pack_start)

            try:
                has_pack: bool = (await self.wait_for(packets.PackResponse, 3)).value
            except asyncio.TimeoutError:
                continue
            if has_pack:  # client has pack cached
                continue

            with io.BytesIO(data) as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    pack_chunk.data = data
                    self.send_loader(pack_chunk)
                    await asyncio.sleep(0.1)

    async def send_map(self):
        crc: str = (await self.wait_for(packets.MapDataValidation, 5)).crc
        print(f"Client sent map CRC: {crc}")

        map_data_validation.crc = crc
        self.send_loader(map_data_validation, jprefix=0x31)

        map = self.protocol.map
        print(f"Map estimated size: {map.estimated_size}")
        map_sync_start.size = map.estimated_size
        self.send_loader(map_sync_start, jprefix=0x32)

        # Use the proper chunker from VXL - handles serialization and zlib streaming
        chunker = map.get_chunker()
        chunk_queue = list(chunker.iter())
        total_chunks = len(chunk_queue)

        # Send chunks
        for index, chunk in enumerate(chunk_queue):
            if not chunk:
                continue
            
            # Chunks from MapSyncChunker are already compressed - send directly
            map_sync_chunk.data = chunk
            map_sync_chunk.percent_complete = int((index / total_chunks) * 100)
            self.send_loader(map_sync_chunk, jprefix=0x31, no_log=True)

        self.send_loader(map_sync_end, jprefix=0x31)

    def send_state(self):
        data = self.protocol.get_state()
        data.player_id = self.id
        self.send_loader(data, jprefix=0x31)

    def send_skybox(self):
        skybox_data.value = "Chicago.txt"
        self.send_loader(skybox_data)
        print("Skybox data sent!")

    def send_players(self):
        for conn in self.protocol.players.values():
            self.send_loader(conn.to_existing_player())

    def spawn(self, x: float=None, y: float=None, z: float=None):
        pos = self.protocol.mode.get_spawn_point(self) if x is None or y is None or z is None else (x, y, z)

        hook = self.try_player_spawn(self, x, y, z)
        if hook is False:
            return
        pos = pos if hook is None else hook

        create_player.x, create_player.y, create_player.z = pos
        create_player.ori_x, create_player.ori_y, create_player.ori_z = (0, 0, 255.5)

        create_player.loadout = self.loadout_next
        create_player.prefabs = self.prefabs_next

        create_player.class_id = self.class_id

        create_player.player_id = self.id
        create_player.demo_player = 0
        create_player.dead = 0
        create_player.local_language = 0
        create_player.name = self.name
        create_player.team = self.team.id
        self.protocol.broadcast_loader(create_player)

        if self.team == self.protocol.spectator_team:
            return

        if self.wo is None:
            self.wo = world.Player(self.protocol.map)

        self.wo.set_dead(False)
        self.wo.set_position(*pos, reset=True)
        # Update player's class-specific multipliers
        self.wo.update_class_multipliers(self.class_id)
        self.restock()
        self.protocol.loop.create_task(self.on_player_spawn(self, x, y, z))

    def set_hp(self, hp: int, reason: DAMAGE=None, source: tuple=(0, 0, 0)):
        if reason is None:
            if hp >= self.hp:
                reason = DAMAGE.HEAL
            else:
                reason = DAMAGE.SELF
        self.hp = max(0, min(int(hp), 255))
        set_hp.hp = self.hp
        set_hp.damage_type = reason
        set_hp.source.xyz = source
        self.send_loader(set_hp)

    def kill(self, kill_type: KILL=KILL.FALL_KILL, killer: 'ServerConnection'=None, respawn_time=None):
        if self.dead or self.store.get("respawn_task") is not None: return

        respawn_time = respawn_time or self.protocol.get_respawn_time()
        hook = self.try_player_kill(self, kill_type, killer, respawn_time)
        if hook is False:
            return
        respawn_time = hook or respawn_time

        self.wo.set_dead(True)
        kill_action.player_id = self.id
        kill_action.killer_id = (killer or self).id
        kill_action.kill_type = kill_type
        kill_action.respawn_time = respawn_time + 1
        self.protocol.broadcast_loader(kill_action)

        self.store["respawn_task"] = self.protocol.loop.create_task(self.respawn(respawn_time))
        self.protocol.loop.create_task(self.on_player_kill(self, kill_type, killer, respawn_time))

    async def respawn(self, respawn_time=0):
        await asyncio.sleep(respawn_time)
        self.spawn()
        self.store.pop("respawn_task")

    def hurt(self, damage: int, cause: KILL=KILL.FALL_KILL, damager=None, source=(0, 0, 0)):
        reason = DAMAGE.OTHER
        if not source:
            if damager is not None:
                source = damager.position.xyz
            else:
                source = self.position.xyz
                reason = DAMAGE.SELF
        damager = damager or self

        hook = self.try_player_hurt(self, damage, damager, cause)
        if hook is False:
            return
        damage = damage if hook is None else hook
        self.set_hp(self.hp - damage, reason, source)
        if self.hp <= 0:
            self.kill(cause, damager)
        else:
            self.protocol.loop.create_task(self.on_player_hurt(self, damage, damager, reason))

    def set_tool(self, tool: WEAPON):
        # TODO hooks
        if tool == self.tool_type:
            return

        self.tool.set_primary(False)
        self.tool.set_secondary(False)
        self.tool_type = tool
        self.wo.set_weapon(tool in (WEAPON.PICKAXE_TOOL, WEAPON.SNIPER_TOOL))

        set_tool.player_id = self.id
        set_tool.value = tool
        self.protocol.broadcast_loader(set_tool, no_send=True)

    def set_weapon(self, weapon: WEAPON, respawn_time=None):
        # TODO hooks
        if self.weapon.type == weapon:
            return
        self.weapon = weapons.WEAPONS[weapon](self)
        # Update player's class-specific multipliers
        if self.wo:
            self.wo.update_class_multipliers(self.class_id)
        self.kill(KILL.CLASS_CHANGE_KILL, respawn_time=respawn_time)

    def set_team(self, team: TEAM, respawn_time=None):
        # TODO hooks
        if self.team.id == team:
            return
        old_team = self.team
        self.team = self.protocol.teams[team]
        if old_team.spectator:
            self.spawn()
        else:
            self.kill(KILL.TEAM_CHANGE_KILL, respawn_time=respawn_time)

    def destroy_block(self, x: int, y: int, z: int, destroy_type: ACTION=ACTION.DESTROY):
        hook = self.try_destroy_block(self, x, y, z, destroy_type)
        if hook is False:
            return False
        if hook is not None:
            x, y, z = hook

        to_destroy = [(x, y, z)]
        if destroy_type == ACTION.SPADE and self.tool_type == WEAPON.SPADE_TOOL:
            if not self.spade.check_rapid(primary=False):
                return False

            to_destroy.extend(((x, y, z - 1), (x, y, z + 1)))
        elif destroy_type == ACTION.GRENADE:
            for ax in range(x - 1, x + 2):
                for ay in range(y - 1, y + 2):
                    for az in range(z - 1, z + 2):
                        to_destroy.append((ax, ay, az))
        elif destroy_type == ACTION.DESTROY:
            if self.mounted_entity:
                if not isinstance(self.mounted_entity, types.MachineGun) or not self.mounted_entity.check_rapid():
                    return
            elif not self.tool.check_rapid(primary=True, times=1 if self.weapon.type == WEAPON.SHOTGUN_TOOL else 2):
                return False
            self.block.destroy()

        for ax, ay, az in to_destroy:
            self.protocol.map.destroy_point(ax, ay, az)

        block_build.player_id = self.id
        block_build.xyz = (x, y, z)
        block_build.block_type = 1
        self.protocol.broadcast_loader(block_build)
        self.protocol.loop.create_task(self.on_destroy_block(self, x, y, z, destroy_type))
        return True

    def build_block(self, x: int, y: int, z: int) -> bool:
        if not self.block.build() or not self.block.check_rapid():
            return False

        hook = self.try_build_block(self, x, y, z)
        if hook is False:
            return False
        if hook is not None:
            x, y, z = hook

        if self.protocol.map.build_point(x, y, z, self.block.color.rgb):
            block_build.player_id = self.id
            block_build.xyz = (x, y, z)
            block_build.block_type = ACTION.BUILD
            self.protocol.broadcast_loader(block_build)
            self.protocol.loop.create_task(self.on_build_block(self, x, y, z))
            return True
        return False

    def build_line(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> bool:
        if not self.block.check_rapid(primary=False):
            print("Failed to build line - check rapid")
            return False

        points = self.protocol.map.block_line(x1, y1, z1, x2, y2, z2)
        if not points:
            print("Failed to build line - no points")
            return False

        if not self.block.build(len(points)):
            print("Failed to build line - build")
            return False

        for point in points:
            x, y, z = point
            self.protocol.map.build_point(x, y, z, self.block.color.rgb)

        # TODO hooks
        # hook = await self.try_build_block(self, x, y, z)
        # if hook is False:
        #     return False
        # if hook is not None:
        #     x, y, z = hook

        block_line.player_id = self.id
        block_line.xyz1 = x1, y1, z1
        block_line.xyz2 = x2, y2, z2
        self.protocol.broadcast_loader(block_line)
        return True

    def set_position(self, x=None, y=None, z=None, reset=True):
        if x is None or y is None:
            x, y, z = self.position.xyz
        else:
            if z is None:
                z = self.protocol.map.get_z(x, y) - 2
        print(f"Setting pos to {x}, {y}, {z}")
        self.wo.set_position(x, y, z, reset)
        position_data.data.xyz = x, y, z
        self.send_loader(position_data)

    def restock(self):
        self.set_hp(100)
        #[tool.restock() for tool in self.tools]
        #self.send_loader(restock)

    def play_sound(self, sound: types.Sound):
        pkt = sound.to_play_sound()
        self.send_loader(pkt)

    # Chat Message Related
    @util.static_vars(wrapper=textwrap.TextWrapper(width=MAX_CHAT_SIZE))
    def send_message(self, message: str, chat_type=CHAT.CHAT_SYSTEM, player_id=0xFF):
        chat_message.chat_type = chat_type
        chat_message.player_id = player_id
        lines: List[str] = self.send_message.wrapper.wrap(message)
        for line in lines:
            chat_message.value = line
            self.send_loader(chat_message)

    def send_chat_message(self, message: str, sender: 'ServerConnection', team: bool=False):
        chat_type = CHAT.CHAT_TEAM if team else CHAT.CHAT_ALL
        return self.send_message(message, player_id=sender.id, chat_type=chat_type)

    def send_server_message(self, message: str):
        return self.send_message("[*] " + message, chat_type=CHAT.CHAT_SYSTEM)

    def send_hud_message(self, message: str):
        return self.send_message(message, chat_type=CHAT.CHAT_BIG)
    

    @on_loader_receive(packets.ClientInMenu)
    def recv_client_in_menu(self, loader: packets.ClientInMenu):
        # Set the client in menu flag
        pass


    @on_loader_receive(packets.ClientData)
    def recv_client_data(self, loader: packets.ClientData):
        if self.dead: return

        walk = loader.up, loader.down, loader.left, loader.right
        animation = loader.jump, loader.crouch, loader.sneak, loader.sprint

        self.tool_type = loader.tool_id

        # px = loader.data.p.x
        # py = loader.data.p.y
        # pz = loader.data.p.z
        
        ox = loader.o_x
        oy = loader.o_y
        oz = loader.o_z


        input_flags = 0
        if loader.up: input_flags |= 1
        if loader.down: input_flags |= 2
        if loader.left: input_flags |= 4
        if loader.right: input_flags |= 8
        if loader.jump: input_flags |= 16
        if loader.crouch: input_flags |= 32
        if loader.sneak: input_flags |= 64
        if loader.sprint: input_flags |= 128
        self.input_flags = input_flags

        # self.action_flags = loader.action_flags # This probably doesn't exist either
        action_flags = 0
        if loader.primary: action_flags |= 1
        if loader.secondary: action_flags |= 2
        # ... other flags?
        self.action_flags = action_flags
        # if util.bad_float(px, py, pz, ox, oy, oz):
        #     print("Bad float")
        #     #return self.disconnect()

        # if glm.Vector3(px, py, pz).sq_distance(self.wo.position) >= 3 ** 2:
        #     self.set_position(reset=False)
        #     print("Setting position")
        # else:
        #     self.wo.set_position(px, py, pz)

        self.wo.set_orientation((ox, oy, oz))
        
        # TODO: verify set_walk and set_animation on server Authoritative movement
        # self.wo.set_walk(*walk)
        # self.protocol.loop.create_task(self.on_walk_change(self, *walk))
        # self.wo.set_animation(*animation)
        # self.protocol.loop.create_task(self.on_animation_change(self, *animation))

        loader.player_id = self.id
        self.protocol.broadcast_loader(loader, predicate=lambda conn: conn is not self, no_log=True)

    @on_loader_receive(packets.ExistingPlayer)
    def recv_existing_player(self, loader: packets.ExistingPlayer):
        if loader.weapon not in weapons.WEAPONS or loader.team not in self.protocol.teams:
            return self.disconnect()

        self.name = self.validate_name(loader.name)
        self.weapon = weapons.WEAPONS[loader.weapon](self)
        self.team = self.protocol.teams[loader.team]
        self.protocol.loop.create_task(self.on_player_join(self))
        self.spawn()



    @on_loader_receive(packets.NewPlayerConnection)
    def recv_new_player(self, loader: packets.NewPlayerConnection):
        # if loader.team not in self.protocol.teams:
        #     return self.disconnect()

        self.name = self.validate_name(loader.name)
        self.class_id = loader.class_id
        self.team = self.protocol.teams[loader.team]
        
        # Initialize player with class-specific multipliers right from the start
        if self.wo:
            self.wo.update_class_multipliers(self.class_id)
            
        self.protocol.loop.create_task(self.on_player_join(self))
        self.spawn()

    # TODO: Implement build prefab action
    @on_loader_receive(packets.BuildPrefabAction)
    def recv_build_prefab_action(self, loader: packets.BuildPrefabAction):
        print(loader.prefab_name)


    def validate_name(self, name: str):
        name = name.strip()
        if name.isspace() or name == "Deuce":
            name = f"Deuce{self.id}"

        new_name = name
        existing_names = [ply.name.lower() for ply in self.protocol.players.values()]
        x = 0
        while new_name in existing_names:
            new_name = f"{name}{x}"
            x += 1
        return new_name

    @on_loader_receive(packets.ChatMessage)
    def recv_chat_message(self, loader: packets.ChatMessage):
        if loader.chat_type not in (CHAT.CHAT_TEAM, CHAT.CHAT_ALL):
            return
        hook = self.try_chat_message(self, loader.value, loader.chat_type)
        if hook is False:
            return
        message = hook or loader.value
        if loader.chat_type == CHAT.CHAT_TEAM:
            self.team.broadcast_chat_message(message, sender=self)
        else:
            self.protocol.broadcast_chat_message(message, sender=self)
        self.protocol.loop.create_task(self.on_chat_message(self, loader.value, loader.chat_type))

    @on_loader_receive(packets.BlockBuild)
    def recv_block_build(self, loader: packets.BlockBuild):
        if self.dead: return

        if loader.value == ACTION.GRENADE:
            print("Grenade action")
            return  # client shouldnt send this

        if loader.value == ACTION.BUILD:
            print("Build action")
            if self.tool_type != WEAPON.BLOCK_TOOL:
                return
            self.build_block(loader.x, loader.y, loader.z)
        else:
            print("Destroy action")
            self.destroy_block(loader.x, loader.y, loader.z, loader.value)

    @on_loader_receive(packets.BlockLine)
    def recv_block_line(self, loader: packets.BlockLine):
        if self.dead or self.tool_type != WEAPON.BLOCK_TOOL: 
            print("Block line action - dead or not block tool")
            return
        self.build_line(loader.x1, loader.y1, loader.z1, loader.x2, loader.y2, loader.z2)

    # @on_loader_receive(packets.WeaponInput)
    # def recv_weapon_input(self, loader: packets.WeaponInput):
    #     if self.dead: return

    #     loader.primary = self.tool.set_primary(loader.primary)
    #     loader.secondary = self.tool.set_secondary(loader.secondary)
    #     loader.player_id = self.id
    #     self.wo.set_fire(loader.primary, loader.secondary)
    #     self.protocol.broadcast_loader(loader, predicate=lambda conn: conn is not self)

    @on_loader_receive(packets.WeaponReload)
    def recv_weapon_reload(self, loader: packets.WeaponReload):
        if self.dead: return
        reloading = self.tool.reload()
        if reloading:
            loader.player_id = self.id
            self.protocol.broadcast_loader(loader, predicate=lambda conn: conn is not self)

    @on_loader_receive(packets.ChangeClass)
    def recv_change_class(self, loader: packets.ChangeClass):
        if self.dead: return
        #self.set_tool(loader.value)
        self.set_weapon(loader.class_id)

    @on_loader_receive(packets.ChangeTeam)
    def recv_change_team(self, loader: packets.ChangeTeam):
        self.set_team(loader.team)


    @on_loader_receive(packets.SetColor)
    def recv_set_color(self, loader: packets.SetColor):
        if self.dead or self.tool_type != WEAPON.BLOCK_TOOL: return

        # Unpack integer color from packet
        c = loader.value
        r = (c >> 16) & 0xFF
        g = (c >> 8) & 0xFF
        b = c & 0xFF
        
        # Set block color safely
        if hasattr(self.block.color, 'rgb'):
            self.block.color.rgb = (r, g, b)
        else:
            self.block.color = (r, g, b) # Fallback if it's a tuple

        loader.player_id = self.id
        # Broadcast needs packed int value again if we rebroadcast SetColor
        # But SetColor definition has 'int value', so we just set loader.value
        loader.value = c 
        self.protocol.broadcast_loader(loader, predicate=lambda conn: conn is not self)

    @on_loader_receive(packets.UseOrientedItem)
    def recv_oriented_item(self, loader: packets.UseOrientedItem):
        if self.dead:
            print("dead")
            return

        if util.bad_float(*loader.position.xyz, *loader.velocity.xyz, loader.value):
            print("bad float")
            return self.disconnect()

        position = validate(glm.Vector3(*loader.position.xyz), self.wo.position).xyz
        print(position)
        velocity = loader.velocity.xyz
        print(loader.tool)
        obj_type = None
        if loader.tool in THROWABLE_EXPLOSIVE_TOOLS:
            print("tool is grenade tool")
            if self.tool_type not in THROWABLE_EXPLOSIVE_TOOLS:
                print("tool is not grenade tool")
                return
            if self.grenade.on_primary():
                print("grenade is on primary")
                obj_type = types.Grenade
            print(self.wo.velocity + self.wo.orientation)
            print(loader.velocity.xyz)
            velocity = validate(glm.Vector3(*velocity), self.wo.orientation + self.wo.velocity).xyz
        elif loader.tool == WEAPON.RPG_TOOL:
            print("tool is rpg tool")
            if self.tool_type != WEAPON.RPG_TOOL:
                print("tool is not rpg tool")
                return
            if self.rpg.on_primary():
                print("rpg is on primary")
                obj_type = types.Rocket
            velocity = validate(glm.Vector3(*velocity), self.wo.orientation).xyz
            print("velocity", velocity)
            # note: loader.velocity is actually orientation for RPG rockets.

        if obj_type is not None:
            print("obj_type is not None")
            obj: types.Explosive = self.protocol.create_object(obj_type, self, position, velocity, loader.value)
            print("obj created")
            obj.broadcast_item()
        else:
            print("obj_type is None")

    @on_loader_receive(packets.SetClassLoadout)
    def recv_set_class_loadout(self, loader: packets.SetClassLoadout):
        if self.dead and not loader.instant: 
            self.loadout_next = loader.loadout
            self.prefabs_next = loader.prefabs
            self.ugc_tools_next = loader.ugc_tools
            self.class_id_next = loader.class_id
        else:
            self.loadout = loader.loadout
            self.prefabs = loader.prefabs
            self.ugc_tools = loader.ugc_tools
            self.class_id = loader.class_id
            # Update player's class-specific multipliers if not dead
            if not self.dead and self.wo:
                self.wo.update_class_multipliers(self.class_id)
            
        # Convert loadout numbers to weapon names
        loadout_names = [f"{WEAPON(v).name}({v})" if v in WEAPON.__members__.values() else f"WEAPON({v})" 
                        for v in loader.loadout]
        print(f"Received SetClassLoadout: class {CLASS(loader.class_id).name} ({loader.class_id}), loadout {loadout_names} ({loader.loadout}), prefabs {loader.prefabs}")
        
    @on_loader_receive(packets.ShootPacket)
    def recv_hit_packet(self, loader: packets.ShootPacket):
        # TODO this is a bit of a mess
        if self.dead:
            return

        # TODO our own raycasting and hack detection etc.
        print(f"recv_hit_packet for {self!r}")
        print(f"loader.affect_shooter={loader.affect_shooter}")
        print(f"loader.shooter_id={loader.shooter_id}")
        other = self.protocol.players.get(loader.affect_shooter)
        if loader.shooter_id == loader.affect_shooter or other is None:
            # Handle shooting blocks
            print("Shooting block")
            # damage.player_id = self.id
            # damage.x = loader.position.x
            # damage.y = loader.position.y
            # damage.z = loader.position.z
            # damage.type = 0
            # damage.face = 0
            # damage.chunk_check = 0
            # damage.seed = loader.seed
            # damage.damage = loader.damage
            # damage.causer_id = loader.shooter_id
            # self.protocol.broadcast_loader(damage)
            return
        
        vec = (other.eye - self.eye).normalized
        if self.orientation.dot(vec) <= 0.9:
            print(f"incorrect orientation to hit for {self!r}")
            print(f"self.pos={self.position} other.pos={other.position}")
            print(f"self.orien={self.orientation} expected={vec}")
            return

        other.hurt(damage=loader.damage, cause=KILL.ENTITY_KILL, damager=self)

    @on_loader_receive(packets.PlaceMG)
    def recv_place_mg(self, loader: packets.PlaceMG):
        x, y, z = loader.xyz
        yaw = loader.yaw
        if util.bad_float(yaw):
            return self.disconnect()
        self.protocol.create_entity(types.MachineGun, position=(x, y, z), yaw=yaw, team=self.team)

    @on_loader_receive(packets.SteamSessionTicket) 
    def recv_steam_ticket(self, loader: packets.SteamSessionTicket):
        if self.steam_key is not None:
            return  # Already authenticated
        self.steam_key = loader.ticket
        self.steam_id = 89
        
        if self.steam_id:
            print(f"Steam key received – Steam ID is {self.steam_id}")
        else:
            print(f"No steam key from {self} - client playing in offline mode")
            
        # Schedule sending connection data after short delay
        self.protocol.loop.create_task(self.send_connection_data())

    @on_loader_receive(packets.ClockSync)
    def recv_clock_sync(self, loader: packets.ClockSync):
        """Handle clock sync packet from client"""
        # Store client time
        self.ping_ctime = loader.client_time
        
        # Create response packet
        response = packets.ClockSync()
        response.client_time = self.ping_ctime
        response.server_loop_count = self.protocol.time
        
        self.send_loader(response, no_log=True)

    @on_loader_receive(packets.UseCommand)
    def recv_use_command(self, loader: packets.UseCommand):
        self.protocol.loop.create_task(self.on_use_command(self))

    def update(self, dt):
        if self.dead: return

        self.wo.update(dt)
        # TODO: Implement fall damage in Player physics
        fall_dmg = 0
        if fall_dmg > 0:
            self.hurt(fall_dmg)
        self.tool.update(dt)

    def to_existing_player(self) -> packets.ExistingPlayer:
        existing_player.name = self.name
        existing_player.player_id = self.id
        existing_player.tool = self.tool_type
        existing_player.class_id = 0
        existing_player.score = self._score
        existing_player.team = self.team.id
        
        # Handle color packing (tuple/obj -> int)
        bc = self.block.color
        if hasattr(bc, 'rgb'):
            r, g, b = bc.rgb
        elif isinstance(bc, tuple) and len(bc) >= 3:
            r, g, b = bc[:3]
        else:
            r, g, b = (112, 112, 112)
            
        existing_player.color = (r << 16) | (g << 8) | b
        
        existing_player.demo_player = False
        existing_player.pickup = False
        existing_player.dead = False
        existing_player.forced_team = 0
        existing_player.local_language = 0
        return existing_player

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = max(0, min(int(value), 255))
        set_score.type = SCORE.PLAYER
        set_score.reason = SCORE_REASON.NO_SCORE_REASON
        set_score.specifier = self.id
        set_score.value = self._score
        self.protocol._broadcast_loader(set_score.generate(), no_send=True)

    @property
    def tool(self) -> weapons.Tool:
        return self.tools[self.tool_type]

    @property
    def tools(self) -> List[weapons.Tool]:
        return [self.spade, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper, self.block, self.weapon, self.grenade, self.rpg, self.mg, self.sniper]

    @property
    def position(self) -> glm.Vector3:
        return self.wo.position

    @property
    def eye(self) -> glm.Vector3:
        return self.wo.eye

    @property
    def orientation(self) -> glm.Vector3:
        return self.wo.orientation

    @property
    def velocity(self) -> glm.Vector3:
        return self.wo.velocity

    @property
    def dead(self) -> bool:
        return not self.wo or self.wo.dead

    # TODO: I dislike these. The += business was cute at first, but a much cleaner hook system required.

    # Called after the player connects to the server (after being sent packs, map, game state, etc.)
    # (self) -> None
    on_player_connect = util.AsyncEvent()
    # Called after the player joins the game (first time spawning)
    # (self) -> None
    on_player_join = util.AsyncEvent()
    # Calls after the player leaves from the game.
    # (self) -> None
    on_player_leave = on_player_disconnect = util.AsyncEvent()

    # Called before/after spawning the player
    # (self, x, y, z) -> None | `x, y, z` to override | False to cancel
    try_player_spawn = util.Event(overridable=True)
    # (self, x, y, z) -> None
    on_player_spawn = util.AsyncEvent()

    # Called before/after the player is hurt
    # (self, damage, damager, position) -> None | New `damage` to override | False to cancel
    try_player_hurt = util.Event(overridable=True)
    # (self, damage, damager, position) -> None
    on_player_hurt = util.AsyncEvent()

    # Called before/after the player dies
    # (self, kill_type, killer, respawn_time) -> None | New `respawn_time` to override | False to cancel
    try_player_kill = util.Event(overridable=True)
    # (self, kill_type, killer, respawn_time) -> None
    on_player_kill = util.AsyncEvent()

    # Called before/after the player builds
    # (self, x, y, z) -> None | New `x, y, z` to override | False to cancel
    try_build_block = util.Event(overridable=True)
    # (self, x, y, z) -> None
    on_build_block = util.AsyncEvent()

    # Called before/after the player destroys
    # (self, x, y, z, destroy_type) -> None | New `x, y, z` to override | False to cancel
    try_destroy_block = util.Event(overridable=True)
    # (self, x, y, z, destroy_type) -> None
    on_destroy_block = util.AsyncEvent()

    # Called before/after the player sends a chat message
    # (self, chat_message, chat_type) -> None | New `chat_message` to override | False to cancel
    try_chat_message = util.Event(overridable=True)
    # (self, chat_message, chat_type) -> None
    on_chat_message = util.AsyncEvent()

    # TODO allow direct packet hooks or just proxy them within the handlers?
    # (self, forward, backward, left, right) -> None
    on_walk_change = util.AsyncEvent()
    # (self, jump, crouch, sneak, sprint) -> None
    on_animation_change = util.AsyncEvent()
    # (self, position, orientation) -> None
    on_client_update = util.AsyncEvent()

    # (self) -> None
    on_use_command = util.AsyncEvent()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, name={self.name}, pos={self.position}, tool={self.tool})>"


def validate(client: glm.Vector3, server: glm.Vector3) -> glm.Vector3:

    if client.sq_distance(server) >= 3 ** 2:
        return server
    else:
        return client
