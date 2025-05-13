# cython: language_level=3
# distutils: language = c++

from libcpp cimport bool

cdef extern from "glm_c.h":
    cdef cppclass Vector3Cpp "Vector3":
        double x, y, z
        
        Vector3Cpp() except +
        Vector3Cpp(double x, double y, double z) except +
        Vector3Cpp copy()
        double* get()
        Vector3Cpp& set(double x, double y, double z)
        Vector3Cpp& set_vector(Vector3Cpp& other)
        Vector3Cpp translate(double dx, double dy, double dz)
        double distance(Vector3Cpp& other)
        double dot(Vector3Cpp& other)
        Vector3Cpp cross(Vector3Cpp& other)
        Vector3Cpp slerp(Vector3Cpp& other, double t)
        double sq_distance(Vector3Cpp& other)
        double magnitude()
        double sq_magnitude()
        Vector3Cpp norm()
        Vector3Cpp clamp(double min_val, double max_val)
        Vector3Cpp clamp(Vector3Cpp& min_val, Vector3Cpp& max_val)
    
    cdef cppclass IntVector3Cpp "IntVector3":
        int x, y, z
        
        IntVector3Cpp() except +
        IntVector3Cpp(int x, int y, int z) except +
        IntVector3Cpp copy()
        int* get()
        IntVector3Cpp& set(int x, int y, int z)
        IntVector3Cpp& set_vector(IntVector3Cpp& other)
    
    cdef cppclass Matrix4Cpp "Matrix4":
        double data[16]
        
        Matrix4Cpp() except +
        Matrix4Cpp& set_identity()
        Matrix4Cpp copy()
        Matrix4Cpp& rotate(double angle, double x, double y, double z)
        Matrix4Cpp& translate(double x, double y, double z)
        Matrix4Cpp& orientation(double fx, double fy, double fz, double ux, double uy, double uz)
        Vector3Cpp multiply_vector(Vector3Cpp& vector)

cdef class Vector3:
    cdef Vector3Cpp cpp_obj
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
    cdef IntVector3Cpp cpp_obj
    cpdef IntVector3 copy(self)
    cpdef get(self)
    cpdef set(self, int x, int y, int z)
    cpdef set_vector(self, IntVector3 other)

cdef class Matrix4:
    cdef Matrix4Cpp cpp_obj
    cpdef set_identity(self)
    cpdef Matrix4 copy(self)
    cpdef rotate(self, double angle, axis)
    cpdef translate(self, vector)
    cpdef orientation(self, forward, up)
    cpdef Vector3 multiply_vector(self, Vector3 vector)
