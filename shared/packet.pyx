from libc.stddef cimport size_t
from libc.string cimport memcpy
from shared.bytes cimport ByteReader, ByteWriter
from libc.stdint cimport uint64_t
import cython

cdef inline int to_color(object color):
    """Convert color to wire format (reverse byte order)
    Works with both int color (0xRRGGBB) and tuple color (r,g,b)"""
    cdef int r, g, b
    
    if isinstance(color, tuple) and len(color) >= 3:
        r = color[0]
        g = color[1]
        b = color[2]
    else:
        # Assume int format 0xRRGGBB
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
    
    # Return in reversed wire format
    return (r << 24) | (g << 16) | (b << 8)

cdef inline object from_color(object color, bint as_tuple=False):
    """Convert wire format color (reverse byte order) to normal format
    If as_tuple is True, returns (r,g,b) tuple, otherwise returns 0xRRGGBB int"""
    cdef int r, g, b
    
    if isinstance(color, tuple) and len(color) >= 3:
        # Already a tuple, use as is for Python 2.7 compatibility
        return color
    else:
        # Extract from Python 2.7 lib wire format
        r = (color >> 24) & 0xFF
        g = (color >> 16) & 0xFF
        b = (color >> 8) & 0xFF
    
    if as_tuple:
        return (r, g, b)
    else:
        return (r << 16) | (g << 8) | b

# Function to read color bytes and return in desired format
cdef inline object read_color(ByteReader reader, bint as_tuple=False):
    """Read 3 color bytes and return in desired format"""
    cdef int r, g, b
    
    # Read 3 bytes in Python 2.7 order
    b = reader.read_byte()
    g = reader.read_byte()
    r = reader.read_byte()
    
    if as_tuple:
        # For Python 2.7 compatibility, return as (r,g,b)
        return (r, g, b)
    else:
        return (r << 16) | (g << 8) | b

# Function to write color in either format
cdef inline void write_color(ByteWriter writer, object color):
    """Write color (either int or tuple) to writer in byte-reversed format"""
    cdef int r, g, b
    
    if isinstance(color, tuple) and len(color) >= 3:
        # Color is a tuple (r,g,b)
        r = color[0]
        g = color[1] 
        b = color[2]
    else:
        # Assume int 0xRRGGBB format
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
    
    # Write in Python 2.7 lib format
    writer.write_byte(b)
    writer.write_byte(g)
    writer.write_byte(r)

cdef inline int tofixed(double v):
    """
    Convert a float into a fixed-point representation.
    """
    cdef int iv, mag, sgn
    v = v * 64 + 0.5
    iv = <int>v
    mag = iv if iv >= 0 else -iv
    if mag > 0x7FFF:
        mag = 0x7FFF
    sgn = 0x8000 if iv < 0 else 0
    return mag | sgn

cdef inline double fromfixed(int v):
    """Convert 1.6 fixed to float."""
    cdef int mag
    cdef double sgn
    sgn = -1.0 if (v & 0x8000) else 1.0
    mag = v & 0x7FFF
    
    # Standard scale - depends on application
    return sgn * (mag / 64.0)    

# String encoding/decoding helpers
def encode(s):
    """
    Encode string for Python 3 compatibility
    """
    if isinstance(s, str):
        return s
    return s.decode('utf-8')

def decode(s):
    """
    Decode string for Python 3 compatibility
    """
    if isinstance(s, str):
        return s
    return s.encode('utf-8')

# Loader functions - simple placeholders for now
def load_client_packet():
    """Placeholder for client packet loader function"""
    return None

def load_server_packet():
    """Placeholder for server packet loader function"""
    return None

def load_master_packet():
    """Placeholder for master packet loader function"""
    return None

# Base classes
cdef class Entity:
    pass

cdef class PacketLoader:
    pass

@cython.freelist(512)
cdef class Loader:
    id: int = -1

    def __init__(self, ByteReader reader = None):
        if reader is not None:
            self.read(reader)

    cpdef read(self, ByteReader reader):
        raise NotImplementedError

    cpdef write(self, ByteWriter writer):
        raise NotImplementedError

    cpdef ByteWriter generate(self):
        cdef ByteWriter writer = ByteWriter()
        self.write(writer)
        return writer

# Packet Classes
cdef class AddServer(Loader): # Fixed BUT WTF?
    id: int = 0
    compress_packet: bool = False
    cdef public:
        int count
        str game_mode
        str map
        int max_players
        str name
        int port

    cpdef read(self, ByteReader reader):
        self.count = reader.read_byte()
        self.game_mode = None
        self.map = None
        self.max_players = 0
        self.name = None
        self.port = 0

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.count)

cdef class BlockBuild(Loader): # Fixed
    id: int = 32
    compress_packet: bool = False
    cdef public:
        int loop_count, player_id, block_type 
        int x, y, z

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.player_id = reader.read_byte()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()
        self.block_type = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.player_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)
        writer.write_byte(self.block_type)

cdef class BlockBuildColored:
    pass

cdef class BlockLiberate(Loader): # Fixed
    id: int = 35
    compress_packet: bool = False
    cdef public:
        int loop_count
        int player_id
        int x, y, z

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.player_id = reader.read_byte()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.player_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)

cdef class BlockLine(Loader): # Fixed
    id: int = 40
    compress_packet: bool = False
    cdef public:
        int player_id
        int loop_count
        int x1, y1, z1, x2, y2, z2

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.player_id = reader.read_byte()
        self.x1 = reader.read_short()
        self.y1 = reader.read_short()
        self.z1 = reader.read_short()
        self.x2 = reader.read_short()
        self.y2 = reader.read_short()
        self.z2 = reader.read_short()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.player_id)
        writer.write_short(self.x1)
        writer.write_short(self.y1)
        writer.write_short(self.z1)
        writer.write_short(self.x2)
        writer.write_short(self.y2)
        writer.write_short(self.z2)

cdef class BlockManagerState: 
    pass

cdef class BlockOccupy(Loader): # Fixed
    id: int = 34
    compress_packet: bool = False
    cdef public:
        int loop_count
        int player_id
        int x, y, z

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.player_id = reader.read_byte()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.player_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)

cdef class BlockSuckerPacket(Loader): # Fixed
    id: int = 94
    compress_packet: bool = False
    cdef public:
        int loop_count
        int shooter_id, state, shot

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.shooter_id = reader.read_byte()
        self.state = reader.read_byte()
        self.shot = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.shooter_id)
        writer.write_byte(self.state)
        writer.write_byte(self.shot)

cdef class BuildPrefabAction:
    pass

cdef class ChangeClass(Loader): # Fixed
    id: int = 78
    compress_packet: bool = False
    cdef public:
        int player_id, class_id

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.class_id = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.class_id)

cdef class ChangeEntity:
    pass

