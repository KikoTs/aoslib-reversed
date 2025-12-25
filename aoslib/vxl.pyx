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


from libc.math cimport sin, cos

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
    
    cpdef void delete_chunk(self):
        """Delete this chunk (renamed from 'delete' to avoid C++ keyword conflict)"""
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
    # Column storage for network transmission
    cdef public list columns
    cdef public bint ready
    cdef public int estimated_size
    cdef public dict map_info
    cdef bytes _raw_data
    
    def __init__(self, object arg1=None, object arg2=None, int data_size=0, int detail_level=2):
        self._x_size = 512
        self._y_size = 512
        self._z_size = 64
        self._detail_level = detail_level
        self._blocks = {}
        self.minimap_texture = None
        self.name = "Unknown"
        self._initialized = True
        
        # Initialize column storage (512x512 grid of byte columns)
        self.columns = [[b"" for _ in range(512)] for _ in range(512)]
        self.ready = False
        self.estimated_size = 0
        self.map_info = {}
        self._raw_data = b""

        if isinstance(arg1, (bytes, bytearray)):
            # VXL(data, metadata) usage
            if isinstance(arg2, dict):
                self.map_info = arg2
                self.name = arg2.get("name", "Unknown")
            # Load map data into columns
            self.load_vxl(arg1)

    
    def __repr__(self):
        return f"<VXL map {self._x_size}x{self._y_size}x{self._z_size}>"

    def width(self):
        return self._x_size

    def height(self):
        return self._y_size

    def depth(self):
        return self._z_size

    cpdef object get_random_pos(self, int x1, int y1, int x2, int y2):
        """Get a random valid spawn position within the given bounds.
        
        Uses direct random sampling within the bounding box to ensure
        unbiased distribution of spawn points.
        """
        import random
        
        cdef int attempts = 0
        cdef int max_attempts = 100
        cdef int rx, ry, rz
        cdef int temp_z
        
        # Ensure bounds are correct (min < max)
        cdef int min_x = min(x1, x2)
        cdef int max_x = max(x1, x2)
        cdef int min_y = min(y1, y2)
        cdef int max_y = max(y1, y2)
        
        # Clamp to map dimensions
        min_x = max(0, min_x)
        max_x = min(self._x_size - 1, max_x)
        min_y = max(0, min_y)
        max_y = min(self._y_size - 1, max_y)
        
        # Main loop: Try random positions
        while attempts < max_attempts:
            rx = random.randint(min_x, max_x)
            ry = random.randint(min_y, max_y)
            
            temp_z = self.get_z(rx, ry)
            
            # Validity check:
            # 1. Not too deep (z < MAP_Z - 2)
            # 2. Block is solid
            # 3. Not water
            # 4. Space above is clear
            if (temp_z < self._z_size - 2 and
                self.get_solid(rx, ry, temp_z) and
                not self.is_water(rx, ry, temp_z) and
                not self.get_solid(rx, ry, temp_z - 1) and
                not self.get_solid(rx, ry, temp_z - 2)):
                
                return (rx, ry, temp_z)
            
            attempts += 1
            
        # Fallback: Scan center of the requested area
        cdef int center_x = (min_x + max_x) // 2
        cdef int center_y = (min_y + max_y) // 2
        cdef int search_radius = 25
        cdef int sx, sy
        
        for sx in range(center_x - search_radius, center_x + search_radius):
            for sy in range(center_y - search_radius, center_y + search_radius):
                if sx < min_x or sx > max_x or sy < min_y or sy > max_y:
                    continue
                    
                temp_z = self.get_z(sx, sy)
                if (temp_z < self._z_size - 2 and 
                    self.get_solid(sx, sy, temp_z) and
                    not self.is_water(sx, sy, temp_z)):
                    return (sx, sy, temp_z)
                        
        # Final fallback: return center (risky but better than crash)
        return (center_x, center_y, self.get_z(center_x, center_y))

    cpdef bint is_water(self, int x, int y, int z):
        """Check if block is water based on color."""
        cdef unsigned int color = self._blocks.get((x, y, z), 0)
        if color == 0: return False
        
        # Extract RGB (Format is 0xAARRGGBB in our code)
        cdef int r = (color >> 16) & 0xFF
        cdef int g = (color >> 8) & 0xFF
        cdef int b = color & 0xFF
        
        # Water check from AceMap
        return (b > 180 and r < 100 and g < 150) or (b > r + g)
    
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
    
    cpdef bint build_point(self, int x, int y, int z, object color):
        """Build a block at the given position with the given color (int or tuple)."""
        cdef unsigned int color_int
        cdef int r, g, b
        
        if x < 0 or x >= self._x_size or y < 0 or y >= self._y_size or z < 0 or z >= self._z_size:
            return False
            
        if isinstance(color, tuple):
            if len(color) >= 3:
                r, g, b = color[0], color[1], color[2]
                color_int = (r << 16) | (g << 8) | b
            else:
                color_int = 0xFFFFFF
        elif isinstance(color, int):
            color_int = <unsigned int>color
        else:
            try:
                # Try to access rgb attribute if it exists (e.g. KV6 color object)
                if hasattr(color, 'rgb'):
                    color_val = color.rgb
                    if isinstance(color_val, tuple):
                        r, g, b = color_val[0], color_val[1], color_val[2]
                        color_int = (r << 16) | (g << 8) | b
                    else:
                        color_int = <unsigned int>color_val
                else:
                    color_int = 0xFFFFFF
            except:
                color_int = 0xFFFFFF
                
        self._blocks[(x, y, z)] = color_int
        return True
    
    cpdef bint destroy_point(self, int x, int y, int z):
        """Destroy (remove) a block at the given position."""
        cdef tuple key = (x, y, z)
        if key in self._blocks:
            del self._blocks[key]
            return True
        return False
    
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
    
    cpdef int get_z(self, int x, int y):
        cdef int z
        for z in range(self._z_size):
            if self.get_solid(x, y, z):
                return z
        return self._z_size - 1
    
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
    
    # Block line traversal (3D Bresenham-like algorithm from acemap)
    cpdef list block_line(self, int x1, int y1, int z1, int x2, int y2, int z2):
        """Return list of block positions along a line from (x1,y1,z1) to (x2,y2,z2).
        
        Based on acemap C++ block_line implementation.
        """
        cdef list result = []
        cdef int cx = x1, cy = y1, cz = z1
        cdef int dx = x2 - x1, dy = y2 - y1, dz = z2 - z1
        cdef int ixi, iyi, izi
        cdef long dxi, dyi, dzi, lx, ly, lz
        cdef int VSID = 512
        
        # Determine step direction
        ixi = 1 if dx >= 0 else -1
        iyi = 1 if dy >= 0 else -1
        izi = 1 if dz >= 0 else -1
        
        # Calculate increments based on dominant axis
        if abs(dx) >= abs(dy) and abs(dx) >= abs(dz):
            dxi = 1024
            lx = 512
            dyi = 0x3fffffff // VSID if dy == 0 else abs(dx * 1024 // dy)
            ly = dyi // 2
            dzi = 0x3fffffff // VSID if dz == 0 else abs(dx * 1024 // dz)
            lz = dzi // 2
        elif abs(dy) >= abs(dz):
            dyi = 1024
            ly = 512
            dxi = 0x3fffffff // VSID if dx == 0 else abs(dy * 1024 // dx)
            lx = dxi // 2
            dzi = 0x3fffffff // VSID if dz == 0 else abs(dy * 1024 // dz)
            lz = dzi // 2
        else:
            dzi = 1024
            lz = 512
            dxi = 0x3fffffff // VSID if dx == 0 else abs(dz * 1024 // dx)
            lx = dxi // 2
            dyi = 0x3fffffff // VSID if dy == 0 else abs(dz * 1024 // dy)
            ly = dyi // 2
        
        if ixi >= 0:
            lx = dxi - lx
        if iyi >= 0:
            ly = dyi - ly
        if izi >= 0:
            lz = dzi - lz
        
        while True:
            result.append((cx, cy, cz))
            
            if cx == x2 and cy == y2 and cz == z2:
                break
            
            if lz <= lx and lz <= ly:
                cz += izi
                if cz < 0 or cz >= self._z_size:
                    break
                lz += dzi
            elif lx < ly:
                cx += ixi
                if cx < 0 or cx >= VSID:
                    break
                lx += dxi
            else:
                cy += iyi
                if cy < 0 or cy >= VSID:
                    break
                ly += dyi
        
        return result
    
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
    
    # =========================================================================
    # Column storage and network transmission methods (integrated from wrapper)
    # =========================================================================
    
    cpdef bint load_vxl(self, object data):
        """Load VXL data using reference implementation approach.
        
        Follows Mari Kiri's original map.py logic:
        - Row-major order: for y in [0..511], for x in [0..511]
        - Read 4 bytes 'ns' header for each span:
          * if ns[0] == 0, read (ns[2] - ns[1] + 1)*4 color bytes and break
          * else read (ns[0]-1)*4 color bytes (no break)
        - Track lowest_point for older 0.x map format detection
        """
        if isinstance(data, bytearray):
            self._raw_data = bytes(data)
        else:
            self._raw_data = data
        self.estimated_size = len(data)
        
        # Declare all Cython variables at the top
        cdef int x, y
        cdef int pos = 0
        cdef bytes ns
        cdef int lowest_point = 63
        cdef int highest_point = 255
        cdef int cand_lowest
        cdef Py_ssize_t length = len(data)
        cdef int finals, needed, block_size
        
        try:
            # Go row-major: each row is y, each column is x
            for y in range(512):
                for x in range(512):
                    # If we've exhausted the file, store a 4-byte dummy column
                    if pos >= length:
                        self.columns[y][x] = b"\x00\x00\x00\x00"
                        continue

                    col_data = bytearray()

                    # Keep reading 4-byte blocks until we see ns[0] == 0
                    while True:
                        # If there's not even 4 bytes left, bail out
                        if pos + 4 > length:
                            break

                        ns = data[pos:pos+4]
                        pos += 4

                        # Track lowest_point for older map format detection
                        cand_lowest = max(ns[2], ns[1])
                        if cand_lowest > lowest_point:
                            lowest_point = cand_lowest
                        if ns[1] < highest_point:
                            highest_point = ns[1]

                        # Always append this 4-byte header to col_data
                        col_data += ns

                        if ns[0] == 0:
                            # If spans=0, read final color block => break
                            finals = ns[2] - ns[1] + 1
                            needed = 4 * finals
                            if pos + needed > length:
                                # Not enough data => partial read => break
                                break
                            col_data += data[pos:pos+needed]
                            pos += needed
                            break
                        else:
                            # If spans != 0, read (spans-1)*4 color bytes
                            block_size = (ns[0] - 1) * 4
                            if block_size < 0:
                                # Protect from negative
                                break
                            if pos + block_size > length:
                                break

                            col_data += data[pos:pos+block_size]
                            pos += block_size
                            # Then we loop again until ns[0] == 0

                    self.columns[y][x] = bytes(col_data)

            # After reading all columns, if lowest_point==63 => older 0.x map => shift up by 64
            # (Not implemented for now - most maps are 1.x format)
            
            print(f"VXL loaded: {self.estimated_size} bytes")
            self.ready = True
            return True

        except Exception as e:
            print(f"Map load error: {e}")
            import traceback
            traceback.print_exc()
            self.ready = False
            return False
    
    def get_chunker(self):
        """Return a MapSyncChunker for network transmission"""
        return MapSyncChunker(self)


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
        self.serializer = MapSerializer(data, delta_mode=True)
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
                else:
                    s += b"".join(row)
            yield s


# Compatibility alias - VXL now has all functionality built-in
VXLMap = VXL

