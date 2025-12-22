import asyncio

from shared.constants import *
from shared import packet as packets
from server import connection, loaders


class Tool:
    name: str = "None"
    type = None
    
    # Model properties
    model = []
    view_model = []
    model_size = 0.03
    view_model_size = 0.025
    image = None
    
    # Sound properties
    hit_player_sound = None
    hit_block_sound = None
    pitch_increase = 0
    
    max_primary: int = 0
    max_secondary: int = 0

    primary_rate: float = 0
    secondary_rate: float = 0

    last_primary: float = 0
    last_secondary: float = 0

    def __init__(self, connection: 'connection.ServerConnection'):
        self.connection = connection
        self.next_primary = connection.protocol.time
        self.next_secondary = connection.protocol.time

        self.primary = False
        self.secondary = False

        self.primary_ammo = self.max_primary
        self.secondary_ammo = self.max_secondary

    def update(self, dt: float):
        if self.primary_rate:
            if self.primary_ammo > 0 and self.primary and self.connection.protocol.time >= self.next_primary:
                self.next_primary = self.connection.protocol.time + self.primary_rate
                self.on_primary()

        if self.secondary_rate:
            if self.secondary_ammo > 0 and self.secondary and self.connection.protocol.time >= self.next_secondary:
                self.next_secondary = self.connection.protocol.time + self.secondary_rate
                self.on_secondary()

    def set_primary(self, primary: bool):
        self.primary = primary
        return primary

    def set_secondary(self, secondary: bool):
        self.secondary = secondary
        return secondary

    def on_primary(self, *args, **kwargs):
        return True

    def on_secondary(self, *args, **kwargs):
        return True

    def reload(self, *args, **kwargs):
        return True

    def restock(self):
        self.primary_ammo = self.max_primary
        self.secondary_ammo = self.max_secondary

    def check_rapid(self, primary=True, times=1):
        # this is awful i know
        type = "primary" if primary else "secondary"
        time = self.connection.protocol.time

        last_use = getattr(self, "last_" + type)
        setattr(self, "last_" + type, time)
        rate = (getattr(self, type + "_rate") * times) - (0.025 + self.connection.peer.roundTripTime / 1000)

        return time - last_use >= rate

    def reset(self):
        pass


class Spade(Tool):
    name = "Spade"
    type = WEAPON.SPADE_TOOL
    
    # Model properties
    model = []  # SPADE_MODEL
    view_model = []  # SPADE_VIEW_MODEL
    
    # Sound properties
    hit_player_sound = "SPADE_HIT_PLAYER_SOUND"
    hit_block_sound = "SPADE_HIT_BLOCK_SOUND"
    pitch_increase = 50
    
    primary_rate = 0.2
    secondary_rate = 1.0


class Block(Tool):
    name = "Block"
    type = WEAPON.BLOCK_TOOL
    
    # Model properties
    model = []  # BLOCK_MODEL
    view_model = []  # BLOCK_VIEW_MODEL
    
    max_primary = 50

    primary_rate = 0.5

    def __init__(self, connection: 'connection.ServerConnection'):
        super().__init__(connection)
        self.color = packets.Color()
        self.color.rgb = (112, 112, 112)

    def build(self, num=1):
        if self.primary_ammo < num:
            return False
        self.primary_ammo -= num
        return True

    def destroy(self, num=1):
        self.primary_ammo = max(0, min(self.primary_ammo + num, self.max_primary))

    def reset(self):
        super().reset()
        self.color = packets.Color()
        self.color.rgb = (112, 112, 112)

    async def set_color(self, r, g, b, *, sender_is_self=False):
        self.color.rgb = r, g, b
        loaders.set_color.player_id = self.connection.id
        loaders.set_color.color.rgb = r, g, b
        predicate = lambda conn: conn != self.connection if sender_is_self else None
        self.connection.protocol.broadcast_loader(loaders.set_color, predicate)