cdef class ChangePlayer(Loader): # Fixed
    id: int = 17
    compress_packet: bool = False
    cdef public:
        int player_id
        int type, chase_cam, high_minimap_visibility

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_short()
        self.type = reader.read_byte()

        if self.type == 8: # Idk what this is for check constants.py for more info
            self.high_minimap_visibility = reader.read_byte()

        if self.type == 9: # Idk what this is for check constants.py for more info
            self.chase_cam = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_short(self.player_id)
        writer.write_byte(self.type) 
        if self.type == 8: # Idk what this is for check constants.py for more info
            writer.write_byte(self.high_minimap_visibility)
        if self.type == 9: # Idk what this is for check constants.py for more info
            writer.write_byte(self.chase_cam)

cdef class ChangeTeam(Loader): # Fixed
    id: int = 77
    compress_packet: bool = False
    cdef public:
        int player_id, team

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.team = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.team)

cdef class ChatMessage(Loader): # Fixed
    id: int = 49
    compress_packet: bool = False
    cdef public:
        int player_id, chat_type
        str value

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.chat_type = reader.read_byte()
        self.value = reader.read_string()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.chat_type)
        writer.write_string(self.value)

cdef class ClientData:
    pass

cdef class ClientInMenu(Loader): # Fixed
    id: int = 110
    compress_packet: bool = False
    cdef public:
        int in_menu

    cpdef read(self, ByteReader reader):
        self.in_menu = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.in_menu)

cdef class ClockSync(Loader): # Fixed
    id: int = 0
    compress_packet: bool = False
    cdef public:
        int client_time, server_loop_count

    cpdef read(self, ByteReader reader):
        self.client_time = reader.read_int()
        self.server_loop_count = reader.read_int()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.client_time)
        writer.write_int(self.server_loop_count)

cdef class CreateAmbientSound(Loader): # Fixed
    id: int = 22
    compress_packet: bool = False
    cdef public:
        int loop_id
        str name
        list points

    cpdef read(self, ByteReader reader):
        self.name = reader.read_string()
        self.loop_id = reader.read_int()
        self.points = []
        for i in range(reader.read_byte()):
            self.points.append((reader.read_short(), reader.read_short(), reader.read_short()))

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_string(self.name)
        writer.write_int(self.loop_id)
        writer.write_byte(len(self.points))
        for point in self.points:
            writer.write_short(point[0])
            writer.write_short(point[1])
            writer.write_short(point[2])

cdef class CreateEntity:
    pass

cdef class CreatePlayer:
    pass

cdef class Damage: # Suspission on position
    pass

cdef class DebugDraw(Loader): # Fixed
    id: int = 107
    compress_packet: bool = False
    cdef public:
        int colour, frames, type
        float size, x, x2, y, y2, z, z2
        
    cpdef read(self, ByteReader reader):
        self.type = reader.read_byte()
        self.colour = reader.read_int()
        self.frames = reader.read_int()
        
        # Initialize all values to 0
        self.size = 0.0
        self.x = 0.0
        self.y = 0.0 
        self.z = 0.0
        self.x2 = 0.0
        self.y2 = 0.0
        self.z2 = 0.0
            
        # Read data based on type
        if self.type == 0:  # Box - all coordinates
            self.x = reader.read_float()
            self.y = reader.read_float()
            self.z = reader.read_float()
            self.x2 = reader.read_float()
            self.y2 = reader.read_float()
            self.z2 = reader.read_float()
        elif self.type == 1:  # Sphere - center point
            self.x = reader.read_float()
            self.y = reader.read_float()
            self.z = reader.read_float()

        # Read size byte if it's a sphere (type 1)
        if self.type == 1:
            self.size = fromfixed(reader.read_short())
        # Types 2, 3, 4 don't have additional data
            
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.type)
        writer.write_int(self.colour)
        writer.write_int(self.frames)
            
        # Write data based on type
        if self.type == 0:  # Box - all coordinates
            writer.write_float(self.x)
            writer.write_float(self.y)
            writer.write_float(self.z)
            writer.write_float(self.x2)
            writer.write_float(self.y2)
            writer.write_float(self.z2)
        elif self.type == 1:  # Sphere - center point
            writer.write_float(self.x)
            writer.write_float(self.y)
            writer.write_float(self.z)

        # Write size byte if it's a sphere (type 1)
        if self.type == 1:
            writer.write_short(tofixed(self.size))

        # Types 2, 3, 4 don't have additional data

cdef class DestroyEntity(Loader): # Fixed
    id: int = 19
    compress_packet: bool = False
    cdef public:
        int entity_id

    cpdef read(self, ByteReader reader):
        self.entity_id = reader.read_short()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_short(self.entity_id)

    def set_entity(self, entity):
        self.entity_id = entity.id

cdef class DetonateC4(Loader): # Fixed
    id: int = 93
    compress_packet: bool = False
    cdef public:
        int loop_count

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)

cdef class DisableEntity(Loader): # Fixed
    id: int = 96
    compress_packet: bool = False
    cdef public:
        int entity_id

    cpdef read(self, ByteReader reader):
        self.entity_id = reader.read_short()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_short(self.entity_id)

cdef class DisguisePacket(Loader): # Fixed
    id: int = 95
    compress_packet: bool = False
    cdef public:
        int loop_count
        int active

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.active = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.active)

cdef class DisplayCountdown(Loader): # Fixed
    id: int = 84
    compress_packet: bool = False
    cdef public:
        float timer

    cpdef read(self, ByteReader reader):
        self.timer = reader.read_float()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_float(self.timer)

cdef class DropPickup(Loader): # Fixed
    id: int = 71
    compress_packet: bool = False
    cdef public:
        int loop_count
        int player_id, pickup_id
        tuple position, velocity

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.player_id = reader.read_byte()
        self.pickup_id = reader.read_byte()
        self.position = (fromfixed(reader.read_short()), fromfixed(reader.read_short()), fromfixed(reader.read_short()))
        self.velocity = (fromfixed(reader.read_short()), fromfixed(reader.read_short()), fromfixed(reader.read_short()))

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.player_id)
        writer.write_byte(self.pickup_id)
        writer.write_short(tofixed(self.position[0]))
        writer.write_short(tofixed(self.position[1]))
        writer.write_short(tofixed(self.position[2]))
        writer.write_short(tofixed(self.velocity[0]))
        writer.write_short(tofixed(self.velocity[1]))
        writer.write_short(tofixed(self.velocity[2]))

cdef class EntityUpdates:
    pass

cdef class ErasePrefabAction:
    pass

cdef class ExistingPlayer:
    pass

cdef class ExplodeCorpse(Loader): # Fixed
    id: int = 36
    compress_packet: bool = False
    cdef public:
        int player_id, show_explosion_effect

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.show_explosion_effect = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.show_explosion_effect)

cdef class FogColor(Loader): # Fixed
    id: int = 74
    compress_packet: bool = False
    cdef public:
        int color
        
    cpdef read(self, ByteReader reader):
        # Read color in Python 2.7 format and convert to standard format
        self.color = from_color(reader.read_int())
        
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        # Convert color to Python 2.7 format and write
        writer.write_int(to_color(self.color))

cdef class ForceShowScores(Loader): # Fixed
    id: int = 72
    compress_packet: bool = False
    cdef public:
        int forced

    cpdef read(self, ByteReader reader):
        self.forced = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.forced)

