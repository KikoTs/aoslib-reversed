#include "glm_c.h"
#include <cmath>
#include <algorithm>

// Vector3 implementation
Vector3::Vector3(double x, double y, double z) : x(x), y(y), z(z) {}

Vector3 Vector3::copy() {
    return Vector3(x, y, z);
}

double* Vector3::get() {
    static double result[3];
    result[0] = x;
    result[1] = y;
    result[2] = z;
    return result;
}

Vector3& Vector3::set(double x, double y, double z) {
    this->x = x;
    this->y = y;
    this->z = z;
    return *this;
}

Vector3& Vector3::set_vector(Vector3& other) {
    x = other.x;
    y = other.y;
    z = other.z;
    return *this;
}

Vector3 Vector3::translate(double dx, double dy, double dz) {
    return Vector3(x + dx, y + dy, z + dz);
}

double Vector3::distance(Vector3& other) {
    return sqrt(sq_distance(other));
}

double Vector3::dot(Vector3& other) {
    return x * other.x + y * other.y + z * other.z;
}

Vector3 Vector3::cross(Vector3& other) {
    return Vector3(
        y * other.z - z * other.y,
        z * other.x - x * other.z,
        x * other.y - y * other.x
    );
}

Vector3 Vector3::slerp(Vector3& other, double t) {
    double mag1 = magnitude();
    double mag2 = other.magnitude();
    
    if (mag1 == 0 || mag2 == 0) {
        return copy();
    }
    
    Vector3 v1(x / mag1, y / mag1, z / mag1);
    Vector3 v2(other.x / mag2, other.y / mag2, other.z / mag2);
    
    double dot_product = v1.dot(v2);
    
    if (dot_product > 1.0) {
        dot_product = 1.0;
    } else if (dot_product < -1.0) {
        dot_product = -1.0;
    }
    
    double theta = acos(dot_product);
    double sin_theta = sin(theta);
    
    double a, b;
    if (sin_theta < 0.001) {
        a = 1.0 - t;
        b = t;
    } else {
        a = sin((1.0 - t) * theta) / sin_theta;
        b = sin(t * theta) / sin_theta;
    }
    
    double resultX = a * x + b * other.x;
    double resultY = a * y + b * other.y;
    double resultZ = a * z + b * other.z;
    
    return Vector3(resultX, resultY, resultZ);
}

double Vector3::sq_distance(Vector3& other) {
    double dx = x - other.x;
    double dy = y - other.y;
    double dz = z - other.z;
    return dx * dx + dy * dy + dz * dz;
}

double Vector3::magnitude() {
    return sqrt(sq_magnitude());
}

double Vector3::sq_magnitude() {
    return x * x + y * y + z * z;
}

Vector3 Vector3::norm() {
    double mag = magnitude();
    if (mag > 0) {
        return Vector3(x / mag, y / mag, z / mag);
    }
    return Vector3(0, 0, 0);
}

Vector3 Vector3::clamp(double min_val, double max_val) {
    return Vector3(
        std::max(min_val, std::min(x, max_val)),
        std::max(min_val, std::min(y, max_val)),
        std::max(min_val, std::min(z, max_val))
    );
}

Vector3 Vector3::clamp(Vector3& min_val, Vector3& max_val) {
    return Vector3(
        std::max(min_val.x, std::min(x, max_val.x)),
        std::max(min_val.y, std::min(y, max_val.y)),
        std::max(min_val.z, std::min(z, max_val.z))
    );
}

// IntVector3 implementation
IntVector3::IntVector3(int x, int y, int z) : x(x), y(y), z(z) {}

IntVector3 IntVector3::copy() {
    return IntVector3(x, y, z);
}

int* IntVector3::get() {
    static int result[3];
    result[0] = x;
    result[1] = y;
    result[2] = z;
    return result;
}

IntVector3& IntVector3::set(int x, int y, int z) {
    this->x = x;
    this->y = y;
    this->z = z;
    return *this;
}

IntVector3& IntVector3::set_vector(IntVector3& other) {
    x = other.x;
    y = other.y;
    z = other.z;
    return *this;
}

// Matrix4 implementation
Matrix4::Matrix4() {
    set_identity();
}