class Weapon(Tool):
    type = WEAPON.PICKAXE_TOOL
    name = "Pickaxe"
    reload_time = 0
    one_by_one = False
    
    # Model properties
    model = []  # PICKAXE_MODEL
    view_model = []  # PICKAXE_VIEW_MODEL
    
    # Sound properties
    hit_player_sound = "PICKAXE_HIT_PLAYER_SOUND"
    hit_block_sound = "PICKAXE_HIT_BLOCK_SOUND"
    shoot_sound = "PICKAXE_SHOOT_SOUND"
    reload_sound = None
    
    damage = {HIT.PART_TORSO: None, HIT.PART_HEAD: None, HIT.PART_ARMS: None, HIT.PART_LEFT_LEG: None, HIT.PART_RIGHT_LEG: None}
    damage_type = "PICKAXE_DAMAGE"
    falloff = 0

    def __init__(self, connection: 'connection.ServerConnection'):
        super().__init__(connection)

        self.reloading: bool = False
        self.reload_call: asyncio.Task = None

    def set_primary(self, primary: bool):
        # prevent server/client ammo desync (happens often :s not sure why)
        if primary != self.primary and not primary and not self.one_by_one and not self.reloading:
            self.connection.protocol.loop.create_task(self.send_ammo())

        if self.primary_ammo <= 0:
            self.primary = False
            return False
        if primary and self.one_by_one and self.reloading:
            self.reloading = False
            self.reload_call.cancel()
        self.primary = primary
        return primary

    def set_secondary(self, secondary: bool):
        self.secondary = secondary
        return secondary

    def reload(self):
        if self.reloading:
            return False
        if not self.secondary_ammo or self.primary_ammo >= self.max_primary:
            self.reloading = False
            return False

        self.reloading = True

        self.reload_call = asyncio.ensure_future(self.on_reload())
        return True

    async def on_reload(self):
        await asyncio.sleep(self.reload_time)
        self.reloading = False
        if not self.one_by_one:
            reserve = max(0, self.secondary_ammo - (self.max_primary - self.primary_ammo))
            self.primary_ammo += self.secondary_ammo - reserve
            self.secondary_ammo = reserve
            await self.send_ammo()
        else:
            self.primary_ammo += 1
            self.secondary_ammo -= 1
            await self.send_ammo()
            self.reload()

    def on_primary(self):
        if self.reloading:
            return False
        if self.primary_ammo <= 0:
            return False
        self.primary_ammo -= 1
        # print(self.primary_ammo)
        return True

    def on_secondary(self):
        pass

    def get_damage(self, area, distance=0):
        if not self.primary or self.reloading:
            return None

        clip_tolerance = int(self.max_primary * 0.3)
        if self.primary_ammo + clip_tolerance <= 0:
            return None

        damage = self.damage[area]
        if damage is not None:
            damage *= (1 - min(self.falloff * distance / 30, 1))
        return damage

    async def send_ammo(self):
        loaders.weapon_reload.player_id = self.connection.id
        loaders.weapon_reload.clip_ammo = self.primary_ammo
        loaders.weapon_reload.reserve_ammo = self.secondary_ammo
        self.connection.send_loader(loaders.weapon_reload)


class Semi(Weapon):
    type = WEAPON.RIFLE_TOOL
    name = "Rifle"

    max_primary = 10
    max_secondary = 50

    primary_rate = 0.5

    reload_time = 2.5
    one_by_one = False
    
    # Model properties
    model = []  # RIFLE_MODEL
    view_model = []  # RIFLE_VIEW_MODEL
    
    # Sound properties
    hit_player_sound = "RIFLE_HIT_PLAYER_SOUND"
    hit_block_sound = "RIFLE_HIT_BLOCK_SOUND"
    shoot_sound = "RIFLE_SHOOT_SOUND"
    reload_sound = "RIFLE_RELOAD_SOUND"

    damage = {HIT.PART_TORSO: 50, HIT.PART_HEAD: 150, HIT.PART_ARMS: 35, HIT.PART_LEFT_LEG: 35, HIT.PART_RIGHT_LEG: 35}
    damage_type = "RIFLE_DAMAGE"
    falloff = 0.03


class SMG(Weapon):
    type = WEAPON.SMG_TOOL
    name = "SMG"

    max_primary = 30
    max_secondary = 120

    primary_rate = 0.1

    reload_time = 2.5
    one_by_one = False
    
    # Model properties
    model = []  # SMG_MODEL
    view_model = []  # SMG_VIEW_MODEL
    
    # Sound properties
    hit_player_sound = "SMG_HIT_PLAYER_SOUND"
    hit_block_sound = "SMG_HIT_BLOCK_SOUND"
    shoot_sound = "SMG_SHOOT_SOUND"
    reload_sound = "SMG_RELOAD_SOUND"

    damage = {HIT.PART_TORSO: 30, HIT.PART_HEAD: 80, HIT.PART_ARMS: 20, HIT.PART_LEFT_LEG: 20, HIT.PART_RIGHT_LEG: 20}
    damage_type = "SMG_DAMAGE"
    falloff = 0.20


