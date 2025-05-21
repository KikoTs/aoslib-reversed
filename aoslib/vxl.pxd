# distutils: sources = aoslib/vxl_c.cpp
from libc.stdint cimport *
from libcpp.vector cimport vector
from libcpp cimport bool

cdef extern from "vxl_c.h" nogil:
    struct Pos3:
        int x, y, z

    # Add constants
    cdef int MAP_X
    cdef int MAP_Y 
    cdef int MAP_Z
    cdef uint32_t DEFAULT_COLOR

    cdef cppclass AceMap:
        AceMap(uint8_t *buf) except +
        void read(uint8_t *buf) except +
        vector[uint8_t] write() except +
        size_t write(vector[uint8_t] &v, int *sx, int *sy, int columns);

        bool is_surface(int x, int y, int z) except +
        bool get_solid(int x, int y, int z, bool wrapped=False) except +
        uint32_t get_color(int x, int y, int z, bool wrapped=False) except +
        int get_z(int x, int y, int start) except +
        void get_random_point(int *x, int *y, int *z, int x1, int y1, int x2, int y2)
        vector[Pos3] get_neighbors(int x, int y, int z)
        vector[Pos3] block_line(int x1, int y1, int z1, int x2, int y2, int z2)

        bool set_point(int x, int y, int z, bool solid, uint32_t color) except +
        void set_column_solid(int x, int y, int z_start, int z_end, bool solid) except +
        void set_column_color(int x, int y, int z_start, int z_end, uint32_t solid) except +

        bool check_node(int x, int y, int z, bool destroy)

    int get_pos(int x, int y, int z)
    bool is_valid_pos(int x, int y, int z)
    bool is_valid_pos(int pos)

cpdef block_color(int r, int g, int b)

cdef class VXL:
    cdef:
        AceMap *map_data
        
    cpdef add_point(self, int x, int y, int z, tuple color)
    cpdef add_static_light(self, int x, int y, int z, unsigned char r, unsigned char g, unsigned char b, float light_radius)
    cpdef change_thread_state(self, int state, object data, int data_size)
    cpdef check_only(self, int x, int y, int z)
    cpdef chunk_to_pointlist(self, chunk)
    cpdef cleanup(self)
    cpdef clear_checked_geometry(self)
    cpdef color_block(self, int x, int y, int z)
    cpdef create_spot_shadows(self, positions)
    cpdef destroy(self)
    cpdef done_processing(self)
    cpdef draw(self, int x, int y, int z, int draw_distance)
    cpdef draw_sea(self)
    cpdef draw_spot_shadows(self)
    cpdef erase_prefab_from_world(self, model, int position_x, int position_y, int position_z, int prefab_yaw, int prefab_pitch, int prefab_roll, int from_block_index, int to_block_index, float time_limit)
    cpdef generate_vxl(self, novo=*)
    cpdef get_color(self, int x, int y, int z)
    cpdef get_color_tuple(self, int x, int y, int z)
    cpdef get_ground_colors(self)
    cpdef get_max_modifiable_z(self)
    cpdef get_overview(self, z=*, rgba=*)
    cpdef get_point(self, int x, int y, int z)
    cpdef get_prefab_touches_world(self, model, int position_x, int position_y, int position_z, int prefab_yaw, int prefab_pitch, int prefab_roll, int check_world_bounds)
    cpdef get_solid(self, int x, int y, int z)
    cpdef has_neighbors(self, int x, int y, int z, int solid_only)
    cpdef is_space_to_add_blocks(self)
    cpdef place_prefab_in_world(self, model, int position_x, int position_y, int position_z, int prefab_yaw, float prefab_pitch, int prefab_roll, int from_block_index, int to_block_index, float time_limit)
    cpdef post_load_draw_setup(self, texture_quality=*)
    cpdef refresh_ground_colors(self)
    cpdef remove_point(self, int x, int y, int z)
    cpdef remove_point_nochecks(self, int x, int y, int z)
    cpdef remove_static_light(self, int x, int y, int z)
    cpdef set_max_modifiable_z(self, int max_z)
    cpdef set_point(self, int x, int y, int z, tuple color_tuple)
    cpdef set_shadow_char_height(self, int height)
    cpdef update_static_light_colour(self, int x, int y, int z, unsigned char r, unsigned char g, unsigned char b)