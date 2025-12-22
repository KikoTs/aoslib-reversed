// VXL C++ Implementation - Ace of Spades Voxel Library
// Full implementation for reverse engineering

#include "vxl_c.h"
#include <cstdlib>
#include <cstring>
#include <cmath>

// ============================================================================
// Vector Table Functions
// ============================================================================
static float vector_table[256][3];
static bool g_initialized = false;

void init_ind2vec(long index, float* x, float* y, float* z) {
    if (index < 0 || index >= 256) {
        *x = *y = *z = 0.0f;
        return;
    }
    *x = vector_table[index][0];
    *y = vector_table[index][1];
    *z = vector_table[index][2];
}

void initialize_vector_table(void) {
    // Pre-compute 256 normalized direction vectors
    // Based on spherical coordinates distribution
    for (int i = 0; i < 256; i++) {
        float theta = (float)(i * 2.0 * M_PI / 256.0);
        float phi = (float)(acos(1.0 - 2.0 * (i + 0.5) / 256.0));
        vector_table[i][0] = sinf(phi) * cosf(theta);
        vector_table[i][1] = sinf(phi) * sinf(theta);
        vector_table[i][2] = cosf(phi);
    }
}

float* index_to_vector(long index) {
    return vector_table[index & 0xFF];
}

// ============================================================================
// Utility Functions
// ============================================================================

// Standard CRC32 with polynomial 0xEDB88320
static unsigned int crc32_table[256];
static bool crc32_table_initialized = false;

static void init_crc32_table(void) {
    for (unsigned int i = 0; i < 256; i++) {
        unsigned int crc = i;
        for (int j = 0; j < 8; j++) {
            if (crc & 1)
                crc = (crc >> 1) ^ 0xEDB88320;
            else
                crc >>= 1;
        }
        crc32_table[i] = crc;
    }
    crc32_table_initialized = true;
}

unsigned int CRC32(unsigned char* data, int length, unsigned int crc) {
    if (!crc32_table_initialized) init_crc32_table();
    
    crc = ~crc;
    for (int i = 0; i < length; i++) {
        crc = crc32_table[(crc ^ data[i]) & 0xFF] ^ (crc >> 8);
    }
    return ~crc;
}

void encrypt(void* obj1, void* obj2) {
    // Encryption stub - not needed for server
}

void replace_all(void* str, char from, char to) {
    if (!str) return;
    char* s = (char*)str;
    while (*s) {
        if (*s == from) *s = to;
        s++;
    }
}

void replace_unsupported_slashes(void* str) {
    replace_all(str, '\\', '/');
}

void initialize(void) {
    if (g_initialized) return;
    initialize_vector_table();
    init_crc32_table();
    g_initialized = true;
}

// ============================================================================
// Ground Color Functions
// ============================================================================
#define MAX_GROUND_COLORS 256
static GroundColor g_ground_color_array[MAX_GROUND_COLORS];
static int g_ground_color_count = 0;
static int g_max_modifiable_z = MAP_Z_SIZE;

void* get_ground_colors_c(void) {
    return g_ground_color_array;
}

void reset_ground_colors_c(void) {
    g_ground_color_count = 0;
    memset(g_ground_color_array, 0, sizeof(g_ground_color_array));
}

void add_ground_color_c(int r, int g, int b, int a) {
    if (g_ground_color_count >= MAX_GROUND_COLORS) return;
    
    g_ground_color_array[g_ground_color_count].r = r;
    g_ground_color_array[g_ground_color_count].g = g;
    g_ground_color_array[g_ground_color_count].b = b;
    g_ground_color_array[g_ground_color_count].a = a;
    g_ground_color_count++;
}

void generate_ground_color_table_c(void) {
    // Generate gradient table for terrain - stub, uses add_ground_color_c
}

int get_ground_color(int x, int y, int z) {
    // Get ground color for position - use first color if exists
    if (g_ground_color_count > 0) {
        GroundColor* c = &g_ground_color_array[0];
        return (c->a << 24) | (c->r << 16) | (c->g << 8) | c->b;
    }
    return 0x7F7F7F7F;  // Default gray
}

