# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
"""
VXL Module - Ace of Spades Voxel Library
Cython implementation for binary compatibility

Classes:
    - CChunk: Chunk class representing a portion of the map
    - VXL: Main VXL map class for voxel map manipulation
    - Enum: Enumeration helper class
    - array: Array buffer class with memview property
    - memoryview: Memory view class

Module-level functions:
    - A2, add_ground_color, clamp, create_shadow_vbo, delete_shadow_vbo
    - generate_ground_color_table, get_color_tuple, reset_ground_colors
    - sphere_in_frustum, parse_constant_overrides
"""

# ============================================================================
# Module-level state
# ============================================================================
cdef list _ground_colors = []
cdef int _max_modifiable_z = 238

# ============================================================================
# Module-level Functions
# ============================================================================

cpdef object A2(object arg):
    """Utility function A2"""
    return arg

cpdef object add_ground_color(int r, int g, int b, int a=255):
    """Add a ground color to the color table"""
    global _ground_colors
    _ground_colors.append((r, g, b, a))
    return None

cpdef object clamp(object value, object min_val=0, object max_val=1):
    """Clamp a value between min and max"""
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value

cpdef object create_shadow_vbo():
    """Create the shadow vertex buffer object"""
    return None

cpdef object delete_shadow_vbo():
    """Delete the shadow vertex buffer object"""
    return None

cpdef object generate_ground_color_table():
    """Generate the ground color lookup table"""
    return None

cpdef tuple get_color_tuple(unsigned int color, int include_alpha=0):
    """Convert an integer color to RGBA tuple
    
    The original VXL format stores colors as 0xAARRGGBB where:
    - AA: Alpha (7-bit, stored as 0-127, converted to 0-253)
    - RR: Red (0-255)
    - GG: Green (0-255)  
    - BB: Blue (0-255)
    
    Alpha conversion: if alpha_byte > 0, alpha = alpha_byte * 2 - 1
    """
    cdef int b = color & 0xFF
    cdef int g = (color >> 8) & 0xFF
    cdef int r = (color >> 16) & 0xFF
    cdef int alpha_byte = (color >> 24) & 0xFF
    cdef int a
    
    if alpha_byte == 0:
        a = 0
    else:
        a = alpha_byte * 2 - 1
    
    return (r, g, b, a)

cpdef object reset_ground_colors():
    """Reset the ground color table"""
    global _ground_colors
    _ground_colors = []
    return None

cpdef bint sphere_in_frustum(float x, float y, float z, float radius):
    """Test if a sphere is within the view frustum
    
    Returns True by default (everything in frustum when not rendering)
    """
    return True

cpdef object parse_constant_overrides(object arg):
    """Parse constant overrides from configuration"""
    return arg


# ============================================================================
# CChunk Class
# ============================================================================

cdef class CChunk:
    """Chunk class representing a portion of the voxel map"""
    
    cdef public int _x1, _y1, _z1
    cdef public int _x2, _y2, _z2
    
    def __init__(self):
        self._x1 = 0
        self._y1 = 0
        self._z1 = 0
        self._x2 = 0
        self._y2 = 0
        self._z2 = 0
    
    @property
    def x1(self):
        return self._x1
    
    @property
    def y1(self):
        return self._y1
    
    @property
    def z1(self):
        return self._z1
    
    @property
    def x2(self):
        return self._x2
    
    @property
    def y2(self):
        return self._y2
    
    @property
    def z2(self):
        return self._z2
    
    cpdef void delete(self):
        pass
    
    cpdef void draw(self):
        pass
    
    cpdef list get_colors(self):
        return []
    
    cpdef list to_block_list(self):
        return []


# ============================================================================
# VXL Class
# ============================================================================

