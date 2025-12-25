# World module declarations for Cython
# cython: language_level=3

# ============================================================================
# Module-level Functions
# ============================================================================
cpdef object A2(object arg)
cpdef object cube_line(int x1, int y1, int z1, int x2, int y2, int z2)
cpdef float floor(float val)
cpdef tuple get_next_cube(tuple pos, tuple direction)
cpdef tuple get_random_vector()
cpdef bint is_centered(tuple pos)
cpdef object parse_constant_overrides(object arg)
cdef bint clipbox(object map_obj, float x, float y, float z)
cdef bint clipworld(object map_obj, long x, long y, long z)

# ============================================================================
# World Class
# ============================================================================
cdef class World:
    cdef public object map
    cdef public float timer
    cdef float _gravity
    cdef public list objects
    
    cpdef object create_object(self, object obj_type)
    cpdef tuple get_block_face_center_position(self, object pos, int face)
    cpdef float get_gravity(self)
    cpdef void set_gravity(self, float gravity)
    cpdef bint get_solid(self, int x, int y, int z)
    cpdef object hitscan(self, tuple start, tuple direction, float max_distance)
    cpdef object hitscan_accurate(self, tuple start, tuple direction, float max_distance)
    cpdef void update(self, float dt)

# ============================================================================
# Base Object Class
# ============================================================================
cdef class Object:
    cdef public bint deleted
    cdef public str name
    cdef public tuple position
    cdef public object world
    
    cpdef bint check_valid_position(self, tuple pos)
    cpdef void delete(self)
    cpdef void initialize(self)
    cpdef void update(self, float dt)

# ============================================================================
# Player Class
# ============================================================================
cdef class Player(Object):
    # Movement input state
    cdef public bint airborne
    cdef public bint burdened
    cdef public bint crouch
    cdef public bint down
    cdef public bint fall
    cdef public bint hover
    cdef public bint is_locked_to_box
    cdef public bint jetpack
    cdef public bint jetpack_active
    cdef public bint jetpack_passive
    cdef public bint jump
    cdef public bint jump_this_frame
    cdef public float last_climb
    cdef public float timer
    cdef public float fall_damage_this_frame
    cdef public bint left
    cdef public tuple orientation
    cdef public bint parachute
    cdef public bint parachute_active
    cdef public bint right
    cdef public object s
    cdef public bint sneak
    cdef public bint sprint
    cdef public bint up
    cdef public tuple velocity
    cdef public bint wade
    
    # Class multipliers (private)
    cdef float _accel_multiplier
    cdef float _sprint_multiplier
    cdef float _crouch_sneak_multiplier
    cdef float _jump_multiplier
    cdef float _water_friction
    cdef float _falling_damage_min_dist
    cdef float _falling_damage_max_dist
    cdef float _falling_damage_max_damage
    cdef float _fall_on_water_damage_mult
    cdef bint _can_sprint_uphill
    cdef float _climb_slowdown
    cdef bint _dead
    cdef bint _exploded
    cdef bint _walk
    
    cpdef bint check_cube_placement(self, int x, int y, int z)
    cpdef void clear_locked_to_box(self)
    cpdef float get_cube_sq_distance(self, int x, int y, int z)
    cpdef void set_class_accel_multiplier(self, float multiplier)
    cpdef void set_class_can_sprint_uphill(self, bint can_sprint)
    cpdef void set_class_crouch_sneak_multiplier(self, float multiplier)
    cpdef void set_class_fall_on_water_damage_multiplier(self, float multiplier)
    cpdef void set_class_falling_damage_max_damage(self, float damage)
    cpdef void set_class_falling_damage_max_distance(self, float distance)
    cpdef void set_class_falling_damage_min_distance(self, float distance)
    cpdef void set_class_jump_multiplier(self, float multiplier)
    cpdef void set_class_sprint_multiplier(self, float multiplier)
    cpdef void set_class_water_friction(self, float friction)
    cpdef void set_climb_slowdown(self, float slowdown)
    cpdef void set_crouch(self, bint crouch)
    cpdef void set_dead(self, bint is_dead)
    cpdef void set_exploded(self, bint exploded)
    cpdef void set_locked_to_box(self, object box)
    cpdef void set_orientation(self, object orientation)
    cpdef void set_position(self, object x, object y, object z)
    cpdef void set_velocity(self, object x, object y, object z)
    cpdef void set_walk(self, bint walk)
    cpdef void update_class_multipliers(self, int class_id)
    cpdef void update(self, float dt)
    cdef void boxclipmove(self, double dt, double time)
    cdef void reposition(self, double dt, double time)

