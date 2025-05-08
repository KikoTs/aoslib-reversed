#TODO: Implement World

from libc.math cimport floor
import cython

# Forward declarations for external types
cdef extern from "glm/glm.hpp" namespace "glm":
    cdef cppclass vec3[T]:
        vec3() nogil
        vec3(T) nogil
        vec3(T, T, T) nogil
        T x, y, z

cdef extern from "glm/glm.hpp" namespace "glm::detail":
    cdef cppclass tvec3[T]:
        tvec3() nogil
        tvec3(T) nogil
        tvec3(T, T, T) nogil
        T x, y, z

# C-level type declarations
ctypedef struct MapData:
    pass

ctypedef struct PlayerType:
    pass

ctypedef struct GenericMovementType:
    pass

ctypedef struct ControlledGenericMovementType:
    pass

# C-level function declarations
cdef class BlockLine:
    cdef:
        # Private attributes
        pass
    
    cdef NextBlock(self)

cdef clipworld(long x, long y, long z, float *height)

cdef GetBlockFromRayWorldSpace(tvec3[float] *pos, tvec3[float] *direction, float max_distance, tvec3[int] *result, int *face, bint player_objects)

cdef GetBlockFromRayWorldSpace(tvec3[float] *pos, tvec3[float] *direction, float max_distance, tvec3[int] *result, int *face, tvec3[float] *hitpoint, bint player_objects)

cdef hitscan_accurate(tvec3[float] *pos, tvec3[float] *direction, tvec3[int] *result, float max_distance, tvec3[float] *hitpoint, int *face, bint player_objects)

cdef hitscan(tvec3[float] *pos, tvec3[float] *direction, tvec3[int] *result, int *face)

cdef hitscan_point_to_point(tvec3[float] *start, tvec3[float] *end, tvec3[int] *result, int *face)

cdef check_for_ground_holes(PlayerType *player)

cdef create_generic_movement(tvec3[float] *position, tvec3[float] *velocity)

cdef set_bouncing(GenericMovementType *movement, bint enabled)

cdef set_stop_on_collision(GenericMovementType *movement, bint enabled)

cdef set_stop_on_face(GenericMovementType *movement, bint enabled)

cdef set_gravity_multiplier(GenericMovementType *movement, float value)

cdef set_max_speed(GenericMovementType *movement, float value)

cdef set_allow_burying(GenericMovementType *movement, bint enabled)

cdef set_allow_floating(GenericMovementType *movement, bint enabled)

cdef destroy_generic_movement(GenericMovementType *movement)

cdef destroy_controlled_generic_movement(ControlledGenericMovementType *movement)

cdef create_controlled_generic_movement(tvec3[float] *position, tvec3[float] *velocity, tvec3[float] *forward_vector)

cdef sq_magnitude(tvec3[float] vec)

cdef magnitude(tvec3[float] vec)

cdef norm(tvec3[float] vec)

cdef sq_distance(tvec3[float] vec1, tvec3[float] vec2)

cdef move_generic(GenericMovementType *movement, bint interpolate)

cdef move_controlled_generic(ControlledGenericMovementType *movement)

cdef create_player()

cdef copy_player(PlayerType *dest, PlayerType *source, int preserve_state)

cdef destroy_player(PlayerType *player)

cdef autoclimb_offset(PlayerType *player)

cdef reposition_player(PlayerType *player, tvec3[float] *position)

cdef clipbox(float x, float y, float z, bint player_objects, object objects, int object_count, float *height)

cdef round(float val)

cdef boxclipmove(PlayerType *player, object objects, int object_count, float *height)

cdef collide_with_players(PlayerType *player, object objects, int object_count, float height, bint slide)

cdef move_player(PlayerType *player, object objects, int object_count, float *height)

cdef try_uncrouch(PlayerType *player, object objects, int object_count, float *height)

cdef reorient_player(PlayerType *player, tvec3[float] *orientation)

cdef cube_line(int x1, int y1, int z1, int x2, int y2, int z2)

cdef check_collision(tvec3[float] *position)

cdef vecrand(tvec3[float] *vector)

cdef bounce(tvec3[float] *velocity, tvec3[float] *normal)

cdef check_cube_placement(tvec3[int] *position, PlayerType *player, float height, int facing)

cdef get_cube_sq_distance()

cdef is_centered(double x, double y, double z, double cx, double cy, double cz, double width, double height, double depth, double epsilon)

cdef update_timer(float dt, float tick_rate)

cdef set_globals(MapData *map_data)

cdef set_gravity(float value)

cdef get_gravity()

cdef _initworld()

