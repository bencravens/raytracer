import numpy as np    
import sys
import math
import random

"""
3d array utility functions   
"""
def x(vec3):
    return vec3[0]

def y(vec3):
    return vec3[1]

def z(vec3):
    return vec3[2]      

def output(vec3):
    return "{} {} {}".format(vec3[0],vec3[1],vec3[2])

def length_squared(vec3):
    return np.dot(vec3,vec3)

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

"""
misc utility functions
"""
def clamp(x, minval, maxval):
    if (x < minval):
        return minval
    if (x > maxval):
        return maxval
    return x

"""
function to write a single pixel's color to the standard
output stream (after taking multiple samples)
"""
def write_color(pixel_color, samples_per_pixel):
    r = x(pixel_color)
    g = y(pixel_color)
    b = z(pixel_color)

    #normalize by number of samples per pixel
    scale = 1.0 / (samples_per_pixel)
    r *= scale
    g *= scale
    b *= scale

    ix = int(256 * clamp(r, 0.0, 0.999))
    iy = int(256 * clamp(g, 0.0, 0.999))
    iz = int(256 * clamp(b, 0.0, 0.999))
    print("{} {} {}\n".format(ix,iy,iz))

"""
Class representing a ray
with a getter 
function to generate the light ray 
P(O,t,b) = O + t*b
O = origin (x,y,z)
t = length of ray (scalar)
b = direction of ray (x^,y^,z^)
"""
class ray:

    def __init__(self,O,b,t=1.0):
        self.O = O
        self.b = b
        self.t = t
        self.p = self.O + self.t*self.b

"""
struct like class to store
a record of points that have been hit, 
surface normals and the corresponding
t's.
"""

class hit_record:
    def __init__(self,p=np.array([0.0,0.0,0.0]),normal=np.array([0.0,0.0,0.0]),t=1.0):
        self.p = p
        self.normal = normal
        self.t = t
    
    #is the incident ray coming inside the sphere,
    #or leaving it?
    def set_face_normal(self,r,outward_normal):
        if (np.dot(r.b, outward_normal) > 0):
            #ray is inside the sphere
            self.normal = -outward_normal
            self.front_face = false
        else:
            #ray outside the sphere
            self.normal = outward_normal
            self.front_face = True
 
"""
a class representing a hittable object 
we are firing light rays at
"""
class hittable:
    def __init__(self,r,t_min,t_max,rec):
        self.r = r
        self.t_min = t_min
        self.t_max = t_max
        self.rec = rec
        self.is_hit = False

"""
camera class
"""
class camera:
        
    def __init__(self):
        #camera
        self.aspect_ratio = 16 / 9
        self.viewport_height = 2.0
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.focal_length = 1.0
        
        self.origin = np.array([0,0,0])
        self.horizontal = np.array([self.viewport_width,0.0,0.0])
        self.vertical = np.array([0.0,self.viewport_height,0.0])
        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - np.array([0,0,self.focal_length])
    
    def get_ray(self,u,v):
        return ray(self.origin, self.lower_left_corner + u*self.horizontal + v*self.vertical - self.origin)


"""
class to store a list of 
hittable objects in the scene
"""
class hittable_list:
    def __init__(self):
        self.objects = []
    def add(self,obj):
        self.objects.append(obj)
    def list_is_hit(self,r, t_min, t_max, rec):
        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = t_max

        #find the object the ray hits first
        for obj in self.objects:
            if obj.sphere_is_hit(r,t_min,closest_so_far,temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
        return hit_anything

"""
class sphere which subclasses/
extends hittable
"""
class sphere(hittable):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    def sphere_is_hit(self,r,t_min,t_max,rec):
        oc = r.O - self.center
        a = length_squared(r.b)
        half_b = np.dot(oc,r.b)
        c = length_squared(oc) - self.radius**2
        discriminant = half_b*half_b - a*c
        
        if (discriminant < 0):
            return False
        
        sqrtd = np.sqrt(discriminant)
        
        #find the nearest root that lies in the acceptable range
        root = (-half_b - sqrtd) / a
        if (root < t_min or t_max < root):
            root = (-half_b + sqrtd) / a
            if (root < t_min or t_max < root):
                return False
        
        rec.t = root
        myray = ray(r.O,r.b,rec.t)
        rec.p = myray.p
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        return True

"""
generate a background color for the scene
based on a big sphere and then a gradient
for a blue sky
"""
def ray_color(r, world):
    myrec = hit_record()
    is_hit = world.list_is_hit(r,0,np.inf,myrec)
    if (is_hit):
        return 0.5 * (myrec.normal + np.array([1,1,1]))
    unit_direction = normalize(r.b)
    t = 0.5*(y(unit_direction) + 1.0)
    result = (1.0-t)*np.array([1.0,1.0,1.0]) + t*np.array([0.5,0.7,1.0])
    return result

"""
run the raytracer
"""
def rt_main():
    #image
    aspect_ratio = 16 / 9
    image_width = 400
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 10
    
    #world
    world = hittable_list()
    sp1 = sphere(np.array([0,0,-1]),0.5)
    world.add(sp1)
    sp2 = sphere(np.array([0,-100.5,-1]),100)
    world.add(sp2)

    #camera object
    cam = camera()

    #render
    print("P3\n{} {}\n255\n".format(image_width,image_height))

    for i in reversed(range(image_height)):
        for j in range(image_width):
            pixel_color = np.array([0.0,0.0,0.0])
            for s in range(samples_per_pixel):
                u = (j+random.uniform(0,1)) / (image_width-1)
                v = (i+random.uniform(0,1)) / (image_height-1)
                r = cam.get_ray(u,v)
                pixel_color = ray_color(r, world) + pixel_color
            write_color(pixel_color,samples_per_pixel)

if __name__=="__main__":
    rt_main()