cdef class ForceTeamJoin(Loader): # Fixed
    id: int = 115
    compress_packet: bool = False
    cdef public:
        int team_id, instant

    cpdef read(self, ByteReader reader):
        self.team_id = reader.read_byte()
        self.instant = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.team_id)
        writer.write_byte(self.instant)

cdef class GameStats:
    pass

cdef class GenericVoteMessage(Loader): # Fixed
    id: int = 109
    compress_packet: bool = False
    cdef public:
        int player_id, message_type
        str description, title
        int can_vote, allow_revote, hide_after_vote
        list candidates # list {'name': str, 'votes': int} {name: '1', votes: 1}

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.message_type = reader.read_byte()

        # Read candidates list
        self.candidates = []
        count = reader.read_byte()
        for i in range(count):
            name = reader.read_string()
            votes = reader.read_byte()
            self.candidates.append({"name": name, "votes": votes})

        self.title = reader.read_string()
        self.description = reader.read_string()

        cdef int vote_flags = reader.read_byte()
        self.allow_revote = (vote_flags & 0x01) != 0
        self.hide_after_vote = (vote_flags & 0x02) != 0
        self.can_vote = (vote_flags & 0x04) != 0
        
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.message_type)

        # Write candidates list
        writer.write_byte(len(self.candidates))
        for candidate in self.candidates:
            writer.write_string(candidate["name"])
            writer.write_byte(candidate["votes"])

        writer.write_string(self.title)
        writer.write_string(self.description)

        writer.write_byte(self.can_vote | (self.allow_revote << 1) | (self.hide_after_vote << 2))

cdef class HelpMessage(Loader): # Fixed
    id: int = 109
    compress_packet: bool = False
    cdef public:
        float delay
        list message_ids
        
    def __cinit__(self):
        self.message_ids = []
        
    cpdef read(self, ByteReader reader):
        self.delay = reader.read_float()
        count = reader.read_byte()
        self.message_ids = []
        for i in range(count):
            msg = reader.read_string()
            if msg:  # Only add non-empty strings
                self.message_ids.append(msg)
            
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_float(self.delay)
        writer.write_byte(len(self.message_ids))
        for msg_id in self.message_ids:
            writer.write_string(msg_id)

cdef class HitEntity(Loader): # Fixed
    id: int = 20
    compress_packet: bool = False
    cdef public:
        int entity_id
        float x, y, z
        int type

    cpdef read(self, ByteReader reader):
        self.entity_id = reader.read_short()
        self.x = fromfixed(reader.read_short())
        self.y = fromfixed(reader.read_short())
        self.z = fromfixed(reader.read_short())
        self.type = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_short(self.entity_id)
        writer.write_short(tofixed(self.x))
        writer.write_short(tofixed(self.y))
        writer.write_short(tofixed(self.z))
        writer.write_byte(self.type)