Matrix4& Matrix4::set_identity() {
    for (int i = 0; i < 16; i++) {
        data[i] = 0.0;
    }
    
    // Set diagonal elements to 1
    data[0] = 1.0;  // [0,0]
    data[5] = 1.0;  // [1,1]
    data[10] = 1.0; // [2,2]
    data[15] = 1.0; // [3,3]
    
    return *this;
}

Matrix4 Matrix4::copy() {
    Matrix4 result;
    for (int i = 0; i < 16; i++) {
        result.data[i] = data[i];
    }
    return result;
}

Matrix4& Matrix4::rotate(double angle, double x, double y, double z) {
    double c = cos(angle);
    double s = sin(angle);
    double t = 1.0 - c;
    
    // Normalize the axis
    double length = sqrt(x*x + y*y + z*z);
    if (length > 0) {
        x /= length;
        y /= length;
        z /= length;
    }
    
    // Create rotation matrix
    Matrix4 rot;
    
    rot.data[0] = t * x * x + c;
    rot.data[1] = t * x * y - s * z;
    rot.data[2] = t * x * z + s * y;
    
    rot.data[4] = t * x * y + s * z;
    rot.data[5] = t * y * y + c;
    rot.data[6] = t * y * z - s * x;
    
    rot.data[8] = t * x * z - s * y;
    rot.data[9] = t * y * z + s * x;
    rot.data[10] = t * z * z + c;
    
    // Multiply this matrix by rotation matrix
    Matrix4 result;
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            result.data[i*4+j] = 0;
            for (int k = 0; k < 4; k++) {
                result.data[i*4+j] += data[i*4+k] * rot.data[k*4+j];
            }
        }
    }
    
    // Copy result back to this matrix
    for (int i = 0; i < 16; i++) {
        data[i] = result.data[i];
    }
    
    return *this;
}

Matrix4& Matrix4::translate(double x, double y, double z) {
    // Update the translation components of the matrix
    data[12] = x;
    data[13] = y;
    data[14] = z;
    
    return *this;
}

Matrix4& Matrix4::orientation(double fx, double fy, double fz, double ux, double uy, double uz) {
    // Normalize forward vector
    double f_length = sqrt(fx*fx + fy*fy + fz*fz);
    if (f_length > 0) {
        fx /= f_length;
        fy /= f_length;
        fz /= f_length;
    }
    
    // Calculate right vector as cross product of up and forward
    double rx = uy * fz - uz * fy;
    double ry = uz * fx - ux * fz;
    double rz = ux * fy - uy * fx;
    
    // Normalize right vector
    double r_length = sqrt(rx*rx + ry*ry + rz*rz);
    if (r_length > 0) {
        rx /= r_length;
        ry /= r_length;
        rz /= r_length;
    }
    
    // Recalculate up vector to ensure orthogonality
    double new_ux = fy * rz - fz * ry;
    double new_uy = fz * rx - fx * rz;
    double new_uz = fx * ry - fy * rx;
    
    // Set matrix values
    data[0] = rx;
    data[1] = new_ux;
    data[2] = fx;
    data[3] = 0.0;
    
    data[4] = ry;
    data[5] = new_uy;
    data[6] = fy;
    data[7] = 0.0;
    
    data[8] = rz;
    data[9] = new_uz;
    data[10] = fz;
    data[11] = 0.0;
    
    data[12] = 0.0;
    data[13] = 0.0;
    data[14] = 0.0;
    data[15] = 1.0;
    
    return *this;
}

Vector3 Matrix4::multiply_vector(Vector3& vector) {
    double x = vector.x * data[0] + vector.y * data[4] + vector.z * data[8] + data[12];
    double y = vector.x * data[1] + vector.y * data[5] + vector.z * data[9] + data[13];
    double z = vector.x * data[2] + vector.y * data[6] + vector.z * data[10] + data[14];
    double w = vector.x * data[3] + vector.y * data[7] + vector.z * data[11] + data[15];
    
    // If w is not 1, perform perspective division
    if (w != 1.0 && w != 0.0) {
        x /= w;
        y /= w;
        z /= w;
    }
    
    return Vector3(x, y, z);
}