cdef class VXL:
    """Main VXL map class for voxel map manipulation"""
    
    cdef int _x_size, _y_size, _z_size
    cdef int _detail_level
    cdef dict _blocks
    cdef public object minimap_texture
    cdef public str name
    cdef bint _initialized
    
    def __init__(self, object arg1=None, object arg2=None, int data_size=0, int detail_level=2):
        self._x_size = 512
        self._y_size = 512
        self._z_size = 64
        self._detail_level = detail_level
        self._blocks = {}
        self.minimap_texture = None
        self.name = "Unknown"
        self._initialized = True

        if isinstance(arg1, (bytes, bytearray)):
            # VXLMap(data, metadata) usage
            if isinstance(arg2, dict):
                self.name = arg2.get("name", "Unknown")
            # TODO: Load map from data?

    
    def __repr__(self):
        return f"<VXL map {self._x_size}x{self._y_size}x{self._z_size}>"

    def width(self):
        return self._x_size

    def height(self):
        return self._y_size

    def depth(self):
        return self._z_size

    cpdef object get_random_pos(self, int x1, int y1, int x2, int y2):
        # Stub implementation to allow server start
        # Returns (x, y, z) tuple
        import random
        cdef int x = random.randint(x1, x2)
        cdef int y = random.randint(y1, y2)
        cdef int z = 0 # Surface?
        # TODO: Implement actual raycast/check for solid ground
        return (x, y, z)
    
    # Block manipulation
    cpdef object add_point(self, int x, int y, int z, tuple color_tuple):
        """Add a point to the map
        
        Args:
            x, y, z: Block coordinates
            color_tuple: (r, g, b, a) tuple
        """
        cdef int r, g, b, a, alpha_byte
        cdef unsigned int color
        
        if not isinstance(color_tuple, tuple) or len(color_tuple) != 4:
            raise TypeError("Argument 'color_tuple' has incorrect type (expected tuple, got %s)" % type(color_tuple).__name__)
        
        r, g, b, a = color_tuple
        alpha_byte = (a + 1) // 2 if a > 0 else 0
        color = (alpha_byte << 24) | (r << 16) | (g << 8) | b
        self._blocks[(x, y, z)] = color
        return None
    
    cpdef object set_point(self, int x, int y, int z, tuple color_tuple):
        """Set a point in the map (alias for add_point)"""
        return self.add_point(x, y, z, color_tuple)
    
    cpdef object remove_point(self, int x, int y, int z):
        """Remove a point from the map"""
        cdef tuple key = (x, y, z)
        if key in self._blocks:
            del self._blocks[key]
        return None
    
    cpdef object remove_point_nochecks(self, int x, int y, int z):
        return self.remove_point(x, y, z)
    
    cpdef object color_block(self, int x, int y, int z, unsigned int color=0xFFFFFF):
        cdef tuple key = (x, y, z)
        if key in self._blocks:
            self._blocks[key] = color
        return None
    
    cpdef object check_only(self, int x, int y, int z):
        return None
    
    cpdef void clear_checked_geometry(self):
        pass
    
    # Block queries
    cpdef bint get_solid(self, int x, int y, int z):
        return (x, y, z) in self._blocks
    
    cpdef object get_point(self, int x, int y, int z):
        cdef tuple key = (x, y, z)
        if key in self._blocks:
            return self._blocks[key]
        return None
    
    cpdef unsigned int get_color(self, int x, int y, int z):
        return self._blocks.get((x, y, z), 0)
    
    cpdef object get_color_tuple(self, int x, int y, int z):
        cdef unsigned int color = self.get_color(x, y, z)
        if color == 0:
            return None
        return get_color_tuple(color, 0)
    
    cpdef bint has_neighbors(self, int x, int y, int z, int min_neighbors=1, int check_water=0):
        return False
    
    cpdef int is_space_to_add_blocks(self, int count=1):
        return count
    
    # Static lighting
    cpdef void add_static_light(self, int x, int y, int z, int r, int g, int b, float intensity=1.0):
        pass
    
    cpdef void update_static_light_colour(self, int x, int y, int z, int r, int g, int b):
        pass
    
    cpdef void remove_static_light(self, int x, int y, int z):
        pass
    
    # Shadows
    cpdef void create_spot_shadows(self, object positions):
        pass
    
    cpdef void set_shadow_char_height(self, int height):
        pass
    
    cpdef void draw_spot_shadows(self):
        pass
    
    # Rendering
    cpdef void draw(self, int x, int y, int z, int draw_distance=0):
        pass
    
    cpdef void draw_sea(self):
        pass
    
    cpdef void post_load_draw_setup(self, int flags=0):
        pass
    
    cpdef object get_overview(self, int x=0, int y=0, int width=0, int height=0):
        return None
    
    # Prefabs
    cpdef bint get_prefab_touches_world(self, object kv6, int x, int y, int z, 
                                         int rx=0, int ry=0, int rz=0, int scale=1):
        return False
    
    cpdef void place_prefab_in_world(self, object kv6, int x, int y, int z,
                                      int rx=0, int ry=0, int rz=0, int scale=1,
                                      int flags=0, float tolerance=0.0):
        pass
    
    cpdef void erase_prefab_from_world(self, object kv6, int x, int y, int z,
                                        int rx=0, int ry=0, int rz=0, int scale=1,
                                        int flags=0, float tolerance=0.0):
        pass
    
    # Ground colors
    cpdef list get_ground_colors(self):
        return _ground_colors
    
    cpdef void refresh_ground_colors(self):
        pass
    
    # Z-limits
    cpdef void set_max_modifiable_z(self, int z):
        global _max_modifiable_z
        _max_modifiable_z = z
    
    cpdef int get_max_modifiable_z(self):
        return _max_modifiable_z
    
    # Threading
    cpdef bint done_processing(self):
        return False
    
    cpdef void change_thread_state(self, int mode, object data=None, int data_size=0):
        pass
    
    # Chunks
    cpdef list chunk_to_pointlist(self, object chunk):
        if isinstance(chunk, CChunk):
            return (<CChunk>chunk).to_block_list()
        return []
    
    # VXL serialization
    cpdef bytes generate_vxl(self, bint compress=True):
        """Generate VXL file data from current map
        
        VXL format: 512x512 columns, each column contains N spans + top air
        For an empty map, each column is 4 bytes: 00 F0 EF 00
        """
        cdef bytes empty_column = b'\x00\xF0\xEF\x00'
        cdef int num_columns = 512 * 512
        return empty_column * num_columns
    
    # Cleanup
    cpdef void destroy(self):
        self._blocks.clear()
        self._initialized = False
    
    cpdef void cleanup(self):
        pass


