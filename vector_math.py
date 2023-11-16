from collections import namedtuple
import numpy as np 

# Spherical R^3 Vector
sphVec3 = namedtuple('sphVec3', ['r', 'theta', 'phi'])

# Cartesian R^3 Vector
cartVec3 = namedtuple('cartVec3', ['x', 'y', 'z'])

# convert spherical to cartesian vector 
def sph_to_cart(point: sphVec3):
    x = point.r * np.sin(point.phi) * np.cos(point.theta)
    y = point.r * np.sin(point.phi) * np.sin(point.theta)
    z = point.r * np.cos(point.phi)
    return cartVec3(x, y, z)

# convert cartesian to spherical vector 
def cart_to_sph(point: cartVec3):
    x, y, z, = point.x, point.y, point.z 
    r = np.sqrt((x * x) + (y * y) + (z * z))
    if x == 0:
        theta = np.pi/2
    else:
        theta = np.arctan(y/x)
    phi = np.arccos(z/r)
    return sphVec3(r, theta, phi)

# subtract cartesian vectors (pt2 - pt1)
def sub_cart_vec(pt1: cartVec3, pt2: cartVec3):
    return cartVec3(pt2.x - pt1.x, pt2.y - pt1.y, pt2.z - pt1.z)

# add cartesian vectors (pt1 + pt2)
def add_cart_vec(pt1: cartVec3, pt2: cartVec3):
    return cartVec3(pt1.x + pt2.x, pt1.y + pt2.y, pt1.z + pt2.z)

def normalize(pt: cartVec3):
    length = magnitude(pt)
    if length == 0:
        raise ZeroDivisionError('length was equal to 0, cannot divide to normalize')
    return cartVec3(pt.x / length, pt.y / length, pt.z / length)

def magnitude(pt: cartVec3):
    return np.sqrt((pt.x ** 2) + (pt.y ** 2) + (pt.z ** 2))

def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

def cross(first, other) -> 'vecC3':
    x = (first.y * other.z) - (first.z * other.y)
    y = (first.z * other.x) - (first.x * other.z)
    z = (first.x * other.y) - (first.y * other.x)
    return cartVec3(x, y, z)


class vecC3: # cartesian vector
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.mag = np.sqrt((x**2) + (y**2) + (z**2))
    
    def __str__(self):
        return f'<{self.x}, {self.y}, {self.z}>'
    
    def __add__(self, other):
        return vecC3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return vecC3(self.x - other.x, self.y - other.y, self.z - other.z)

    def normalize(self) -> 'vecC3':
        return vecC3(self.x/self.mag, self.y/self.mag, self.z/self.mag)

    def convert_sph(self) -> 'vecS3':
        x, y, z, = self.x, self.y, self.z 
        r = np.sqrt((x * x) + (y * y) + (z * z))
        if x == 0:
            theta = np.pi/2
        else:
            theta = np.arctan(y/x)
        phi = np.arccos(z/r)
        return vecS3(r, theta, phi)
    
    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other) -> 'vecC3':
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return vecC3(x, y, z)

    
class vecS3: # spherical vector 
    def __init__(self, r, theta, phi):
        self.r, self.theta, self.phi = r, theta, phi

    def convert_cart(self) -> 'vecC3':
        x = self.r * np.sin(self.phi) * np.cos(self.theta)
        y = self.r * np.sin(self.phi) * np.sin(self.theta)
        z = self.r * np.cos(self.phi)
        return vecS3(x, y, z)