# Python wrapper classes
cdef class World:
    cdef:
        object map
        float timer
    
    cpdef set_gravity(self, float value)
    cpdef get_gravity(self)
    cpdef create_object(self, object object_type, object position)
    cpdef update(self)
    cpdef hitscan(self, object position, object direction)
    cpdef hitscan_accurate(self, object position, object direction, float max_distance=*, bint player_objects=*)
    cpdef get_block_face_center_position(self, object position, int face)

cdef class Object:
    cdef:
        object name
        object position
        bint deleted
        World world
    
    cpdef check_valid_position(self)
    cpdef delete(self)
    cpdef initialize(self)
    cpdef update(self, float dt)

cdef class Player(Object):
    cdef:
        bint up
        bint down
        bint left
        bint right
        bint jump
        bint hover
        bint jump_this_frame
        bint crouch
        bint sneak
        bint burdened
        bint sprint
        bint wade
        bint airborne
        bint fall
        bint jetpack
        bint jetpack_active
        bint jetpack_passive
        bint parachute
        bint parachute_active
        object orientation
        object velocity
        object s  # state
        bint is_locked_to_box
    
    cpdef initialize(self)
    cpdef update(self, float dt, object objects=*)
    cpdef set_locked_to_box(self)
    cpdef clear_locked_to_box(self)
    cpdef set_orientation(self, object orientation)
    cpdef set_position(self, object position, bint force=*)
    cpdef set_velocity(self, object velocity, bint force=*)
    cpdef set_walk(self, bint up, bint down, bint left, bint right)
    cpdef set_crouch(self, bint crouch, bint force=*)
    cpdef set_dead(self, bint dead)
    cpdef set_exploded(self, bint exploded)
    cpdef set_class_accel_multiplier(self, float value)
    cpdef set_class_sprint_multiplier(self, float value)
    cpdef set_class_crouch_sneak_multiplier(self, float value)
    cpdef set_class_fall_on_water_damage_multiplier(self, float value)
    cpdef set_class_jump_multiplier(self, float value)
    cpdef set_class_can_sprint_uphill(self, bint value)
    cpdef set_climb_slowdown(self, float value)
    cpdef set_class_water_friction(self, float value)
    cpdef set_class_falling_damage_min_distance(self, float value)
    cpdef set_class_falling_damage_max_distance(self, float value)
    cpdef set_class_falling_damage_max_damage(self, float value)
    cpdef check_cube_placement(self, object position, float height=*, int facing=*)
    cpdef get_cube_sq_distance(self)

cdef class PlayerMovementHistory:
    cdef:
        object position
        object velocity
        int loop_count
    
    cpdef set_all_data(self, object position, object velocity, int loop_count)
    cpdef get_client_data(self)

cdef class Debris(Object):
    cdef:
        object velocity
        object rotation
        object rotation_speed
        bint in_use
    
    cpdef initialize(self, object position=*, object velocity=*, object rotation=*)
    cpdef use(self)
    cpdef free(self)
    cpdef update(self, float dt)

cdef class FallingBlocks(Object):
    cdef:
        object velocity
        object rotation
    
    cpdef initialize(self, object position=*, object velocity=*)
    cpdef update(self, float dt)

cdef class GenericMovement(Object):
    cdef:
        object velocity
        object last_hit_collision_block
        object last_hit_normal
    
    cpdef initialize(self, object position=*, object velocity=*)
    cpdef set_bouncing(self, bint enabled)
    cpdef set_stop_on_collision(self, bint enabled)
    cpdef set_stop_on_face(self, bint enabled)
    cpdef set_allow_burying(self, bint enabled)
    cpdef set_allow_floating(self, bint enabled)
    cpdef set_gravity_multiplier(self, float value)
    cpdef set_max_speed(self, float value)
    cpdef update(self, float dt)
    cpdef set_position(self, object position)
    cpdef set_velocity(self, object velocity)

cdef class ControlledGenericMovement(GenericMovement):
    cdef:
        bint input_forward
        bint input_back
        bint input_left
        bint input_right
        bint strafing
        float speed_forward
        float speed_back
        float speed_left
        float speed_right
        object forward_vector
    
    cpdef initialize(self, object position=*, object velocity=*, object forward_vector=*)
    cpdef set_forward_vector(self, object forward_vector)

cdef class Grenade(Object):
    cdef:
        object velocity
        float fuse
    
    cpdef initialize(self, object position=*, object velocity=*)
    cpdef update(self, float dt)

# Helper functions
cpdef get_next_cube(int x, int y, int z, int face)
cpdef cube_line(int x1, int y1, int z1, int x2, int y2, int z2)
cpdef get_random_vector()
cpdef is_centered(double x, double y, double z, double cx, double cy, double cz, 
                 double width, double height, double depth, double epsilon=*)
cpdef parse_constant_overrides(object data)
cpdef A2(int x)
