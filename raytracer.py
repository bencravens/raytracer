import numpy as np    
import math

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
function to write a single pixel's color to the standard
output stream.
"""
def write_color(pixel_color):
    ix = int(255.999 * x(pixel_color))
    iy = int(255.999 * y(pixel_color))
    iz = int(255.999 * z(pixel_color))
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

    #world
    world = hittable_list()
    sp1 = sphere(np.array([0,0,-1]),0.5)
    world.add(sp1)
    sp2 = sphere(np.array([0,-100.5,-1]),100)
    world.add(sp2)

    #camera
    viewport_height = 2.0
    viewport_width = aspect_ratio * viewport_height
    focal_length = 1.0
    
    origin = np.array([0,0,0])
    horizontal = np.array([viewport_width,0,0])
    vertical = np.array([0,viewport_height,0])
    lower_left_corner = origin - horizontal/2 - vertical/2 - np.array([0,0,focal_length])

    #render
    print("P3\n{} {}\n255\n".format(image_width,image_height))

    for i in reversed(range(image_height)):
        for j in range(image_width):
            u = j / (image_width-1)
            v = i / (image_height-1)
            r = ray(origin,lower_left_corner + u*horizontal + v*vertical - origin)
            pixel_color = ray_color(r, world)
            write_color(pixel_color)

if __name__=="__main__":
    rt_main()
