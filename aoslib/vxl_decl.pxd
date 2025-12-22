# VXL Cython Declaration File
# Declares external C structures and functions from vxl_c.h

from libc.stdint cimport uint8_t, uint32_t
from libcpp cimport bool

cdef extern from "vxl_c.h":
    # Constants
    int MAP_X_SIZE
    int MAP_Y_SIZE
    int MAP_Z_SIZE
    int CHUNK_SIZE

    # Point structure
    ctypedef struct Point:
        int x
        int y
        int z

    # BlockData structure
    ctypedef struct BlockData:
        int color
        bool solid

    # GroundColor structure
    ctypedef struct GroundColor:
        int r
        int g
        int b
        int a

    # StaticPointLight structure
    ctypedef struct StaticPointLight:
        int x
        int y
        int z
        unsigned char r
        unsigned char g
        unsigned char b
        float intensity

    # ChunkVBO structure
    ctypedef struct ChunkVBO:
        unsigned int vbo_id
        unsigned int ibo_id
        int vertex_count
        int index_count
        bool dirty

    # Chunk structure
    ctypedef struct Chunk:
        int x1, y1, z1
        int x2, y2, z2
        ChunkVBO* vbo
        bool dirty
        bool visible
        int block_count
        void* static_lights

    # MapData structure
    ctypedef struct MapData:
        int x_size
        int y_size
        int z_size
        int detail_level
        unsigned char* solid_data
        int* color_data
        Chunk** chunks
        int chunk_count_x
        int chunk_count_y
        Chunk* sea_chunks
        int sea_chunk_count
        Point* spawn_points
        int spawn_count
        unsigned int minimap_texture
        void* update_thread
        bool processing
        void* static_point_lights
        GroundColor* ground_colors
        int ground_color_count
        int max_modifiable_z
        int total_blocks

    # KV6Data structure
    ctypedef struct KV6Data:
        int x_size
        int y_size
        int z_size
        float pivot_x
        float pivot_y
        float pivot_z
        int* voxels
        int voxel_count

    # FallingBlocks structure
    ctypedef struct FallingBlocks:
        Point* blocks
        int* colors
        int count
        float x, y, z
        float vx, vy, vz
        float rx, ry, rz

    # Function declarations
    void initialize()
    void initialize_vector_table()
    float* index_to_vector(long index)
    void init_ind2vec(long index, float* x, float* y, float* z)

    unsigned int CRC32(unsigned char* data, int length, unsigned int crc)

    void* get_ground_colors_c()
    void reset_ground_colors_c()
    void add_ground_color_c(int r, int g, int b, int a)
    void generate_ground_color_table_c()
    int get_ground_color(int x, int y, int z)
    void set_max_modifiable_z(int z)
    int get_max_modifiable_z()

    void extract_frustum()
    bool sphere_in_frustum(float x, float y, float z, float radius)

    MapData* create_blank_map_data(int size)
    void MapData_initialize(MapData* map)
    void load_vxl(MapData* map, unsigned char* data, int length)
    void load_part_vxl(MapData* map, unsigned char* data, int length)
    void* save_vxl(MapData* map)
    void delete_map(MapData* map)

    void initialise_chunk_data(MapData* map)
    void initialise_sea_chunk_data(MapData* map)
    void Chunk_initialize(Chunk* chunk)
    void update_chunk_data(Chunk* chunk, MapData* map, bool full)

    bool set_point(int x, int y, int z, MapData* map, bool value, int color)
    bool remove_point(int x, int y, int z, MapData* map)
    void color_block(int x, int y, int z, MapData* map)
    bool check_only(int x, int y, int z, MapData* map)
    void check_node(int x, int y, int z, MapData* map, FallingBlocks* fb)

    void add_static_point_light(MapData* map, int x, int y, int z,
                                unsigned char r, unsigned char g, unsigned char b,
                                float intensity)
    void update_static_point_light_colour(MapData* map, int x, int y, int z,
                                           unsigned char r, unsigned char g, unsigned char b)
    void remove_static_point_light(MapData* map, int x, int y, int z)

    void create_shadow_vbo()
    void set_shadow_char_height(int height)
    void delete_shadow_vbo()
    void create_shadows_from_positions(MapData* map, void* positions, int count)
    void draw_shadows()

    bool get_prefab_touches_world(MapData* map, KV6Data* kv6,
                                   int x, int y, int z,
                                   int rx, int ry, int rz, int scale)
    void place_prefab_in_world(MapData* map, KV6Data* kv6,
                               int x, int y, int z,
                               int rx, int ry, int rz, int scale,
                               int flags, float tolerance)
    void erase_prefab_from_world(MapData* map, KV6Data* kv6,
                                  int x, int y, int z,
                                  int rx, int ry, int rz, int scale,
                                  int flags, float tolerance)

    void post_load_draw_setup(MapData* map, int flags)
    void draw_vbo(Chunk* chunk, bool shadows, bool transparent)
    void draw_display_map(MapData* map, int x, int y, int z, int flags)
    void draw_sea(MapData* map)
    void cleanup_gl(MapData* map)

    void run_thread(MapData* map, int mode, unsigned char* data, int length)
    void change_thread(MapData* map, int mode, unsigned char* data, int length)
    void close_thread(MapData* map)
    bool done_processing(MapData* map)

    void find_marker_points(MapData* map)
    void post_load_map_setup(MapData* map)
    void update_shadows(MapData* map)
    void refresh_ground_colors_c_map(MapData* map)


# Note: Class implementations (CChunk, VXL, Enum, array, memoryview) 
# are defined directly in vxl.pyx, not declared here