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



class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w

        return Quaternion(w, x, y, z)

    def inverse(self):
        norm_sq = self.w**2 + self.x**2 + self.y**2 + self.z**2
        if norm_sq == 0:
            return Quaternion(0, 0, 0, 0)
        inv_norm_sq = 1.0 / norm_sq
        return Quaternion(self.w * inv_norm_sq, -self.x * inv_norm_sq, -self.y * inv_norm_sq, -self.z * inv_norm_sq)

    def rotate_point(self, point):
        # Convert the point to a quaternion
        p = Quaternion(0, point[0], point[1], point[2])

        # Apply the quaternion rotation
        rotated_point = (self * p * self.inverse()).as_tuple()
        rotated_point = (rotated_point[1], rotated_point[2], rotated_point[3])

        return rotated_point

    def as_tuple(self):
        return (self.w, self.x, self.y, self.z)

    def __str__(self):
        return f"{self.w} + {self.x}i + {self.y}j + {self.z}k"


# test_sat = cartVec3(1, 0, 0)
# test_sun = sub_cart_vec(test_sat, cartVec3(3, 0, 0))
# print(f'test sat, sun {test_sat, test_sun}')

# check = add_cart_vec(test_sat, test_sun)
# print(f'Check: {check.x, check.y, check.z}')

# sph_sat = cart_to_sph(test_sat)
# sph_sun = cart_to_sph(test_sun)
# print(f'sph Sat, Sun: {sph_sat, sph_sun}')

# cart_sat = sph_to_cart(sph_sat)
# cart_sun = sph_to_cart(sph_sun)
# print(f'cart sat, sun {cart_sat, cart_sun}')

# sun_earth = add_cart_vec(cart_sat, cart_sun)
# print(f'sun-earth cart: {sun_earth}')

# print(f'sun-earth sph: {cart_to_sph(sun_earth)}')



