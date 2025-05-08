#TODO: Implement World

# Glm vector type imports
from libc.math cimport floor
import cython

cdef class BlockLine:
    def __cinit__(self, glm.detail.tvec3[float] const& start, glm.detail.tvec3[float] const& end):
        pass
        
    def __dealloc__(self):
        pass
    
    def NextBlock(self):
        pass

cdef clipworld(long x, long y, long z, float *height):
    pass

cdef GetBlockFromRayWorldSpace(glm.detail.tvec3[float] *pos, glm.detail.tvec3[float] *direction, float max_distance, glm.detail.tvec3[int] *result, int *face, bool player_objects):
    pass

cdef GetBlockFromRayWorldSpace(glm.detail.tvec3[float] *pos, glm.detail.tvec3[float] *direction, float max_distance, glm.detail.tvec3[int] *result, int *face, glm.detail.tvec3[float] *hitpoint, bool player_objects):
    pass

cdef hitscan_accurate(glm.detail.tvec3[float] *pos, glm.detail.tvec3[float] *direction, glm.detail.tvec3[int] *result, float max_distance, glm.detail.tvec3[float] *hitpoint, int *face, bool player_objects):
    pass

cdef hitscan(glm.detail.tvec3[float] *pos, glm.detail.tvec3[float] *direction, glm.detail.tvec3[int] *result, int *face):
    pass

cdef hitscan_point_to_point(glm.detail.tvec3[float] *start, glm.detail.tvec3[float] *end, glm.detail.tvec3[int] *result, int *face):
    pass

cdef check_for_ground_holes(PlayerType *player):
    pass

cdef create_generic_movement(glm.detail.tvec3[float] *position, glm.detail.tvec3[float] *velocity):
    pass

cdef set_bouncing(GenericMovementType *movement, bool enabled):
    pass

cdef set_stop_on_collision(GenericMovementType *movement, bool enabled):
    pass

cdef set_stop_on_face(GenericMovementType *movement, bool enabled):
    pass

cdef set_gravity_multiplier(GenericMovementType *movement, float value):
    pass

cdef set_max_speed(GenericMovementType *movement, float value):
    pass

cdef set_allow_burying(GenericMovementType *movement, bool enabled):
    pass

cdef set_allow_floating(GenericMovementType *movement, bool enabled):
    pass

cdef destroy_generic_movement(GenericMovementType *movement):
    pass

cdef destroy_controlled_generic_movement(ControlledGenericMovementType *movement):
    pass

cdef create_controlled_generic_movement(glm.detail.tvec3[float] *position, glm.detail.tvec3[float] *velocity, glm.detail.tvec3[float] *forward_vector):
    pass

cdef sq_magnitude(glm.detail.tvec3[float] vec):
    pass

cdef magnitude(glm.detail.tvec3[float] vec):
    pass

cdef norm(glm.detail.tvec3[float] vec):
    pass

cdef sq_distance(glm.detail.tvec3[float] vec1, glm.detail.tvec3[float] vec2):
    pass

cdef move_generic(GenericMovementType *movement, bool interpolate):
    pass

cdef move_controlled_generic(ControlledGenericMovementType *movement):
    pass

cdef create_player():
    pass

cdef copy_player(PlayerType *dest, PlayerType *source, int preserve_state):
    pass

cdef destroy_player(PlayerType *player):
    pass

cdef autoclimb_offset(PlayerType *player):
    pass

cdef reposition_player(PlayerType *player, glm.detail.tvec3[float] *position):
    pass

cdef clipbox(float x, float y, float z, bool player_objects, _object *objects, int object_count, float *height):
    pass

cdef round(float val):
    pass

cdef boxclipmove(PlayerType *player, _object *objects, int object_count, float *height):
    pass

cdef collide_with_players(PlayerType *player, _object *objects, int object_count, float height, bool slide):
    pass

cdef move_player(PlayerType *player, _object *objects, int object_count, float *height):
    pass

cdef try_uncrouch(PlayerType *player, _object *objects, int object_count, float *height):
    pass

cdef reorient_player(PlayerType *player, glm.detail.tvec3[float] *orientation):
    pass

cdef cube_line(int x1, int y1, int z1, int x2, int y2, int z2):
    pass

cdef check_collision(glm.detail.tvec3[float] *position):
    pass

cdef vecrand(glm.detail.tvec3[float] *vector):
    pass

cdef bounce(glm.detail.tvec3[float] *velocity, glm.detail.tvec3[float] *normal):
    pass

cdef check_cube_placement(glm.detail.tvec3[int] *position, PlayerType *player, float height, int facing):
    pass

cdef get_cube_sq_distance():
    pass

cdef is_centered(double x, double y, double z, double cx, double cy, double cz, double width, double height, double depth, double epsilon):
    pass