cdef class InitialInfo(Loader): # Should be working :D
    id: int = 114
    compress_packet: bool = False
    cdef public:
        uint64_t server_steam_id
        int server_ip, server_port
        str mode_name, mode_description, mode_infographic_text1, mode_infographic_text2, mode_infographic_text3
        str map_name, filename
        int checksum, mode_key
        int map_is_ugc
        int query_port
        int classic, enable_minimap, same_team_collision
        int max_draw_distance
        int enable_colour_picker, enable_colour_palette, enable_deathcam, enable_sniper_beam, enable_spectator, exposed_teams_always_on_minimap, enable_numeric_hp
        str texture_skin
        int beach_z_modifiable
        int enable_minimap_height_icons, enable_fall_on_water_damage
        float block_wallet_multiplier, block_health_multiplier
        list disabled_tools, disabled_classes, movement_speed_multipliers, ugc_prefab_sets
        dict loadout_overrides
        int enable_player_score
        str server_name
        list ground_colors
        int allow_shooting_holding_intel, friendly_fire
        list custom_game_rules
        int enable_corpse_explosion
        int ugc_mode

    def __init__(self, ByteReader reader = None):
        self.disabled_tools = []
        self.disabled_classes = []
        self.movement_speed_multipliers = []
        self.ugc_prefab_sets = []
        self.loadout_overrides = {}
        self.ground_colors = []
        self.custom_game_rules = []
        if reader is not None:
            self.read(reader)

    cpdef read(self, ByteReader reader):
        self.server_steam_id = reader.read_uint64()
        self.server_ip = reader.read_int()
        self.server_port = reader.read_int()
        self.mode_name = reader.read_string()
        self.mode_description = reader.read_string()
        self.mode_infographic_text1 = reader.read_string()
        self.mode_infographic_text2 = reader.read_string()
        self.mode_infographic_text3 = reader.read_string()
        self.map_name = reader.read_string()
        self.filename = reader.read_string()
        self.checksum = reader.read_int()
        self.mode_key = reader.read_byte()
        self.map_is_ugc = reader.read_byte()
        # Convert from signed to unsigned for query_port (preserve bit pattern)
        query_port_signed = reader.read_short()
        self.query_port = query_port_signed & 0xFFFF if query_port_signed < 0 else query_port_signed
        self.classic = reader.read_byte()
        self.enable_minimap = reader.read_byte()
        self.same_team_collision = reader.read_byte()
        self.max_draw_distance = reader.read_byte() # Check
        self.enable_colour_picker = reader.read_byte()
        self.enable_colour_palette = reader.read_byte()
        self.enable_deathcam = reader.read_byte()
        self.enable_sniper_beam = reader.read_byte()
        self.enable_spectator = reader.read_byte()
        self.exposed_teams_always_on_minimap = reader.read_byte()
        self.enable_numeric_hp = reader.read_byte()
        self.texture_skin = reader.read_string()
        self.beach_z_modifiable = reader.read_byte()
        self.enable_minimap_height_icons = reader.read_byte()
        self.enable_fall_on_water_damage = reader.read_byte()
        self.block_wallet_multiplier = fromfixed(reader.read_short())
        self.block_health_multiplier = fromfixed(reader.read_short())

        # Tools
        disabled_tools_size = reader.read_byte()
        for i in range(disabled_tools_size):
            disabled_tool = reader.read_byte()
            self.disabled_tools.append(disabled_tool)

        # Classes
        disabled_classes_size = reader.read_byte()
        for i in range(disabled_classes_size):
            disabled_class = reader.read_byte()
            self.disabled_classes.append(disabled_class)

        # Movement Speed Multipliers
        movement_speed_multipliers_size = reader.read_byte()
        for i in range(movement_speed_multipliers_size):
            movement_speed_multiplier = fromfixed(reader.read_short())
            self.movement_speed_multipliers.append(movement_speed_multiplier)

        # UGC Prefab Sets
        ugc_prefab_sets_size = reader.read_byte()
        for i in range(ugc_prefab_sets_size):
            ugc_prefab_set = reader.read_string()
            self.ugc_prefab_sets.append(ugc_prefab_set)

        # Loadout Overrides FUCK THIS FOR NOW!
        #self.loadout_overrides = {}
        #loadout_overrides_size = reader.read_short()
        #for i in range(loadout_overrides_size):
        #    key = reader.read_string()
        #    value = reader.read_byte()
        #    self.loadout_overrides[key] = value

        self.enable_player_score = reader.read_byte()
        self.server_name = reader.read_string()

        # initial_info.ground_colors = [(1,1,1,1), (2,2,2,2)]
        ground_colors_size = reader.read_byte()
        for i in range(ground_colors_size):
            ground_color = reader.read_byte()
            self.ground_colors.append(ground_color)

        if(ground_colors_size == 0): 
            reader.read_byte()

        # Ensure consistent boolean interpretation (0 or 1)
        self.allow_shooting_holding_intel = reader.read_byte() & 0xFF
        self.friendly_fire = reader.read_byte() & 0xFF
        # custom_game_rules = [("test","test")]
        custom_game_rules_size = reader.read_byte()
        for i in range(custom_game_rules_size):
            custom_game_rule = reader.read_string()
            self.custom_game_rules.append(custom_game_rule)

        self.enable_corpse_explosion = reader.read_byte() & 0xFF
        self.ugc_mode = reader.read_byte() & 0xFF

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_uint64(self.server_steam_id)
        writer.write_int(self.server_ip)
        writer.write_int(self.server_port)
        writer.write_string(self.mode_name)
        writer.write_string(self.mode_description)
        writer.write_string(self.mode_infographic_text1)
        writer.write_string(self.mode_infographic_text2)
        writer.write_string(self.mode_infographic_text3)
        writer.write_string(self.map_name)
        writer.write_string(self.filename)
        writer.write_int(self.checksum)
        writer.write_byte(self.mode_key)
        writer.write_byte(self.map_is_ugc)
        # Ensure query_port is properly encoded as unsigned
        writer.write_short(self.query_port & 0xFFFF)
        writer.write_byte(self.classic)
        writer.write_byte(self.enable_minimap)
        writer.write_byte(self.same_team_collision)
        writer.write_byte(self.max_draw_distance)
        writer.write_byte(self.enable_colour_picker)
        writer.write_byte(self.enable_colour_palette)
        writer.write_byte(self.enable_deathcam)
        writer.write_byte(self.enable_sniper_beam)
        writer.write_byte(self.enable_spectator)
        writer.write_byte(self.exposed_teams_always_on_minimap)
        writer.write_byte(self.enable_numeric_hp)
        writer.write_string(self.texture_skin)
        writer.write_byte(self.beach_z_modifiable)
        writer.write_byte(self.enable_minimap_height_icons)
        writer.write_byte(self.enable_fall_on_water_damage)
        writer.write_short(tofixed(self.block_wallet_multiplier))
        writer.write_short(tofixed(self.block_health_multiplier))

        # Tools
        writer.write_byte(len(self.disabled_tools))
        for disabled_tool in self.disabled_tools:
            writer.write_byte(disabled_tool)

        # Classes
        writer.write_byte(len(self.disabled_classes))
        for disabled_class in self.disabled_classes:
            writer.write_byte(disabled_class)

        # Movement Speed Multipliers
        writer.write_byte(len(self.movement_speed_multipliers))
        for movement_speed_multiplier in self.movement_speed_multipliers:
            writer.write_short(tofixed(movement_speed_multiplier))

        # UGC Prefab Sets
        writer.write_byte(len(self.ugc_prefab_sets))
        for ugc_prefab_set in self.ugc_prefab_sets:
            writer.write_string(ugc_prefab_set)

        # Loadout Overrides FUCK THIS FOR NOW!
        #writer.write_byte(len(self.loadout_overrides))
        #for key, value in self.loadout_overrides.items():
        #    writer.write_string(str(key))
        #    writer.write_byte(int(value))

        writer.write_byte(self.enable_player_score)
        writer.write_string(self.server_name)

        # Ground Colors
        writer.write_byte(len(self.ground_colors))
        for ground_color in self.ground_colors:
            writer.write_byte(ground_color)

        if(len(self.ground_colors) == 0): 
            writer.write_byte(0)

        writer.write_byte(self.allow_shooting_holding_intel & 0xFF)
        writer.write_byte(self.friendly_fire & 0xFF)

        writer.write_byte(len(self.custom_game_rules))
        for custom_game_rule in self.custom_game_rules:
            writer.write_string(custom_game_rule)

        writer.write_byte(self.enable_corpse_explosion & 0xFF)
        writer.write_byte(self.ugc_mode & 0xFF)

        
        
        
        

cdef class InitialUGCBatch:
    pass

cdef class InitiateKickMessage(Loader): # Fixed
    id: int = 48
    compress_packet: bool = False
    cdef public:
        int player_id, target_id, reason

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.target_id = reader.read_byte()
        self.reason = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.target_id)
        writer.write_byte(self.reason)

cdef class KillAction(Loader): # Fixed
    id: int = 46
    compress_packet: bool = False
    cdef public:
        int player_id, killer_id, kill_type, respawn_time
        bint isDominationKill, isRevengeKill
        int kill_count

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.killer_id = reader.read_byte()
        self.kill_type = reader.read_byte()
        self.respawn_time = reader.read_byte()
        self.kill_count = reader.read_byte()
        self.isDominationKill = <bint>reader.read_byte()
        self.isRevengeKill = <bint>reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.killer_id)
        writer.write_byte(self.kill_type)
        writer.write_byte(self.respawn_time)
        writer.write_byte(self.kill_count)
        writer.write_byte(<bint>self.isDominationKill)
        writer.write_byte(<bint>self.isRevengeKill)

cdef class LocalisedMessage:
    pass

cdef class LockTeam(Loader): # Fixed
    id: int = 79
    compress_packet: bool = False
    cdef public:
        int team_id, locked

    cpdef read(self, ByteReader reader):
        self.team_id = reader.read_byte()
        self.locked = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.team_id)
        writer.write_byte(self.locked)

cdef class LockToZone(Loader): # WTF is this? Fixed?
    id: int = 108
    compress_packet: bool = False
    cdef public:
        int A2018, A2020, A2022, A2019, A2021, A2023

    cpdef read(self, ByteReader reader):
        self.A2018 = reader.read_short()
        self.A2020 = reader.read_short()
        self.A2022 = reader.read_short()
        self.A2019 = reader.read_short()
        self.A2021 = reader.read_short()
        self.A2023 = reader.read_short()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_short(self.A2018)
        writer.write_short(self.A2020)
        writer.write_short(self.A2022)
        writer.write_short(self.A2019)
        writer.write_short(self.A2021)
        writer.write_short(self.A2023)

cdef class MapDataChunk:
    pass

cdef class MapDataEnd:
    pass

cdef class MapDataStart:
    pass

cdef class MapDataValidation(Loader): # No way this works
    id: int = 60
    compress_packet: bool = False
    cdef public:
        str crc

    cpdef read(self, ByteReader reader):
        self.crc = reader.read_int()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.crc)

cdef class MapEnded(Loader): # Fixed
    id: int = 58
    compress_packet: bool = False
    cpdef read(self, ByteReader reader):
        pass

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)