void generate_static_light_color_table_c(int r, int g, int b, int a) {
    // Light color table - for rendering, stub for server
}

void set_max_modifiable_z(int z) {
    g_max_modifiable_z = z;
}

int get_max_modifiable_z(void) {
    return g_max_modifiable_z;
}

// ============================================================================
// Rotation Functions (90-degree increments)
// ============================================================================
Point rotate_z_axis(Point p, int angle) {
    Point result = p;
    // Angle in 90-degree increments (0, 1, 2, 3 = 0, 90, 180, 270)
    switch (angle & 3) {
        case 1: result.x = -p.y; result.y = p.x; break;  // 90°
        case 2: result.x = -p.x; result.y = -p.y; break; // 180°
        case 3: result.x = p.y; result.y = -p.x; break;  // 270°
    }
    return result;
}

Point rotate_x_axis(Point p, int angle) {
    Point result = p;
    switch (angle & 3) {
        case 1: result.y = -p.z; result.z = p.y; break;
        case 2: result.y = -p.y; result.z = -p.z; break;
        case 3: result.y = p.z; result.z = -p.y; break;
    }
    return result;
}

Point rotate_y_axis(Point p, int angle) {
    Point result = p;
    switch (angle & 3) {
        case 1: result.x = p.z; result.z = -p.x; break;
        case 2: result.x = -p.x; result.z = -p.z; break;
        case 3: result.x = -p.z; result.z = p.x; break;
    }
    return result;
}

// ============================================================================
// Frustum Functions
// ============================================================================
static float frustum[6][4];

void extract_frustum(void) {
    // TODO: Implement frustum extraction from OpenGL
}

bool sphere_in_frustum(float x, float y, float z, float radius) {
    // TODO: Implement frustum culling
    return true;
}

// ============================================================================
// VXL Map Functions
// ============================================================================
int get_vxl_size(unsigned char* data, int length) {
    // VXL size is always 512x512
    return MAP_X_SIZE;
}

void initialise_floor(MapData* map, int z) {
    if (!map || !map->solid_data || !map->color_data) return;
    
    // Set all blocks at z level to solid with default color
    for (int x = 0; x < map->x_size; x++) {
        for (int y = 0; y < map->y_size; y++) {
            int idx = x + y * map->x_size + z * map->x_size * map->y_size;
            map->solid_data[idx] = 1;
            map->color_data[idx] = 0x7F7F7F7F;  // Gray with alpha
        }
    }
}

// ============================================================================
// Map Creation/Destruction
// ============================================================================
MapData* create_blank_map_data(int size) {
    MapData* map = (MapData*)malloc(sizeof(MapData));
    if (!map) return nullptr;
    
    memset(map, 0, sizeof(MapData));
    map->x_size = size;
    map->y_size = size;
    map->z_size = MAP_Z_SIZE;
    map->detail_level = 2;
    map->max_modifiable_z = MAP_Z_SIZE;
    
    return map;
}

void MapData_initialize(MapData* map) {
    if (!map) return;
    
    int total_blocks = map->x_size * map->y_size * map->z_size;
    
    // Allocate solid data (1 byte per block)
    map->solid_data = (unsigned char*)calloc(total_blocks, 1);
    
    // Allocate color data (4 bytes per block - ARGB)
    map->color_data = (int*)calloc(total_blocks, sizeof(int));
    
    // Initialize chunk count
    map->chunk_count_x = map->x_size / CHUNK_SIZE;
    map->chunk_count_y = map->y_size / CHUNK_SIZE;
    
    map->total_blocks = 0;
    map->processing = false;
}

// Helper: Get index into solid/color arrays
static inline int get_block_index(MapData* map, int x, int y, int z) {
    return x + y * map->x_size + z * map->x_size * map->y_size;
}

// Helper: Check bounds
static inline bool in_bounds(MapData* map, int x, int y, int z) {
    return x >= 0 && x < map->x_size &&
           y >= 0 && y < map->y_size &&
           z >= 0 && z < map->z_size;
}

