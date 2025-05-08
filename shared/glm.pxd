#TODO: Implement GLM

cdef class Vector3:
    cdef public double x, y, z
    
    cpdef Vector3 copy(self)
    cpdef get(self)
    cpdef set(self, double x, double y, double z)
    cpdef set_vector(self, Vector3 other)
    cpdef translate(self, double dx, double dy, double dz)
    cpdef double distance(self, Vector3 other)
    cpdef double dot(self, Vector3 other)
    cpdef Vector3 cross(self, Vector3 other)
    cpdef Vector3 slerp(self, Vector3 other, double t)
    cpdef double sq_distance(self, Vector3 other)
    cpdef double magnitude(self)
    cpdef double sq_magnitude(self)
    cpdef Vector3 norm(self)
    cpdef Vector3 clamp(self, min_val, max_val)

cdef class IntVector3:
    cdef public int x, y, z
    
    cpdef IntVector3 copy(self)
    cpdef get(self)
    cpdef set(self, int x, int y, int z)
    cpdef set_vector(self, IntVector3 other)

cdef class Matrix4:
    cdef double[16] data
    
    cpdef set_identity(self)
    cpdef Matrix4 copy(self)
    cpdef rotate(self, double angle, axis)
    cpdef translate(self, vector)
    cpdef orientation(self, forward, up)
    cpdef Vector3 multiply_vector(self, Vector3 vector)