cdef class MapSyncChunk(Loader): # No way this works
    id: int = 57
    compress_packet: bool = True
    cdef public:
        bytes data
        int percent_complete

    cpdef read(self, ByteReader reader):
        self.data = reader.get()
        self.percent_complete = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.percent_complete)
        writer.write_short(len(self.data)) # not sure
        writer.write(self.data)

cdef class MapSyncEnd(Loader): # Fixed
    id: int = 59
    compress_packet: bool = False
    cpdef read(self, ByteReader reader):
        pass

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)

cdef class MapSyncStart(Loader): # Fixed
    id: int = 55
    compress_packet: bool = False
    cdef public:
        int size

    cpdef read(self, ByteReader reader):
        self.size = reader.read_int()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)

cdef class MinimapBillboard(Loader): # Fixed
    id: int = 41
    compress_packet: bool = False
    cdef public:
        int entity_id, key, tracking
        tuple color
        str icon_name
        float x, y, z
        
    cpdef read(self, ByteReader reader):
        self.entity_id = reader.read_byte()
        self.key = reader.read_byte()
        
        # Read color tuple in Python 2.7 format
        b = reader.read_byte()
        g = reader.read_byte()
        r = reader.read_byte()
        self.color = (r, g, b)  # Store as RGB
        
        # Read coordinates
        self.x = fromfixed(reader.read_short())
        self.y = fromfixed(reader.read_short())
        self.z = fromfixed(reader.read_short())
        
        # Read icon name
        self.icon_name = reader.read_string()
        
        # Read tracking flag
        self.tracking = reader.read_byte()
        
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.entity_id)
        writer.write_byte(self.key)
        
        # Write color tuple in Python 2.7 lib format
        if self.color is not None and len(self.color) >= 3:
            writer.write_byte(self.color[2])  # Write blue
            writer.write_byte(self.color[1])  # Write green
            writer.write_byte(self.color[0])  # Write red
        else:
            # Write zeros if color is missing
            writer.write_byte(0)
            writer.write_byte(0)
            writer.write_byte(0)
            
        # Write coordinates
        writer.write_short(tofixed(self.x))
        writer.write_short(tofixed(self.y))
        writer.write_short(tofixed(self.z))
        
        # Write icon name
        writer.write_string(self.icon_name if self.icon_name else "")
        
        # Write tracking flag
        writer.write_byte(self.tracking)

cdef class MinimapBillboardClear(Loader): # Fixed
    id: int = 42
    compress_packet: bool = False
    cdef public:
        int entity_id

    cpdef read(self, ByteReader reader):
        self.entity_id = reader.read_short()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_short(self.entity_id)

cdef class MinimapZone(Loader): # Fixed
    id: int = 43 
    compress_packet: bool = False
    cdef public:
        int A2018, A2019, A2020, A2021, A2022, A2023
        tuple color
        int icon_id
        float icon_scale
        int key, locked_in_zone
        
    cpdef read(self, ByteReader reader):
        self.key = reader.read_byte()
        
        # Read color tuple in Python 2.7 format
        b = reader.read_byte()
        g = reader.read_byte()
        r = reader.read_byte()
        self.color = (r, g, b)  # Store as RGB
        
        # Read various fields
        self.A2018 = reader.read_short()
        self.A2020 = reader.read_short()
        self.A2022 = reader.read_short()
        self.A2019 = reader.read_short()
        self.A2021 = reader.read_short()
        self.A2023 = reader.read_short()
        
        # Read remaining fields
        self.icon_scale = fromfixed(reader.read_short())
        self.icon_id = reader.read_byte()
        self.locked_in_zone = reader.read_byte()
        
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.key)
        
        # Write color in Python 2.7 format
        if self.color is not None and len(self.color) >= 3:
            writer.write_byte(self.color[2])  # Write blue
            writer.write_byte(self.color[1])  # Write green
            writer.write_byte(self.color[0])  # Write red
        else:
            # Write zeros if color is missing
            writer.write_byte(0)
            writer.write_byte(0)
            writer.write_byte(0)
            
        # Write various fields
        writer.write_short(self.A2018)
        writer.write_short(self.A2020)
        writer.write_short(self.A2022)
        writer.write_short(self.A2019)
        writer.write_short(self.A2021)
        writer.write_short(self.A2023)
        
        # Write remaining fields
        writer.write_short(tofixed(self.icon_scale))
        writer.write_byte(self.icon_id)
        writer.write_byte(self.locked_in_zone)

cdef class MinimapZoneClear(Loader): # Fixed
    id: int = 44 
    compress_packet: bool = False
    cdef public:
        int A2018, A2019, A2020, A2021, A2022, A2023
        
    cpdef read(self, ByteReader reader):
        self.A2018 = reader.read_short()
        self.A2020 = reader.read_short()
        self.A2022 = reader.read_short()
        self.A2019 = reader.read_short()
        self.A2021 = reader.read_short()
        self.A2023 = reader.read_short()

        
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_short(self.A2018)
        writer.write_short(self.A2020)
        writer.write_short(self.A2022)
        writer.write_short(self.A2019)
        writer.write_short(self.A2021)
        writer.write_short(self.A2023)

cdef class NewPlayerConnection:
    pass

cdef class POIFocus(Loader): # Fixed
    id: int = 18
    compress_packet: bool = False   

    cdef public:
        float target_x, target_y, target_z

    cpdef read(self, ByteReader reader):
        self.target_x = fromfixed(reader.read_short())
        self.target_y = fromfixed(reader.read_short())
        self.target_z = fromfixed(reader.read_short())

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_short(tofixed(self.target_x))
        writer.write_short(tofixed(self.target_y))
        writer.write_short(tofixed(self.target_z))

cdef class PackChunk(Loader): # Fixed
    id: int = 63
    compress_packet: bool = False
    cdef public:
        bytes data

    cpdef read(self, ByteReader reader):
        self.data = reader.get()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write(self.data)

cdef class PackResponse(Loader): # Fixed
    id: int = 62
    compress_packet: bool = False
    cdef public:
        int value

    cpdef read(self, ByteReader reader):
        self.value = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.value)

cdef class PackStart(Loader): # Fixed
    id: int = 61
    compress_packet: bool = False
    cdef public:
        int size, checksum

    cpdef read(self, ByteReader reader):
        self.size = reader.read_int()
        self.checksum = reader.read_int()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.size)
        writer.write_int(self.checksum)

cdef class PaintBlockPacket:
    pass

cdef class Password(Loader): # Fixed
    id: int = 111
    compress_packet: bool = True

    cdef public:
        str password

    cpdef read(self, ByteReader reader):
        self.password = reader.read_string()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_string(self.password)

cdef class PasswordNeeded(Loader): # Fixed
    id: int = 112
    compress_packet: bool = False

    cpdef read(self, ByteReader reader):
        pass

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)

cdef class PasswordProvided(Loader): # Fixed
    id: int = 113
    compress_packet: bool = True

    cdef public:
        str password

    cpdef read(self, ByteReader reader):
        self.password = reader.read_string()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_string(self.password)