class Shotgun(Weapon):
    type = WEAPON.SHOTGUN_TOOL
    name = "Shotgun"

    max_primary = 6
    max_secondary = 48

    primary_rate = 1.0

    reload_time = 0.5
    one_by_one = True
    
    # Model properties
    model = []  # SHOTGUN_MODEL
    view_model = []  # SHOTGUN_VIEW_MODEL
    
    # Sound properties
    hit_player_sound = "SHOTGUN_HIT_PLAYER_SOUND"
    hit_block_sound = "SHOTGUN_HIT_BLOCK_SOUND"
    shoot_sound = "SHOTGUN_SHOOT_SOUND"
    reload_sound = "SHOTGUN_RELOAD_SOUND"

    damage = {HIT.PART_TORSO: 25, HIT.PART_HEAD: 30, HIT.PART_ARMS: 20, HIT.PART_LEFT_LEG: 20, HIT.PART_RIGHT_LEG: 20}
    damage_type = "SHOTGUN_DAMAGE"
    falloff = 0.40


class RPG(Weapon):
    type = WEAPON.RPG_TOOL
    name = "RPG"

    max_primary = 1
    max_secondary = 5

    primary_rate = 1.0

    reload_time = 4.0
    one_by_one = False
    
    # Model properties
    model = []  # RPG_MODEL
    view_model = []  # RPG_VIEW_MODEL
    
    # Sound properties
    hit_player_sound = None
    hit_block_sound = None
    shoot_sound = "RPG_SHOOT_SOUND"
    reload_sound = "RPG_RELOAD_SOUND"
    explosion_sound = "RPG_EXPLOSION_SOUND"

    damage = {HIT.PART_TORSO: None, HIT.PART_HEAD: None, HIT.PART_ARMS: None, HIT.PART_LEFT_LEG: None, HIT.PART_RIGHT_LEG: None}
    damage_type = "RPG_DAMAGE"
    falloff = 0
    explosion_damage = 100
    explosion_radius = 3

    def update(self, dt):
        pass


# TODO not really a weapon
class MG(Weapon):
    type = WEAPON.MG_TOOL
    name = "MG"

    max_primary = 1
    max_secondary = 0

    primary_rate = 1.0

    reload_time = 0.0
    one_by_one = False
    
    # Model properties
    model = []  # MG_MODEL
    view_model = []  # MG_VIEW_MODEL
    
    # Sound properties
    hit_player_sound = "MG_HIT_PLAYER_SOUND"
    hit_block_sound = "MG_HIT_BLOCK_SOUND"
    shoot_sound = "MG_SHOOT_SOUND"

    damage = {HIT.PART_TORSO: None, HIT.PART_HEAD: None, HIT.PART_ARMS: None, HIT.PART_LEFT_LEG: None, HIT.PART_RIGHT_LEG: None}
    damage_type = "MG_DAMAGE"
    falloff = 0

    def update(self, dt):
        pass


class Sniper(Weapon):
    type = WEAPON.SNIPER_TOOL
    name = "Sniper"

    max_primary = 5
    max_secondary = 25

    primary_rate = 1

    reload_time = 2.5
    one_by_one = False
    
    # Model properties
    model = []  # SNIPER_MODEL
    view_model = []  # SNIPER_VIEW_MODEL
    
    # Sound properties
    hit_player_sound = "SNIPER_HIT_PLAYER_SOUND"
    hit_block_sound = "SNIPER_HIT_BLOCK_SOUND"
    shoot_sound = "SNIPER_SHOOT_SOUND"
    reload_sound = "SNIPER_RELOAD_SOUND"

    damage = {HIT.PART_TORSO: 50, HIT.PART_HEAD: 150, HIT.PART_ARMS: 35, HIT.PART_LEFT_LEG: 35, HIT.PART_RIGHT_LEG: 35}
    damage_type = "SNIPER_DAMAGE"
    falloff = 0.03


WEAPONS = {cls.type: cls for cls in Weapon.__subclasses__()}


class Grenade(Tool):
    type = WEAPON.GRENADE_TOOL
    name = "Grenade"
    max_primary = 3
    
    # Model properties
    model = []  # GRENADE_MODEL
    view_model = []  # GRENADE_VIEW_MODEL
    
    # Sound properties
    throw_sound = "GRENADE_THROW_SOUND"
    explosion_sound = "GRENADE_EXPLOSION_SOUND"
    
    explosion_damage = 100
    explosion_radius = 3

    def on_primary(self, *args, **kwargs):
        if self.primary_ammo <= 0:
            return False
        self.primary_ammo -= 1
        return True
