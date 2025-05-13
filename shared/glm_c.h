#ifndef GLM_H
#define GLM_H

class Vector3 {
public:
    double x, y, z;
    
    Vector3(double x = 0.0, double y = 0.0, double z = 0.0);
    Vector3 copy();
    double* get();
    Vector3& set(double x, double y, double z);
    Vector3& set_vector(Vector3& other);
    Vector3 translate(double dx, double dy, double dz);
    double distance(Vector3& other);
    double dot(Vector3& other);
    Vector3 cross(Vector3& other);
    Vector3 slerp(Vector3& other, double t);
    double sq_distance(Vector3& other);
    double magnitude();
    double sq_magnitude();
    Vector3 norm();
    Vector3 clamp(double min_val, double max_val);
    Vector3 clamp(Vector3& min_val, Vector3& max_val);
};

class IntVector3 {
public:
    int x, y, z;
    
    IntVector3(int x = 0, int y = 0, int z = 0);
    IntVector3 copy();
    int* get();
    IntVector3& set(int x, int y, int z);
    IntVector3& set_vector(IntVector3& other);
};

class Matrix4 {
public:
    double data[16];
    
    Matrix4();
    Matrix4& set_identity();
    Matrix4 copy();
    Matrix4& rotate(double angle, double x, double y, double z);
    Matrix4& translate(double x, double y, double z);
    Matrix4& orientation(double fx, double fy, double fz, double ux, double uy, double uz);
    Vector3 multiply_vector(Vector3& vector);
};

#endif // GLM_H