cdef class PickPickup(Loader): # Fixed
    id: int = 70
    compress_packet: bool = False
    cdef public:
        int player_id, pickup_id, burdensome

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.pickup_id = reader.read_byte()
        self.burdensome = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.pickup_id)
        writer.write_byte(self.burdensome)

cdef class PlaceC4(Loader): # Fixed
    id: int = 92
    compress_packet: bool = False
    cdef public:
        int loop_count
        int x, y, z
        int face

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()
        self.face = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)
        writer.write_byte(self.face)

cdef class PlaceDynamite(Loader): # Fixed
    id: int = 1
    compress_packet: bool = False
    cdef public:
        int loop_count
        int x, y, z
        int face

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()
        self.face = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)
        writer.write_byte(self.face)

cdef class PlaceFlareBlock(Loader): # Fixed
    id: int = 104
    compress_packet: bool = False
    cdef public:
        int loop_count
        int x, y, z

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)

cdef class PlaceLandmine(Loader): # Fixed
    id: int = 89
    compress_packet: bool = False
    cdef public:
        int loop_count
        int player_id
        int x, y, z

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.player_id = reader.read_byte()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.player_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)

cdef class PlaceMG(Loader): # Fixed
    id: int = 87
    compress_packet: bool = False
    cdef public:
        int loop_count, player_id 
        int x, y, z
        float yaw

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.player_id = reader.read_byte()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()
        self.yaw = fromfixed(reader.read_short())

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.player_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)
        writer.write_short(tofixed(self.yaw))

cdef class PlaceMedPack(Loader): # Fixed
    id: int = 90
    compress_packet: bool = False
    cdef public:
        int loop_count, player_id
        int x, y, z
        int face

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.player_id = reader.read_byte()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()
        self.face = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.player_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)
        writer.write_byte(self.face)

cdef class PlaceRadarStation(Loader): # Fixed
    id: int = 91
    compress_packet: bool = False
    cdef public:
        int loop_count, player_id
        int x, y, z

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.player_id = reader.read_byte()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.player_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)

cdef class PlaceRocketTurret(Loader): # Fixed
    id: int = 88
    compress_packet: bool = False
    cdef public:
        int loop_count, player_id 
        int x, y, z
        float yaw

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.player_id = reader.read_byte()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()
        self.yaw = fromfixed(reader.read_short())

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.player_id)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)
        writer.write_short(tofixed(self.yaw))

cdef class PlaceUGC(Loader): # Fixed
    id: int = 97
    compress_packet: bool = False
    cdef public:
        int loop_count
        int x, y, z
        int ugc_item_id, placing

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.x = reader.read_short()
        self.y = reader.read_short()
        self.z = reader.read_short()
        self.ugc_item_id = reader.read_byte()
        self.placing = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_short(self.x)
        writer.write_short(self.y)
        writer.write_short(self.z)
        writer.write_byte(self.ugc_item_id)
        writer.write_byte(self.placing)

cdef class PlayAmbientSound(Loader): # Fixed
    id: int = 24
    compress_packet: bool = False
    cdef public:
        str name
        int loop_id
        bint looping, positioned
        float volume, time, attenuation
        float x, y, z


    cpdef read(self, ByteReader reader):
        self.name = reader.read_string()

        cdef int flags = reader.read_byte()
        self.looping    = flags & (1 << 0)
        self.positioned = flags & (1 << 1)

        self.volume = fromfixed(reader.read_short())
        self.time = fromfixed(reader.read_short())

        if self.looping:
            self.loop_id = reader.read_byte()
        if self.positioned:
            self.x = fromfixed(reader.read_short())
            self.y = fromfixed(reader.read_short())
            self.z = fromfixed(reader.read_short())
            self.attenuation = fromfixed(reader.read_short())

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_string(self.name)

        cdef int sound_flags = <bint>self.looping << 0 | <bint>self.positioned << 1
        writer.write_byte(sound_flags)

        writer.write_short(tofixed(self.volume))
        writer.write_short(tofixed(self.time))

        if self.looping:
            writer.write_byte(self.loop_id)
        if self.positioned:
            writer.write_short(tofixed(self.x))
            writer.write_short(tofixed(self.y))
            writer.write_short(tofixed(self.z))
            writer.write_short(tofixed(self.attenuation))

cdef class PlayMusic(Loader): # Fixed
    id: int = 26
    compress_packet: bool = False
    cdef public:
        str name
        float seconds_played

    cpdef read(self, ByteReader reader):
        self.name = reader.read_string()
        self.seconds_played = fromfixed(reader.read_short())

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_string(self.name)
        writer.write_short(tofixed(self.seconds_played))

cdef class PlaySound(Loader): # Fixed
    id: int = 23
    compress_packet: bool = False
    cdef public:
        int sound_id, loop_id
        bint looping, positioned
        float volume, time, attenuation
        float x, y, z

    cpdef read(self, ByteReader reader):
        self.sound_id = reader.read_byte()

        cdef int flags = reader.read_byte()
        self.looping    = flags & (1 << 0)
        self.positioned = flags & (1 << 1)

        self.volume = fromfixed(reader.read_short())
        self.time = fromfixed(reader.read_short())

        if self.looping:
            self.loop_id = reader.read_byte()
        if self.positioned:
            self.x = fromfixed(reader.read_short())
            self.y = fromfixed(reader.read_short())
            self.z = fromfixed(reader.read_short())
            self.attenuation = fromfixed(reader.read_short())

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.sound_id)

        cdef int sound_flags = <bint>self.looping << 0 | <bint>self.positioned << 1
        writer.write_byte(sound_flags)

        writer.write_short(tofixed(self.volume))
        writer.write_short(tofixed(self.time))

        if self.looping:
            writer.write_byte(self.loop_id)
        if self.positioned:
            writer.write_short(tofixed(self.x))
            writer.write_short(tofixed(self.y))
            writer.write_short(tofixed(self.z))
            writer.write_short(tofixed(self.attenuation))

cdef class PlayerLeft(Loader): # Fixed
    id: int = 64
    compress_packet: bool = False
    cdef public:
        int player_id

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)

cdef class PositionData:
    pass

cdef class PrefabComplete(Loader): # Fixed
    id: int = 29
    compress_packet: bool = False

    cpdef read(self, ByteReader reader):
        pass

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)


cdef class ProgressBar:
    pass

cdef class RankUps(Loader): # Fixed - string to int conversion for some reason Jagex :D
    id: int = 66
    compress_packet: bool = False
    cdef public:
        int noOfRankUps
        list old_scores, new_scores, score_reasons
        
    cpdef read(self, ByteReader reader):
        self.noOfRankUps = reader.read_int()
        
        # Clear existing lists
        self.old_scores = []
        self.new_scores = []
        self.score_reasons = []
        
        # Read each rank up data
        for i in range(self.noOfRankUps):
            self.score_reasons.append(reader.read_int())      # First is score_reason (integer)
            old_score_str = reader.read_string()              # Read old_score as string
            new_score_str = reader.read_string()              # Read new_score as string
            
            # Convert string scores to integers for consistency
            try:
                self.old_scores.append(int(old_score_str))
                self.new_scores.append(int(new_score_str))
            except:
                self.old_scores.append(0)
                self.new_scores.append(0)
        
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.noOfRankUps)
        
        # Write each rank up data
        for i in range(self.noOfRankUps):
            writer.write_int(self.score_reasons[i])                # First is score_reason (integer)
            writer.write_string(str(self.old_scores[i]))           # Write old_score as string
            writer.write_string(str(self.new_scores[i]))           # Write new_score as string