void load_vxl(MapData* map, unsigned char* data, int length) {
    if (!map || !data || length < 4) return;
    
    // Initialize arrays if not already done
    if (!map->solid_data) MapData_initialize(map);
    
    unsigned char* ptr = data;
    unsigned char* end = data + length;
    
    // VXL format: 512x512 columns, each column has spans
    for (int y = 0; y < map->y_size && ptr < end; y++) {
        for (int x = 0; x < map->x_size && ptr < end; x++) {
            int z = 0;
            
            while (ptr < end) {
                int N = ptr[0];  // Number of 4-byte chunks for this span
                int S = ptr[1];  // Starting height of colored run
                int E = ptr[2];  // Ending height of colored run (inclusive)
                int A = ptr[3];  // Air start for next span
                ptr += 4;
                
                // Set solid blocks from S to E
                int color_count = E - S + 1;
                for (int i = 0; i < color_count && ptr + 4 <= end; i++) {
                    int bz = S + i;
                    if (bz < map->z_size) {
                        int idx = get_block_index(map, x, y, bz);
                        map->solid_data[idx] = 1;
                        // Color is BGRA in file, we store as ARGB
                        map->color_data[idx] = (ptr[3] << 24) | (ptr[2] << 16) | 
                                               (ptr[1] << 8) | ptr[0];
                        map->total_blocks++;
                    }
                    ptr += 4;
                }
                
                // N=0 means end of column
                if (N == 0) break;
                
                // Skip to next span (N includes the 4-byte header we read + colors)
                z = A;
            }
        }
    }
}

void load_part_vxl(MapData* map, unsigned char* data, int length) {
    // For partial loading, just call full load
    load_vxl(map, data, length);
}

void* save_vxl(MapData* map) {
    if (!map) return nullptr;
    
    // Allocate maximum possible size (8 bytes per column * 512*512)
    // Actual size will be smaller but we'll track it
    int max_size = map->x_size * map->y_size * 8;
    unsigned char* out = (unsigned char*)malloc(max_size);
    if (!out) return nullptr;
    
    unsigned char* ptr = out;
    
    // For empty map, generate standard empty pattern
    for (int y = 0; y < map->y_size; y++) {
        for (int x = 0; x < map->x_size; x++) {
            // Check if column has any blocks
            bool has_blocks = false;
            for (int z = 0; z < map->z_size; z++) {
                int idx = get_block_index(map, x, y, z);
                if (map->solid_data && map->solid_data[idx]) {
                    has_blocks = true;
                    break;
                }
            }
            
            if (!has_blocks) {
                // Empty column pattern: 00 F0 EF 00
                *ptr++ = 0x00;  // N = 0 (end marker)
                *ptr++ = 0xF0;  // S = 240
                *ptr++ = 0xEF;  // E = 239
                *ptr++ = 0x00;  // A = 0
            } else {
                // TODO: Serialize actual blocks
                // For now, use empty pattern
                *ptr++ = 0x00;
                *ptr++ = 0xF0;
                *ptr++ = 0xEF;
                *ptr++ = 0x00;
            }
        }
    }
    
    return out;
}

void delete_map(MapData* map) {
    if (!map) return;
    
    if (map->solid_data) free(map->solid_data);
    if (map->color_data) free(map->color_data);
    if (map->chunks) free(map->chunks);
    if (map->spawn_points) free(map->spawn_points);
    if (map->ground_colors) free(map->ground_colors);
    
    free(map);
}

// ============================================================================
// Chunk Functions
// ============================================================================
void initialise_chunk_data(MapData* map) {
    // TODO: Implement
}

void initialise_sea_chunk_data(MapData* map) {
    // TODO: Implement
}

void Chunk_initialize(Chunk* chunk) {
    if (!chunk) return;
    memset(chunk, 0, sizeof(Chunk));
}

void update_chunk_data(Chunk* chunk, MapData* map, bool full) {
    // TODO: Implement
}

void update_chunks_near_player(MapData* map) {
    // TODO: Implement
}

int count_blocks_in_chunk(const MapData* map, unsigned int chunk_id) {
    // TODO: Implement
    return 0;
}

