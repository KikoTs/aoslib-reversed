// VXL C Header - Ace of Spades Voxel Library
// Skeleton file for reverse engineering

#ifndef VXL_C_H
#define VXL_C_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// ============================================================================
// Constants
// ============================================================================
#define MAP_X_SIZE 512
#define MAP_Y_SIZE 512
#define MAP_Z_SIZE 64
#define CHUNK_SIZE 16

// ============================================================================
// Structs
// ============================================================================

// 3D Point structure
typedef struct {
    int x;
    int y;
    int z;
} Point;

// Block data structure
typedef struct {
    int color;
    bool solid;
} BlockData;

// Ground color entry
typedef struct {
    int r;
    int g;
    int b;
    int a;
} GroundColor;

// Static point light
typedef struct {
    int x;
    int y;
    int z;
    unsigned char r;
    unsigned char g;
    unsigned char b;
    float intensity;
} StaticPointLight;

// Block occlusion texture coordinates
typedef struct {
    float coords[6][4][2];  // 6 faces, 4 vertices, 2 coords (u,v)
} BlockOcclusionTexCoords;

// Quad structure (for rendering)
typedef struct {
    float vertices[4][3];   // 4 vertices, xyz
    float normals[4][3];    // 4 normals, xyz
    float texcoords[4][2];  // 4 tex coords, uv
    int color;
} Quad;

// Shadow quad
typedef struct {
    float vertices[4][3];
    float alpha;
} ShadowQuad;

// Falling blocks structure
typedef struct {
    Point* blocks;
    int* colors;
    int count;
    float x, y, z;
    float vx, vy, vz;
    float rx, ry, rz;
} FallingBlocks;

// Chunk VBO data
typedef struct {
    unsigned int vbo_id;
    unsigned int ibo_id;
    int vertex_count;
    int index_count;
    bool dirty;
} ChunkVBO;

// Chunk structure
typedef struct Chunk {
    int x1, y1, z1;
    int x2, y2, z2;
    ChunkVBO* vbo;
    bool dirty;
    bool visible;
    int block_count;
    // Static lighting data
    void* static_lights;  // map<int, StaticPointLight>*
} Chunk;

// MapData - Main map data structure
typedef struct MapData {
    int x_size;
    int y_size;
    int z_size;
    int detail_level;
    
    // Block data - 3D array [x][y][z]
    unsigned char* solid_data;      // Solid/air flags
    int* color_data;                // Block colors
    
    // Chunk data
    Chunk** chunks;
    int chunk_count_x;
    int chunk_count_y;
    
    // Sea/water data
    Chunk* sea_chunks;
    int sea_chunk_count;
    
    // Marker points found in map
    Point* spawn_points;
    int spawn_count;
    
    // Minimap texture
    unsigned int minimap_texture;
    
    // Threading
    void* update_thread;
    bool processing;
    
    // Static lighting
    void* static_point_lights;  // map<int, StaticPointLight>*
    
    // Ground colors
    GroundColor* ground_colors;
    int ground_color_count;
    
    // Max modifiable Z
    int max_modifiable_z;
    
    // Block counts
    int total_blocks;
} MapData;

// KV6 Data (for prefabs)
typedef struct KV6Data {
    int x_size;
    int y_size;
    int z_size;
    float pivot_x;
    float pivot_y;
    float pivot_z;
    int* voxels;
    int voxel_count;
} KV6Data;

// KV6 Display
typedef struct KV6Display {
    void* quads;
    int quad_count;
    unsigned int vbo_id;
} KV6Display;

// ============================================================================
// Vector Table Functions
// ============================================================================
void init_ind2vec(long index, float* x, float* y, float* z);
void initialize_vector_table(void);
float* index_to_vector(long index);

// ============================================================================
// Utility Functions
// ============================================================================
unsigned int CRC32(unsigned char* data, int length, unsigned int crc);
void encrypt(void* obj1, void* obj2);
void replace_all(void* str, char from, char to);
void replace_unsupported_slashes(void* str);
void initialize(void);

// ============================================================================
// KV6 Functions
// ============================================================================
void* load_kv6(char* path, int detail);
void scale_kv6(KV6Data* kv6, int scale);
void destroy_kv6(KV6Data* kv6);
void add_points(KV6Data* kv6, void* points, int count);
void save_kv6(KV6Data* kv6, char* path);
void set_default_color(float r, float g, float b);
void draw_display(KV6Display* display);
void* create_display(KV6Data* kv6, int detail, int flags, bool shadows);
void destroy_display(KV6Display* display);

// ============================================================================
// Frustum Functions
// ============================================================================
void extract_frustum(void);
bool sphere_in_frustum(float x, float y, float z, float radius);

// ============================================================================
// TGA/Texture Functions
// ============================================================================
void* read_tga_bits(const char* path, int* width, int* height, int* bpp, 
                    unsigned int* format, signed char* data);
unsigned int load_tga_texture(const char* path, unsigned int flags1, 
                               unsigned int flags2, unsigned int flags3);

// ============================================================================
// VXL Map Functions
// ============================================================================
int get_vxl_size(unsigned char* data, int length);
void initialise_floor(MapData* map, int z);
void* get_ground_colors_c(void);
void reset_ground_colors_c(void);
void add_ground_color_c(int r, int g, int b, int a);
void generate_ground_color_table_c(void);
int get_ground_color(int x, int y, int z);
void generate_static_light_color_table_c(int r, int g, int b, int a);
void set_max_modifiable_z(int z);
int get_max_modifiable_z(void);