# ============================================================================
# Enum Class
# ============================================================================

cdef class Enum:
    """Enumeration helper class"""
    
    cdef public str name
    cdef public int value
    
    def __init__(self, str name, int value):
        self.name = name
        self.value = value
    
    def __repr__(self):
        return f"{self.name}({self.value})"
    
    def __str__(self):
        return self.name
    
    def __int__(self):
        return self.value
    
    def __eq__(self, other):
        if isinstance(other, Enum):
            return self.value == (<Enum>other).value
        return self.value == other
    
    def __hash__(self):
        return hash(self.value)


# ============================================================================
# Array Class
# ============================================================================

cdef class array:
    """Array buffer class with memview property"""
    
    cdef public tuple shape
    cdef public int itemsize
    cdef public str format
    cdef public str mode
    cdef public bint allocate_buffer
    cdef public object data
    
    def __init__(self, tuple shape, str typestr="f", int itemsize=4, 
                 str format="f", str mode="c", bint allocate_buffer=True):
        self.shape = shape
        self.itemsize = itemsize
        self.format = format
        self.mode = mode
        self.allocate_buffer = allocate_buffer
        self.data = None
        
        cdef int size, dimension
        if allocate_buffer:
            size = itemsize
            for dimension in shape:
                size *= dimension
            self.data = bytearray(size)
    
    @property
    def memview(self):
        return None
    
    def __len__(self):
        if len(self.shape) > 0:
            return self.shape[0]
        return 0


# ============================================================================
# Memoryview Class (custom, not builtin)
# ============================================================================

cdef class memoryview:
    """Memory view class for accessing raw memory buffers"""
    
    cdef public object obj
    cdef object _base
    cdef public bint dtype_is_object
    cdef tuple _shape
    cdef tuple _strides
    cdef int _itemsize
    cdef int _ndim
    
    def __init__(self, object obj, int flags=0, bint dtype_is_object=False):
        self.obj = obj
        self._base = obj
        self.dtype_is_object = dtype_is_object
        self._shape = ()
        self._strides = ()
        self._itemsize = 1
        self._ndim = 0
    
    def __len__(self):
        if len(self._shape) > 0:
            return self._shape[0]
        return 0
    
    def __repr__(self):
        return f"<memoryview object at {id(self):#x}>"
    
    @property
    def T(self):
        return self
    
    @property
    def base(self):
        return self._base
    
    @property
    def shape(self):
        return self._shape
    
    @property
    def strides(self):
        return self._strides
    
    @property
    def suboffsets(self):
        return ()
    
    @property
    def ndim(self):
        return self._ndim
    
    @property
    def itemsize(self):
        return self._itemsize
    
    @property
    def nbytes(self):
        cdef int total = self._itemsize
        cdef int dim
        for dim in self._shape:
            total *= dim
        return total
    
    @property
    def size(self):
        cdef int total = 1
        cdef int dim
        for dim in self._shape:
            total *= dim
        return total
    
    cpdef memoryview copy(self):
        return self
    
    cpdef memoryview copy_fortran(self):
        return self
    
    cpdef bint is_c_contig(self):
        return True
    
    cpdef bint is_f_contig(self):
        return False


# ============================================================================
# Map Sync Classes for Network Transmission (ported from ace.py)
# ============================================================================

import zlib
import struct

# Constants for map chunking
MAP_SEND_ROWS = 4
MAP_PACKET_SIZE = 1024