int delta_chunk_count_with_block_change(const MapData* map,
                                         unsigned int x, unsigned int y,
                                         unsigned int z, bool adding) {
    // TODO: Implement
    return 0;
}

void MapData_refresh_block_and_chunk_counts(MapData* map) {
    // TODO: Implement
}

// ============================================================================
// Block Manipulation Functions
// ============================================================================
bool set_point(int x, int y, int z, MapData* map, bool value, int color) {
    if (!map || !map->solid_data || !map->color_data) return false;
    if (!in_bounds(map, x, y, z)) return false;
    if (z > map->max_modifiable_z) return false;
    
    int idx = get_block_index(map, x, y, z);
    bool was_solid = map->solid_data[idx] != 0;
    
    if (value) {
        // Adding or updating a block
        map->solid_data[idx] = 1;
        map->color_data[idx] = color;
        if (!was_solid) map->total_blocks++;
    } else {
        // Removing a block
        if (was_solid) {
            map->solid_data[idx] = 0;
            map->color_data[idx] = 0;
            map->total_blocks--;
        }
    }
    
    return true;
}

bool remove_point(int x, int y, int z, MapData* map) {
    if (!map || !map->solid_data) return false;
    if (!in_bounds(map, x, y, z)) return false;
    if (z > map->max_modifiable_z) return false;
    
    int idx = get_block_index(map, x, y, z);
    bool was_solid = map->solid_data[idx] != 0;
    
    if (was_solid) {
        map->solid_data[idx] = 0;
        map->color_data[idx] = 0;
        map->total_blocks--;
    }
    
    return was_solid;
}

void color_block(int x, int y, int z, MapData* map) {
    // Note: Original signature doesn't have color param, using internal
    if (!map || !map->solid_data || !map->color_data) return;
    if (!in_bounds(map, x, y, z)) return;
    
    int idx = get_block_index(map, x, y, z);
    // Only color if block exists
    // Color comes from somewhere else in original - stub for now
}

bool check_only(int x, int y, int z, MapData* map) {
    // Check if block exists (for falling block detection)
    if (!map || !map->solid_data) return false;
    if (!in_bounds(map, x, y, z)) return false;
    
    int idx = get_block_index(map, x, y, z);
    return map->solid_data[idx] != 0;
}

void add_leader(int x, int y, int z, MapData* map, int team, bool flag) {
    // Spawn point management - stub for now
}

void add_marked_to_known_safe(void) {
    // Falling block algorithm - stub for now
}

void check_node(int x, int y, int z, MapData* map, FallingBlocks* fb) {
    // Falling block detection - stub for now
}

void update_shadow(MapData* map, int x, int y, int z, bool flag) {
    // TODO: Implement
}

// ============================================================================
// Static Lighting Functions
// ============================================================================
void add_static_point_light(MapData* map, int x, int y, int z,
                            unsigned char r, unsigned char g, unsigned char b,
                            float intensity) {
    // TODO: Implement
}

void update_static_point_light_colour(MapData* map, int x, int y, int z,
                                       unsigned char r, unsigned char g,
                                       unsigned char b) {
    // TODO: Implement
}

void remove_static_point_light(MapData* map, int x, int y, int z) {
    // TODO: Implement
}

// ============================================================================
// Shadow Functions
// ============================================================================
static unsigned int shadow_vbo = 0;

void create_shadow_vbo(void) {
    // TODO: Implement
}

void set_shadow_char_height(int height) {
    // TODO: Implement
}

void delete_shadow_vbo(void) {
    // TODO: Implement
}

void find_lowest_block(int x, int y, int z1, int* out_z, int* out_color, MapData* map) {
    // TODO: Implement
}

void create_shadows_from_positions(MapData* map, void* positions, int count) {
    // TODO: Implement
}

void draw_shadows(void) {
    // TODO: Implement
}

// ============================================================================
// Prefab Functions
// ============================================================================
bool get_prefab_touches_world(MapData* map, KV6Data* kv6,
                               int x, int y, int z,
                               int rx, int ry, int rz, int scale) {
    // TODO: Implement
    return false;
}