cdef class ReqestUGCEntities(Loader): # Fixed
    id: int = 99
    compress_packet: bool = False
    cdef public:
        int game_mode, in_ugc_mode

    cpdef read(self, ByteReader reader):
        self.game_mode = reader.read_byte()
        self.in_ugc_mode = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.game_mode)
        writer.write_byte(self.in_ugc_mode)

cdef class Restock(Loader): # Fixed
    id: int = 69
    compress_packet: bool = False
    cdef public:
        int player_id, type

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.type = reader.read_byte()
        
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.type)

cdef class ServerBlockAction:
    pass

cdef class ServerBlockItem:
    pass

cdef class SetClassLoadout(Loader): # Fixed
    id: int = 13
    compress_packet: bool = True
    cdef public:
        int class_id, player_id, instant
        list prefabs, ugc_tools, loadout

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.class_id = reader.read_byte()
        self.instant = reader.read_byte()
        self.prefabs = []
        self.ugc_tools = []
        self.loadout = []

        # Loadout
        loadout_size = reader.read_byte()
        for i in range(loadout_size):
            loadout = reader.read_byte()
            self.loadout.append(loadout)

        # Prefabs
        prefab_count = reader.read_byte()
        for i in range(prefab_count):
            prefab_b = reader.read_string()
            self.prefabs.append(prefab_b)
        
        # UGC Tools
        ugc_tool_count = reader.read_byte()
        for i in range(ugc_tool_count):
            ugc_tool = reader.read_byte()
            self.ugc_tools.append(ugc_tool)

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.class_id)
        writer.write_byte(self.instant)
        writer.write_byte(len(self.loadout))

        for loadout in self.loadout:
            writer.write_byte(loadout)

        writer.write_byte(len(self.prefabs))
        for prefab in self.prefabs:
            writer.write_string(prefab)

        writer.write_byte(len(self.ugc_tools))
        for ugc_tool in self.ugc_tools:
            writer.write_byte(ugc_tool)

cdef class SetColor:
    pass

cdef class SetGroundColors:
    pass

cdef class SetHP(Loader): # Fixed
    id: int = 5
    compress_packet: bool = False
    cdef public:
        int hp
        int damage_type
        float source_x, source_y, source_z

    cpdef read(self, ByteReader reader):
        self.hp = reader.read_byte()
        self.damage_type = reader.read_byte()
        self.source_x = fromfixed(reader.read_short())
        self.source_y = fromfixed(reader.read_short())
        self.source_z = fromfixed(reader.read_short())

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.hp)
        writer.write_byte(self.damage_type)
        writer.write_short(tofixed(self.source_x))
        writer.write_short(tofixed(self.source_y))
        writer.write_short(tofixed(self.source_z))


cdef class SetScore(Loader): # Fixed
    id: int = 85
    compress_packet: bool = False
    cdef public:
        int type, specifier, reason, value

    cpdef read(self, ByteReader reader):
        self.type = reader.read_byte()
        self.reason = reader.read_byte()
        self.specifier = reader.read_byte()
        self.value = reader.read_int()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.type)
        writer.write_byte(self.reason)
        writer.write_byte(self.specifier)
        writer.write_int(self.value)

cdef class SetUGCEditMode(Loader): # Fixed
    id: int = 12
    compress_packet: bool = False
    cdef public:
        int mode

    cpdef read(self, ByteReader reader):
        self.mode = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.mode)

cdef class ShootFeedbackPacket(Loader): # Fixed
    id: int = 8
    compress_packet: bool = False
    cdef public:
        int loop_count, seed, shooter_id, shot_on_world_update, tool_id

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.shooter_id = reader.read_byte()
        self.tool_id = reader.read_byte()
        self.shot_on_world_update = reader.read_int()
        self.seed = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.shooter_id)
        writer.write_byte(self.tool_id)
        writer.write_int(self.shot_on_world_update)
        writer.write_byte(self.seed)

cdef class ShootPacket(Loader): # Fixed
    id: int = 6
    compress_packet: bool = False
    cdef public:
        int shooter_id, affect_shooter
        int loop_count
        int damage, penetration
        float ori_x, ori_y, ori_z
        float x, y, z
        int secondary
        int shot_on_world_update
        int seed

    cpdef read(self, ByteReader reader):
        self.loop_count = reader.read_int()
        self.shooter_id = reader.read_byte()
        self.shot_on_world_update = reader.read_int()

        self.x = reader.read_float()
        self.y = reader.read_float()
        self.z = reader.read_float()

        self.ori_x = reader.read_float()
        self.ori_y = reader.read_float()
        self.ori_z = reader.read_float()
        
        self.damage = reader.read_short()
        self.penetration = reader.read_short()
        self.secondary = reader.read_byte()
        self.seed = reader.read_byte()


    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.loop_count)
        writer.write_byte(self.shooter_id)
        writer.write_int(self.shot_on_world_update)

        writer.write_float(self.x)
        writer.write_float(self.y)
        writer.write_float(self.z)

        writer.write_float(self.ori_x)
        writer.write_float(self.ori_y)
        writer.write_float(self.ori_z)
        
        writer.write_short(self.damage)
        writer.write_short(self.penetration)
        writer.write_byte(self.secondary)
        writer.write_byte(self.seed)

cdef class ShootResponse(Loader): # Fixed
    id: int = 9
    compress_packet: bool = False
    cdef public:
        int damage_by, damaged, blood
        float position_x, position_y, position_z

    cpdef read(self, ByteReader reader):
        self.damage_by = reader.read_byte()
        self.damaged = reader.read_byte()
        self.blood = reader.read_byte()
        self.position_x = fromfixed(reader.read_short())
        self.position_y = fromfixed(reader.read_short())
        self.position_z = fromfixed(reader.read_short())

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.damage_by)
        writer.write_byte(self.damaged)
        writer.write_byte(self.blood)
        writer.write_short(tofixed(self.position_x))
        writer.write_short(tofixed(self.position_y))
        writer.write_short(tofixed(self.position_z))

cdef class ShowGameStats(Loader): # Fixed
    id: int = 118
    compress_packet: bool = False

    cpdef read(self, ByteReader reader):
        pass

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)

cdef class ShowTextMessage(Loader): # Fixed
    id: int = 73
    compress_packet: bool = False
    cdef public:
        int message_id
        float duration

    cpdef read(self, ByteReader reader):
        self.message_id = reader.read_byte()
        self.duration = fromfixed(reader.read_short())

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.message_id)
        writer.write_short(tofixed(self.duration))