# ============================================================================
# PlayerMovementHistory Class
# ============================================================================
cdef class PlayerMovementHistory:
    cdef public int loop_count
    cdef public list position
    cdef public list velocity
    
    cpdef dict get_client_data(self)
    cpdef void set_all_data(self, dict data)

# ============================================================================
# Grenade Class
# ============================================================================
cdef class Grenade(Object):
    cdef public float fuse
    cdef public tuple velocity
    cdef float _gravity_mult
    cdef float _bounce

# ============================================================================
# GenericMovement Class
# ============================================================================
cdef class GenericMovement(Object):
    cdef public tuple last_hit_collision_block
    cdef public tuple last_hit_normal
    cdef public tuple velocity
    
    cdef bint _allow_burying
    cdef bint _allow_floating
    cdef bint _bouncing
    cdef float _gravity_mult
    cdef float _max_speed
    cdef bint _stop_on_collision
    cdef int _stop_on_face
    
    cpdef void set_allow_burying(self, bint allow)
    cpdef void set_allow_floating(self, bint allow)
    cpdef void set_bouncing(self, bint bouncing)
    cpdef void set_gravity_multiplier(self, float multiplier)
    cpdef void set_max_speed(self, float speed)
    cpdef void set_position(self, float x, float y, float z)
    cpdef void set_stop_on_collision(self, bint stop)
    cpdef void set_stop_on_face(self, int face)
    cpdef void set_velocity(self, float x, float y, float z)

# ============================================================================
# FallingBlocks Class
# ============================================================================
cdef class FallingBlocks(Object):
    cdef public tuple rotation
    cdef public tuple velocity
    cdef public list blocks

# ============================================================================
# Debris Class
# ============================================================================
cdef class Debris(Object):
    cdef public bint in_use
    cdef public tuple rotation
    cdef public tuple rotation_speed
    cdef public tuple velocity
    cdef float _lifetime
    
    cpdef void free(self)
    cpdef void use(self)

# ============================================================================
# ControlledGenericMovement Class
# ============================================================================
cdef class ControlledGenericMovement(Object):
    cdef public tuple forward_vector
    cdef public bint input_back
    cdef public bint input_forward
    cdef public bint input_left
    cdef public bint input_right
    cdef public tuple last_hit_collision_block
    cdef public tuple last_hit_normal
    cdef public float speed_back
    cdef public float speed_forward
    cdef public float speed_left
    cdef public float speed_right
    cdef public bint strafing
    cdef public tuple velocity
    
    cdef bint _allow_burying
    cdef bint _allow_floating
    cdef bint _bouncing
    cdef float _gravity_mult
    cdef float _max_speed
    cdef bint _stop_on_collision
    cdef int _stop_on_face
    
    cpdef void set_allow_burying(self, bint allow)
    cpdef void set_allow_floating(self, bint allow)
    cpdef void set_bouncing(self, bint bouncing)
    cpdef void set_forward_vector(self, tuple vector)
    cpdef void set_gravity_multiplier(self, float multiplier)
    cpdef void set_max_speed(self, float speed)
    cpdef void set_position(self, float x, float y, float z)
    cpdef void set_stop_on_collision(self, bint stop)
    cpdef void set_stop_on_face(self, int face)
    cpdef void set_velocity(self, float x, float y, float z)
