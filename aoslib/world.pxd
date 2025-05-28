from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector

# Forward declarations
cdef class World
cdef class Object
cdef class Player
cdef class PlayerMovementHistory
cdef class Grenade
cdef class GenericMovement
cdef class FallingBlocks
cdef class Debris
cdef class ControlledGenericMovement

# Module-level functions
cpdef object A2(object arg)
cpdef object cube_line(object arg1, object arg2, object arg3)
cpdef object floor(object val)
cpdef object get_next_cube(object arg1, object arg2)
cpdef object get_random_vector()
cpdef bool is_centered(object arg)
cpdef object parse_constant_overrides(object arg)

# World class
cdef class World:
    cdef public object map
    cdef public object timer

# Base Object class
cdef class Object:
    cdef public bool deleted
    cdef public object name
    cdef public object position
    


# Player class (inherits from Object)
cdef class Player(Object):
    cdef public bool airborne
    cdef public bool burdened
    cdef public bool crouch
    cdef public bool down
    cdef public bool fall
    cdef public bool hover
    cdef public bool is_locked_to_box
    cdef public bool jetpack
    cdef public bool jetpack_active
    cdef public bool jetpack_passive
    cdef public bool jump
    cdef public bool jump_this_frame
    cdef public bool left
    cdef public object orientation
    cdef public bool parachute
    cdef public bool parachute_active
    cdef public bool right
    cdef public object s
    cdef public bool sneak
    cdef public bool sprint
    cdef public bool up
    cdef public object velocity
    cdef public bool wade
    
    cpdef void set_orientation(self, object orientation)
    cpdef void set_position(self, object x, object y, object z)
    cpdef void set_velocity(self, object x, object y, object z)

# PlayerMovementHistory class
cdef class PlayerMovementHistory:
    cdef public object loop_count
    cdef public object position
    cdef public object velocity

# Grenade class (inherits from Object)
cdef class Grenade(Object):
    cdef public object fuse
    cdef public object velocity

# GenericMovement class (inherits from Object)
cdef class GenericMovement(Object):
    cdef public object last_hit_collision_block
    cdef public object last_hit_normal
    cdef public object velocity

# FallingBlocks class (inherits from Object)
cdef class FallingBlocks(Object):
    cdef public object rotation
    cdef public object velocity

# Debris class (inherits from Object)
cdef class Debris(Object):
    cdef public bool in_use
    cdef public object rotation
    cdef public object rotation_speed
    cdef public object velocity

# ControlledGenericMovement class (inherits from Object)
cdef class ControlledGenericMovement(Object):
    cdef public object forward_vector
    cdef public bool input_back
    cdef public bool input_forward
    cdef public bool input_left
    cdef public bool input_right
    cdef public object last_hit_collision_block
    cdef public object last_hit_normal
    cdef public object speed_back
    cdef public object speed_forward
    cdef public object speed_left
    cdef public object speed_right
    cdef public bool strafing
    cdef public object velocity
