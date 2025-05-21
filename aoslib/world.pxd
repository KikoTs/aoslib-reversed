# from .vxl cimport VXL, AceMap
from aoslib cimport vxl
from shared cimport glm
from libcpp cimport bool

# C++ class declarations
cdef extern from "world_c.cpp" nogil:
    cdef cppclass AcePlayer:
        AcePlayer(vxl.AceMap *map) except +
        long update(double dt, double time)
        void set_orientation(double x, double y, double z)

        vxl.AceMap *map
        bool mf, mb, ml, mr, jump, crouch, sneak, sprint, primary_fire, secondary_fire, airborne, wade, alive, weapon
        float lastclimb
        double p_x, p_y, p_z  # Position
        double v_x, v_y, v_z  # Velocity 
        double f_x, f_y, f_z  # Forward direction
        double e_x, e_y, e_z  # Eye position

    cdef cppclass AceGrenade:
        AceGrenade(vxl.AceMap *map, double px, double py, double pz, double vx, double vy, double vz) except +
        bool update(double dt, double time)
        bool next_collision(double dt, double max, double *eta, double *px, double *py, double *pz)

        vxl.AceMap *map
        double p_x, p_y, p_z  # Position
        double v_x, v_y, v_z  # Velocity

    bool c_cast_ray "cast_ray" (vxl.AceMap *map,
                               double px, double py, double pz, 
                               double dx, double dy, double dz,
                               long *x, long *y, long *z, float length, bool isdirection)

    bool clipbox(vxl.AceMap *map, float x, float y, float z)


cdef class WorldObject:
    cdef public:
        str name
        vxl.VXL map

    cdef long update(self, double dt, double time)


cdef class Player:
    cdef AcePlayer *ply
    cdef public:
        glm.Vector3 position, velocity, orientation, eye
    
    cdef _sync_from_cpp(self)
    cdef _sync_to_cpp(self)


cdef class Grenade:
    cdef AceGrenade *grenade
    cdef public:
        glm.Vector3 position, velocity
    
    cdef _sync_from_cpp(self)
    cdef _sync_to_cpp(self)


cdef class GenericMovement:
    cdef public:
        vxl.VXL map
        glm.Vector3 position