class MapSyncChunker:
    """Chunker that yields 1024-byte chunks of compressed map data"""
    def __init__(self, vxl_map):
        self.packer = MapPacker(vxl_map)
        self.crc32 = zlib.crc32(b"")
    
    def iter(self):
        s = b""
        for ins in self.packer.iter():
            self.crc32 = self.packer.crc32
            s += ins
            while len(s) >= MAP_PACKET_SIZE:
                yield s[:MAP_PACKET_SIZE]
                s = s[MAP_PACKET_SIZE:]
        if s:
            yield s

class MapPacker:
    """Packer that compresses map data using zlib"""
    def __init__(self, data):
        self.serializer = MapSerializer(data)
        self.crc32 = zlib.crc32(b"")
    
    def iter(self):
        # Use same zlib settings as original (level 6, 15 window bits)
        compressor = zlib.compressobj(
            level=6,
            method=zlib.DEFLATED,
            wbits=15,
            memLevel=8,
            strategy=zlib.Z_DEFAULT_STRATEGY
        )
        for s in self.serializer.iter():
            # Update CRC with raw serialized data BEFORE compression
            self.crc32 = zlib.crc32(s, self.crc32)
            compressed = compressor.compress(s)
            if compressed:
                yield compressed
        # Final flush must use Z_FINISH to match original
        final = compressor.flush(zlib.Z_FINISH)
        if final:
            yield final

class MapSerializer:
    """Serializer that reads raw column data from VXL map"""
    def __init__(self, data, delta_mode=True):
        self.data = data
        self.delta_mode = delta_mode
    
    def iter(self):
        for i in range(0, 512, MAP_SEND_ROWS):
            s = b""
            for j in range(MAP_SEND_ROWS):
                y = i + j
                if y >= 512: 
                    break
                row = self.data.columns[y]
                if self.delta_mode:
                    s += b"".join(
                        struct.pack("<II", x, y) + row[x]
                        for x in range(512)
                    )
            yield s


class VXLMapWrapper:
    """Wrapper class that adds column storage and chunker support to VXL"""
    def __init__(self, data=None, map_info=None):
        self._vxl = VXL(data, map_info)
        self.columns = [[b"" for _ in range(512)] for _ in range(512)]
        self.ready = False
        self.estimated_size = 0
        self.map_info = map_info or {}
        self._raw_data = None
        
        if data is not None:
            self.load_vxl(data)
    
    def load_vxl(self, data):
        """Load VXL data and parse columns for network transmission"""
        self._raw_data = bytes(data)
        self.estimated_size = len(data)
        
        # Parse the VXL format into columns
        pos = 0
        length = len(data)
        
        try:
            for y in range(512):
                for x in range(512):
                    if pos >= length:
                        self.columns[y][x] = b"\x00\x00\x00\x00"
                        continue
                    
                    col_data = bytearray()
                    
                    while True:
                        if pos + 4 > length:
                            break
                        
                        ns = data[pos:pos+4]
                        pos += 4
                        col_data += ns
                        
                        if ns[0] == 0:
                            # Final span - read colors
                            finals = ns[2] - ns[1] + 1
                            needed = 4 * finals
                            if pos + needed > length:
                                break
                            col_data += data[pos:pos+needed]
                            pos += needed
                            break
                        else:
                            # Additional span - read colors
                            block_size = (ns[0] - 1) * 4
                            if block_size < 0 or pos + block_size > length:
                                break
                            col_data += data[pos:pos+block_size]
                            pos += block_size
                    
                    self.columns[y][x] = bytes(col_data)
            
            self.ready = True
            return True
        except Exception as e:
            print(f"Map load error: {e}")
            self.ready = False
            return False
    
    def get_chunker(self):
        """Return a MapSyncChunker for network transmission"""
        return MapSyncChunker(self)
    
    # Delegate other methods to the underlying VXL
    @property
    def name(self):
        return self.map_info.get("name", "Unknown")
    
    def width(self):
        return self._vxl.width()
    
    def height(self):
        return self._vxl.height()
    
    def depth(self):
        return self._vxl.depth()
    
    def get_random_pos(self, x1, y1, x2, y2):
        return self._vxl.get_random_pos(x1, y1, x2, y2)
    
    def get_solid(self, x, y, z):
        return self._vxl.get_solid(x, y, z)
    
    def get_color(self, x, y, z):
        return self._vxl.get_color(x, y, z)
    
    def set_point(self, x, y, z, solid, color=0):
        return self._vxl.set_point(x, y, z, solid, color)
    
    def build_point(self, x, y, z, color):
        return self._vxl.build_point(x, y, z, color)
    
    def destroy_point(self, x, y, z):
        return self._vxl.destroy_point(x, y, z)


# Compatibility alias - use wrapper for full functionality
VXLMap = VXLMapWrapper

