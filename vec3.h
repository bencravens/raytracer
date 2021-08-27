#ifndef VEC3_H
#define VEC3_H

#include <cmath>
#include <iostream>

using std::sqrt;

//Defining the 3d vector class

class vec3 {
    public:
        //constructor to return default 3d-vec
        vec3() {
            e[0] = 0;
            e[1] = 0;
            e[2] = 0;
        }


        //return 3d vec with entries
        vec3(double e0, double e1, double e2) {
            e[0] = e0;
            e[1] = e1;
            e[2] = e2;
        }

        //grab co-ordinates

        double x() const {
            return e[0];
        }

        double y() const {
            return e[1];
        }

        double z() const {
            return e[2];
        }

        //use operator overloading for vector math
         
        //-(x,y,z) = (-x,-y,-z)
        vec3 operator-() const {
            return vec3(-e[0],-e[1],-e[2]);
        }

        //vector indexing to grab value
        double operator[](int i) const {
            return e[i];
        }

        //grab pointer to array entry
        double& operator[](int i) {
            return e[i];
        }

        //add a vector v to our vector e
        vec3& operator+=(const vec3 &v) {
            e[0] += v.e[0];
            e[1] += v.e[1];
            e[2] += v.e[2];
            return *this;
        }

        //multiply our vector by a constant
        vec3& operator*=(const double t) {
            e[0] *= t;
            e[1] *= t;
            e[2] *= t;
            return *this;
        }

        //R3 length of vector 
        double length () const {
            return sqrt(length_squared());
        }

        //squared length of vector
        double length_squared() const {
            return e[0]*e[0] + e[1]*e[1] + e[2]*e[2];
        }

    public:
        double e[3];
};

// Type aliases for vec3.
// There are different "types" of 3d vectors we have for the 
// purpose of this program.
using point3 = vec3; // a 3D point
using color = vec3;  // an RGB pixel

//Now we include some inline utility functions for the vec3 class
//An inline function is just a one-liner optimized by the compiler to have low overhead.
//A utility function in C++ is a private function included in the class header which 
//supports the execution of the public functions.

//send vector to specified output stream
inline std::ostream& operator<<(std::ostream &out, const vec3 &v) {
    return out << v.e[0] << ' ' << v.e[1] << ' ' << v.e[2];
}

//add two vectors
inline vec3 operator+(const vec3 &u, const vec3 &v) {
    return vec3(u.e[0] + v.e[0], u.e[1] + v.e[1], u.e[2] + v.e[2]);
}

//subtract a vector from another
inline vec3 operator-(const vec3 &u, const vec3 &v) {
    return vec3(u.e[0] - v.e[0], u.e[1] - v.e[1], u.e[2] - v.e[2]);
}

//elementwise multiplication
inline vec3 operator*(const vec3 &u, const vec3 &v) {
    return vec3(u.e[0] * v.e[0], u.e[1] * v.e[1], u.e[2] * v.e[2]);
}

//scalar multiplication, making a new vector
inline vec3 operator*(double t, const vec3 &v) {
    return vec3(t*v.e[0], t*v.e[1], t*v.e[2]);
}

//multiply the existing vector by t
inline vec3 operator*(const vec3 &v, double t) {
    return t * v;
}

// division
inline vec3 operator/(vec3 v, double t) {
    return (1/t) * v;
}

//dot product
inline double dot(const vec3 &u, const vec3 &v) {
    return u.e[0] * v.e[0]
        + u.e[1] * v.e[1]
        + u.e[2] * v.e[2];
}

//cross product
inline vec3 cross(const vec3 &u, const vec3 &v) {
    return vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1],
                u.e[2] * v.e[0] - u.e[0] * v.e[2],
                u.e[0] * v.e[1] - u.e[1] * v.e[0]);
}

//generate unit vector
inline vec3 unit_vector(vec3 v) {
    return v / v.length();
}

#endif