// ============================================================================
// Rotation Functions
// ============================================================================
Point rotate_z_axis(Point p, int angle);
Point rotate_x_axis(Point p, int angle);
Point rotate_y_axis(Point p, int angle);

// ============================================================================
// Prefab Functions
// ============================================================================
bool get_prefab_touches_world(MapData* map, KV6Data* kv6, 
                               int x, int y, int z,
                               int rx, int ry, int rz, int scale);
void place_prefab_in_world(MapData* map, KV6Data* kv6,
                           int x, int y, int z,
                           int rx, int ry, int rz, int scale,
                           int flags, float tolerance);
void erase_prefab_from_world(MapData* map, KV6Data* kv6,
                              int x, int y, int z,
                              int rx, int ry, int rz, int scale,
                              int flags, float tolerance);

// ============================================================================
// VXL Save/Load Functions
// ============================================================================
void* create_temp(void);
void* save_vxl(MapData* map);
MapData* create_blank_map_data(int size);
void load_vxl(MapData* map, unsigned char* data, int length);
void load_part_vxl(MapData* map, unsigned char* data, int length);
void delete_map(MapData* map);

// ============================================================================
// Map Initialization Functions
// ============================================================================
void MapData_initialize(MapData* map);
void initialise_chunk_data(MapData* map);
void initialise_sea_chunk_data(MapData* map);
void find_marker_points(MapData* map);
void post_load_map_setup(MapData* map);
void update_shadows(MapData* map);
void compute_static_occlusion(MapData* map);

// ============================================================================
// Block Manipulation Functions
// ============================================================================
bool set_point(int x, int y, int z, MapData* map, bool value, int color);
bool remove_point(int x, int y, int z, MapData* map);
void color_block(int x, int y, int z, MapData* map);
bool check_only(int x, int y, int z, MapData* map);
void add_leader(int x, int y, int z, MapData* map, int team, bool flag);
void add_marked_to_known_safe(void);
void check_node(int x, int y, int z, MapData* map, FallingBlocks* fb);
void update_shadow(MapData* map, int x, int y, int z, bool flag);

// ============================================================================
// Static Lighting Functions
// ============================================================================
void add_static_point_light(MapData* map, int x, int y, int z,
                            unsigned char r, unsigned char g, unsigned char b,
                            float intensity);
void update_static_point_light_colour(MapData* map, int x, int y, int z,
                                       unsigned char r, unsigned char g, 
                                       unsigned char b);
void remove_static_point_light(MapData* map, int x, int y, int z);

// ============================================================================
// Shadow Functions
// ============================================================================
void create_shadow_vbo(void);
void set_shadow_char_height(int height);
void delete_shadow_vbo(void);
void find_lowest_block(int x, int y, int z1, int* out_z, int* out_color, MapData* map);
void create_shadows_from_positions(MapData* map, void* positions, int count);
void draw_shadows(void);

// ============================================================================
// Chunk Functions
// ============================================================================
int count_blocks_in_chunk(const MapData* map, unsigned int chunk_id);
int delta_chunk_count_with_block_change(const MapData* map, 
                                         unsigned int x, unsigned int y, 
                                         unsigned int z, bool adding);
void Chunk_initialize(Chunk* chunk);
void MapData_refresh_block_and_chunk_counts(MapData* map);
void update_chunk_data(Chunk* chunk, MapData* map, bool full);
void update_chunks_near_player(MapData* map);
void refresh_ground_colors_c_map(MapData* map);

// ============================================================================
// OpenGL/Rendering Functions
// ============================================================================
void PrintGLErrors(const char* location);
void delete_gl_texture(unsigned int* texture);
void load_ao_texture(int size);
void reload_ao_texture(int size);
void delete_gl_vbo(MapData* map);
void cleanup_gl(MapData* map);
void post_load_draw_setup(MapData* map, int flags);
void draw_vbo(Chunk* chunk, bool shadows, bool transparent);
void draw_position(MapData* map, int x, int y, int z, int flags);
void update_vbo(Chunk* chunk, MapData* map);
void draw_seascape_single_pass(MapData* map);
void update_vbo_sea(Chunk* chunk, MapData* map);
void create_sea_data(MapData* map);
void draw_display_map(MapData* map, int x, int y, int z, int flags);
void draw_sea(MapData* map);

// ============================================================================
// Occlusion Functions
// ============================================================================
int sunblock(MapData* map, int x, int y, int z);
void compute_block_occlusion_texcoords(bool* faces, BlockOcclusionTexCoords* out);
void compute_block_occlusion(BlockOcclusionTexCoords* out, int x, int y, int z, MapData* map);
void do_edge_highlight(BlockOcclusionTexCoords* out, int x, int y, int z, MapData* map);
void compute_dynamic_occlusion(MapData* map, int x, int y, int z);
void print_occlusion_data(MapData* map);

// ============================================================================
// Utility
// ============================================================================
int color_noise(int color);
void print_chunk_sizes(MapData* map);
void set_vert_text_coords(unsigned char u, unsigned char v, Quad* quad);
void make_sorted_offsets(void);
int compare_offsets(const void* a, const void* b);

// ============================================================================
// Threading
// ============================================================================
void run_thread(MapData* map, int mode, unsigned char* data, int length);
void change_thread(MapData* map, int mode, unsigned char* data, int length);
void close_thread(MapData* map);
bool done_processing(MapData* map);

// ============================================================================
// VXL Module Initialization (Cython)
// ============================================================================
void _initvxl(void);

#ifdef __cplusplus
}
#endif

#endif // VXL_C_H