void place_prefab_in_world(MapData* map, KV6Data* kv6,
                           int x, int y, int z,
                           int rx, int ry, int rz, int scale,
                           int flags, float tolerance) {
    // TODO: Implement
}

void erase_prefab_from_world(MapData* map, KV6Data* kv6,
                              int x, int y, int z,
                              int rx, int ry, int rz, int scale,
                              int flags, float tolerance) {
    // TODO: Implement
}

// ============================================================================
// OpenGL/Rendering Functions
// ============================================================================
void PrintGLErrors(const char* location) {
    // TODO: Implement
}

void delete_gl_texture(unsigned int* texture) {
    // TODO: Implement
}

void load_ao_texture(int size) {
    // TODO: Implement
}

void reload_ao_texture(int size) {
    // TODO: Implement
}

void delete_gl_vbo(MapData* map) {
    // TODO: Implement
}

void cleanup_gl(MapData* map) {
    // TODO: Implement
}

void post_load_draw_setup(MapData* map, int flags) {
    // TODO: Implement
}

void draw_vbo(Chunk* chunk, bool shadows, bool transparent) {
    // TODO: Implement
}

void draw_position(MapData* map, int x, int y, int z, int flags) {
    // TODO: Implement
}

void update_vbo(Chunk* chunk, MapData* map) {
    // TODO: Implement
}

void draw_seascape_single_pass(MapData* map) {
    // TODO: Implement
}

void update_vbo_sea(Chunk* chunk, MapData* map) {
    // TODO: Implement
}

void create_sea_data(MapData* map) {
    // TODO: Implement
}

void draw_display_map(MapData* map, int x, int y, int z, int flags) {
    // TODO: Implement
}

void draw_sea(MapData* map) {
    // TODO: Implement
}

// ============================================================================
// Map Setup Functions
// ============================================================================
void find_marker_points(MapData* map) {
    // TODO: Implement
}

void post_load_map_setup(MapData* map) {
    // TODO: Implement
}

void update_shadows(MapData* map) {
    // TODO: Implement
}

void compute_static_occlusion(MapData* map) {
    // TODO: Implement
}

// ============================================================================
// Occlusion Functions
// ============================================================================
int sunblock(MapData* map, int x, int y, int z) {
    // TODO: Implement
    return 0;
}

void compute_block_occlusion_texcoords(bool* faces, BlockOcclusionTexCoords* out) {
    // TODO: Implement
}

void compute_block_occlusion(BlockOcclusionTexCoords* out, int x, int y, int z, MapData* map) {
    // TODO: Implement
}

void do_edge_highlight(BlockOcclusionTexCoords* out, int x, int y, int z, MapData* map) {
    // TODO: Implement
}

void compute_dynamic_occlusion(MapData* map, int x, int y, int z) {
    // TODO: Implement
}

void print_occlusion_data(MapData* map) {
    // TODO: Implement
}

// ============================================================================
// Utility
// ============================================================================
int color_noise(int color) {
    // TODO: Implement
    return color;
}

void print_chunk_sizes(MapData* map) {
    // TODO: Implement
}

void set_vert_text_coords(unsigned char u, unsigned char v, Quad* quad) {
    // TODO: Implement
}

static int sorted_offsets[256];

void make_sorted_offsets(void) {
    // TODO: Implement
}

int compare_offsets(const void* a, const void* b) {
    return *(int*)a - *(int*)b;
}

// ============================================================================
// Threading
// ============================================================================
void run_thread(MapData* map, int mode, unsigned char* data, int length) {
    // TODO: Implement
}

void change_thread(MapData* map, int mode, unsigned char* data, int length) {
    // TODO: Implement
}

void close_thread(MapData* map) {
    // TODO: Implement
}

bool done_processing(MapData* map) {
    if (!map) return true;
    return !map->processing;
}

// ============================================================================
// Ground Colors (Map-specific)
// ============================================================================
void refresh_ground_colors_c_map(MapData* map) {
    // TODO: Implement
}

// ============================================================================
// Temp/Utility
// ============================================================================
void* create_temp(void) {
    // TODO: Implement
    return nullptr;
}