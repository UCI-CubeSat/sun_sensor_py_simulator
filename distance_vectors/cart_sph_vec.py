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



