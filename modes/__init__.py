import importlib
from typing import Tuple, Dict, Any

from shared import constants
from server import protocol, connection, types, util


class GameMode:
    id: int = 0
    name: str = "Unknown!"
    description: str = "Description!"

    short_name: str = "default"

    title: str = ""
    description_key: str = ""
    info_text1: str = ""
    info_text2: str = ""
    info_text3: str = ""

    @property
    def score_limit(self) -> int:
        return self.config.get("score_limit", 10)

    @property
    def mode_info(self) -> Dict[str, Any]:
        """Return combined mode information for initial packet"""
        mode_id = self.short_name
        
        # Default values if mode not found
        title_key = f"{mode_id.upper()}_TITLE" if mode_id else "UNKNOWN_TITLE"
        description_key = constants.MODE_DESCRIPTIONS.get(mode_id, "UNKNOWN_DESCRIPTION")
        
        # Get infographic texts
        info_texts = constants.MODE_INFOGRAPHIC_TEXTS.get(mode_id, 
            ['UNKNOWN_INFOGRAPHIC_TEXT1', 'UNKNOWN_INFOGRAPHIC_TEXT2', 'UNKNOWN_INFOGRAPHIC_TEXT3'])
        
        return {
            "title_key": title_key,
            "description_key": description_key,
            "info_text1_key": info_texts[0],
            "info_text2_key": info_texts[1],
            "info_text3_key": info_texts[2],
        }

    def __init__(self, protocol: 'protocol.ServerProtocol'):
        self.protocol = protocol
        self.config = protocol.config.get("modes.default", {})
        module_name = ''.join(str(self.__module__).split(".")[1:])  # strip package name
        self.config.update(protocol.config.get("modes." + module_name, {}))

        # TODO should this be in the base GameMode or should this just be default behaviour within these entities?
        types.HealthCrate.on_collide += self.on_health_crate
        types.AmmoCrate.on_collide += self.on_ammo_crate
        connection.ServerConnection.on_player_kill += self.on_player_kill

        self.win_sound = self.protocol.create_sound("horn")

    def start(self):
        pass

    def stop(self):
        pass

    async def reset(self, winner: types.Team=None):
        self.protocol.loop.create_task(self.on_game_end(winner))
        if winner is not None:
            self.win_sound.play()
            self.protocol.broadcast_hud_message(f"{winner.name} team wins!")
        self.stop()
        self.start()
        for player in self.protocol.players.values():
            player.spawn()
        for team in self.protocol.teams.values():
            team.reset()

    def check_win(self):
        if any(team.score == self.score_limit for team in self.protocol.teams.values()):
            winner = max(self.protocol.teams.values(), key=lambda team: team.score)
            self.protocol.loop.create_task(self.reset(winner))

    def update(self, dt: float):
        pass

    def on_health_crate(self, crate: types.HealthCrate, connection: 'connection.ServerConnection'):
        connection.set_hp(100)
        crate.destroy()

    def on_ammo_crate(self, crate: types.AmmoCrate, connection: 'connection.ServerConnection'):
        connection.weapon.restock()
        self.protocol.loop.create_task(connection.weapon.send_ammo())
        crate.destroy()

    async def on_player_kill(self, player: 'connection.ServerConnection', kill_type: constants.KILL, killer: 'connection.ServerConnection',
                             respawn_time: int):
        if not killer or killer is player:
            # suicide
            player.score -= 1
        else:
            killer.score += 1

    def get_spawn_point(self, player: 'connection.ServerConnection') -> Tuple[float, float, float]:
        x, y, z = self.get_random_pos(player.team)
        # VXL Z (0=Top, 63=Bottom). Physics is also Z-Down (0=Top).
        # z is the index of the solid block.
        # We want to spawn ABOVE it (lower Z index).
        world_z = max(0, z - 2.5) # Spawn 2.5 blocks above the solid block
        print(f"Spawn Debug: Map(x={x}, y={y}, z={z}) -> Player(x={x+0.5}, y={y+0.5}, z={world_z})")
        return x + 0.5, y + 0.5, float(world_z)

    def get_random_pos(self, team) -> Tuple[int, int, int]:
        sections = self.protocol.map.width() // 8
        team_idx = 1 if team.id == constants.TEAM.TEAM2 else 0
        offset = team_idx * (self.protocol.map.width() - (sections * 2))
        
        # DEBUG: Check if map has ANY solid blocks at the center
        test_x, test_y = 256, 256
        test_z = self.protocol.map.get_z(test_x, test_y)
        test_solid = self.protocol.map.get_solid(test_x, test_y, 62)
        print(f"DEBUG: Map check at ({test_x},{test_y}): get_z={test_z}, solid@62={test_solid}")
        
        x, y, z = self.protocol.map.get_random_pos(0 + offset, 0, (sections * 2) + offset, self.protocol.map.width())
        print(f"DEBUG: get_random_pos returned ({x},{y},{z})")
        return x, y, z

    # Hooks
    on_game_end = util.AsyncEvent()


def get_game_mode(protocol: 'protocol.ServerProtocol', mode_name: str) -> GameMode:
    module = importlib.import_module(f"modes.{mode_name}")
    mode = module.init(protocol)
    if not isinstance(mode, GameMode):
        raise TypeError(f"Mode {mode_name} did not return a GameMode instance!")
    return mode