cdef update_timer(float dt, float tick_rate):
    pass

cdef set_globals(MapData *map_data):
    pass

cdef set_gravity(float value):
    pass

cdef get_gravity():
    pass

cdef _initworld():
    pass

# Python wrapper classes
cdef class World:
    def __init__(self, map_data):
        pass
    
    def set_gravity(self, value):
        pass
    
    def get_gravity(self):
        pass
    
    def create_object(self, object_type, position):
        pass
    
    def update(self):
        pass
    
    def hitscan(self, position, direction):
        pass
    
    def hitscan_accurate(self, position, direction, max_distance=100.0, player_objects=False):
        pass
    
    def get_block_face_center_position(self, position, face):
        pass

cdef class Object:
    def __init__(self, World world, position=None):
        pass
    
    def check_valid_position(self):
        pass
    
    def delete(self):
        pass
    
    def initialize(self):
        pass
    
    def update(self, dt):
        pass

cdef class Player(Object):
    def initialize(self):
        pass
    
    def update(self, dt, objects=None):
        pass
    
    def set_locked_to_box(self):
        pass
    
    def clear_locked_to_box(self):
        pass
    
    def set_orientation(self, orientation):
        pass
    
    def set_position(self, position, force=False):
        pass
    
    def set_velocity(self, velocity, force=False):
        pass
    
    def set_walk(self, up, down, left, right):
        pass
    
    def set_crouch(self, crouch, force=False):
        pass
    
    def set_dead(self, dead):
        pass
    
    def set_exploded(self, exploded):
        pass
    
    def set_class_accel_multiplier(self, value):
        pass
    
    def set_class_sprint_multiplier(self, value):
        pass
    
    def set_class_crouch_sneak_multiplier(self, value):
        pass
    
    def set_class_fall_on_water_damage_multiplier(self, value):
        pass
    
    def set_class_jump_multiplier(self, value):
        pass
    
    def set_class_can_sprint_uphill(self, value):
        pass
    
    def set_climb_slowdown(self, value):
        pass
    
    def set_class_water_friction(self, value):
        pass
    
    def set_class_falling_damage_min_distance(self, value):
        pass
    
    def set_class_falling_damage_max_distance(self, value):
        pass
    
    def set_class_falling_damage_max_damage(self, value):
        pass
    
    def check_cube_placement(self, position, height=None, facing=0):
        pass
    
    def get_cube_sq_distance(self):
        pass

cdef class PlayerMovementHistory:
    def __init__(self):
        pass
    
    def set_all_data(self, position, velocity, loop_count):
        pass
    
    def get_client_data(self):
        pass

cdef class Debris(Object):
    def initialize(self, position=None, velocity=None, rotation=None):
        pass
    
    def use(self):
        pass
    
    def free(self):
        pass
    
    def update(self, dt):
        pass

cdef class FallingBlocks(Object):
    def initialize(self, position=None, velocity=None):
        pass
    
    def update(self, dt):
        pass

cdef class GenericMovement(Object):
    def initialize(self, position=None, velocity=None):
        pass
    
    def set_bouncing(self, enabled):
        pass
    
    def set_stop_on_collision(self, enabled):
        pass
    
    def set_stop_on_face(self, enabled):
        pass
    
    def set_allow_burying(self, enabled):
        pass
    
    def set_allow_floating(self, enabled):
        pass
    
    def set_gravity_multiplier(self, value):
        pass
    
    def set_max_speed(self, value):
        pass
    
    def update(self, dt):
        pass
    
    def set_position(self, position):
        pass
    
    def set_velocity(self, velocity):
        pass

cdef class ControlledGenericMovement(GenericMovement):
    def initialize(self, position=None, velocity=None, forward_vector=None):
        pass
    
    def set_bouncing(self, enabled):
        pass
    
    def set_stop_on_collision(self, enabled):
        pass
    
    def set_stop_on_face(self, enabled):
        pass
    
    def set_allow_burying(self, enabled):
        pass
    
    def set_allow_floating(self, enabled):
        pass
    
    def set_gravity_multiplier(self, value):
        pass
    
    def set_max_speed(self, value):
        pass
    
    def update(self, dt):
        pass
    
    def set_position(self, position):
        pass
    
    def set_velocity(self, velocity):
        pass
    
    def set_forward_vector(self, forward_vector):
        pass

cdef class Grenade(Object):
    def initialize(self, position=None, velocity=None):
        pass
    
    def update(self, dt):
        pass

# Helper functions
def get_next_cube(x, y, z, face):
    pass

def cube_line(x1, y1, z1, x2, y2, z2):
    pass

def get_random_vector():
    pass

def is_centered(x, y, z, cx, cy, cz, width, height, depth, epsilon=0.1):
    pass

def parse_constant_overrides(data):
    pass

def A2(x):
    pass