cdef class SkyboxData(Loader): # Fixed
    id: int = 51
    compress_packet: bool = False
    cdef public:
        str value
        
    cpdef read(self, ByteReader reader):
        self.value = reader.read_string()
        
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_string(self.value)

cdef class StateData:
    pass

cdef class SteamSessionTicket(Loader): # Fixed
    id: int = 105
    compress_packet: bool = False
    cdef public:
        int ticket_size
        bytes ticket

    cpdef read(self, ByteReader reader):
        self.ticket_size = reader.read_int()
        self.ticket = reader.read(self.ticket_size)

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(self.ticket_size)
        writer.write(self.ticket)
            

cdef class StopMusic(Loader): # Fixed
    id: int = 27
    compress_packet: bool = False
    cpdef read(self, ByteReader reader):
        pass

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)

cdef class StopSound(Loader): # Fixed
    id: int = 25
    compress_packet: bool = False
    cdef public:
        int loop_id

    cpdef read(self, ByteReader reader):
        self.loop_id = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.loop_id)

cdef class TeamInfiniteBlocks(Loader): # Fixed
    id: int = 82
    compress_packet: bool = False
    cdef public:
        int team_id, infinite_blocks

    cpdef read(self, ByteReader reader):
        self.team_id = reader.read_byte()
        self.infinite_blocks = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.team_id)
        writer.write_byte(self.infinite_blocks)

cdef class TeamLockClass(Loader): # Fixed
    id: int = 80
    compress_packet: bool = False
    cdef public:
        int team_id, locked

    cpdef read(self, ByteReader reader):
        self.team_id = reader.read_byte()
        self.locked = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.team_id)
        writer.write_byte(self.locked)

cdef class TeamLockScore(Loader): # Fixed
    id: int = 81
    compress_packet: bool = False
    cdef public:
        int team_id, locked

    cpdef read(self, ByteReader reader):
        self.team_id = reader.read_byte()
        self.locked = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.team_id)
        writer.write_byte(self.locked)

cdef class TeamMapVisibility(Loader): # Fixed
    id: int = 83
    compress_packet: bool = False
    cdef public:
        int team_id, visible

    cpdef read(self, ByteReader reader):
        self.team_id = reader.read_byte()
        self.visible = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.team_id)
        writer.write_byte(self.visible)

cdef class TeamProgress(Loader): # Fixed
    id: int = 117
    compress_packet: bool = False
    cdef public:
        int team_id
        int numerator, denominator
        float percent
        int icon_id
        int show_as_percent, show_particle, show_previous, visible

        
    cpdef read(self, ByteReader reader):
        self.team_id = reader.read_byte()
        
        # Read flags byte with display options
        cdef unsigned char flags = reader.read_byte()
        self.visible = (flags & 0x01) > 0
        self.show_particle = (flags & 0x02) > 0
        self.show_previous = (flags & 0x04) > 0
        self.show_as_percent = (flags & 0x08) > 0
        
        # Read data according to flags
        if self.show_as_percent:
            self.percent = fromfixed(reader.read_short())
            self.numerator = 0
            self.denominator = 0
        else:
            self.numerator = reader.read_int()
            self.denominator = reader.read_int()
            self.percent = 0.0
            
        self.icon_id = reader.read_byte()
            
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.team_id)
        
        # Compose flags byte
        cdef unsigned char flags = 0
        if self.visible:
            flags |= 0x01
        if self.show_particle:
            flags |= 0x02
        if self.show_previous:
            flags |= 0x04
        if self.show_as_percent:
            flags |= 0x08
            
        writer.write_byte(flags)
        
        # Write data according to flags
        if self.show_as_percent:
            writer.write_short(tofixed(self.percent))
        else:
            writer.write_int(self.numerator)
            writer.write_int(self.denominator)
            
        writer.write_byte(self.icon_id)

cdef class TerritoryBaseState:
    pass

cdef class TimeScale(Loader): # Fixed
    id: int = 75
    compress_packet: bool = False
    cdef public:
        float scale

    cpdef read(self, ByteReader reader):
        self.scale = fromfixed(reader.read_short())

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_short(tofixed(self.scale))

cdef class UGCBatchEntity: # Fixed?
    cdef public:
        int mode, ugc_item_id, x, y, z
cdef class UGCMapInfo(Loader): # Fixed
    id: int = 102
    compress_packet: bool = False
    cdef public:
        bytes png_data

    cpdef read(self, ByteReader reader):
        cdef int length = reader.read_int()
        self.png_data = reader.read(length) # TODO: check if this is correct Bytes...

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_int(len(self.png_data))
        writer.write_bytes(self.png_data)

cdef class UGCMapLoadingFromHost(Loader): # Fixed
    id: int = 101
    compress_packet: bool = False
    cdef public:
        int percent_complete
    cpdef read(self, ByteReader reader):
        self.percent_complete = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.percent_complete)

cdef class UGCMessage(Loader): # Fixed
    id: int = 100
    compress_packet: bool = False
    cdef public:
        int message_id
    cpdef read(self, ByteReader reader):
        self.message_id = reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.message_id)

cdef class UGCObjectives(Loader): # Fixed
    id: int = 68
    compress_packet: bool = False
    cdef public:
        int mode, noOfObjectives
        list objective_ids, objective_values
        
    cpdef read(self, ByteReader reader):
        self.mode = reader.read_byte()
        self.noOfObjectives = reader.read_int()
        
        self.objective_ids = []
        self.objective_values = []
        
        for i in range(self.noOfObjectives):
            self.objective_ids.append(reader.read_string())
            self.objective_values.append(reader.read_int())
            
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.mode)
        writer.write_int(self.noOfObjectives)
        
        for i in range(self.noOfObjectives):
            writer.write_string(self.objective_ids[i])
            writer.write_int(self.objective_values[i])

cdef class UseCommand(Loader): # Fixed
    id: int = 86
    compress_packet: bool = False
    cpdef read(self, ByteReader reader):
        pass

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)

cdef class UseOrientedItem:
    pass

cdef class VoiceData(Loader): # Fixed
    id: int = 103
    compress_packet: bool = False
    cdef public:
        int player_id
        int data_size
        str data
        
    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.data_size = reader.read_short()
        
        # Read the voice data as a string
        # Since voice data is binary, we manually read the bytes
        self.data = reader.read(self.data_size).decode('utf-8', 'replace')
        
    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_short(self.data_size)
        writer.write(self.data.encode('utf-8'))

cdef class WeaponReload(Loader): # Fixed
    id: int = 76
    compress_packet: bool = False
    cdef public:
        int player_id, tool_id
        bint is_done

    cpdef read(self, ByteReader reader):
        self.player_id = reader.read_byte()
        self.tool_id = reader.read_byte()
        self.is_done = <bint>reader.read_byte()

    cpdef write(self, ByteWriter writer):
        writer.write_byte(self.id)
        writer.write_byte(self.player_id)
        writer.write_byte(self.tool_id)
        writer.write_byte(<bint>self.is_done)

cdef class WorldUpdate:
    pass

# Alias for compatibility
item = AddServer
