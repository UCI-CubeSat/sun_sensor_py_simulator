import numpy as np
import matplotlib.pyplot as plt
import vector_math as vm
from utils import Quaternion
from mpl_toolkits.mplot3d.art3d import Poly3DCollection 

# constants
sensor_width = 10.0  
num_pixels = 8  
pixel_size = sensor_width / num_pixels  
peak_intensity = 0.01  # chatgpt told me to do this 


# create grid of x, y coords for the sensor 
x_coords = np.linspace(-sensor_width / 2, sensor_width / 2, num_pixels)
y_coords = np.linspace(-sensor_width / 2, sensor_width / 2, num_pixels)
x_grid, y_grid = np.meshgrid(x_coords, y_coords)

# get x y from user 
x = float(input("Enter the x-coordinate (mm) in the sensor frame: "))
y = float(input("Enter the y-coordinate (mm) in the sensor frame: "))

## CUSTOMIZABLE HEIGHT VALUE FOR THE FILTER 
height = 1

# TODO fix this calculation as it should be function of height and 'r' according to the slides
# however the meaning of 'r' is unclear to me at this time 
## CURRENTLY CUSTOMIZABLE FOV VALUE FOR THE FILTER 
fov_degrees = 80 # degrees

# learned that spreads like this can be modeled as a normal distribution expanded to 2D 
# We can use the FOV value as a standard deviation, allowing us to see how much the 
# sun sensor readings expand when given a larger FOV. 
st_dev = np.radians(fov_degrees)
# peak intensity is right now just a variable we defined for the center 
solar_intensity_at_location = peak_intensity * np.exp(-(x_grid - x)**2 / (2 * st_dev**2) - (y_grid - y)**2 / (2 * st_dev**2))

# Calculate the FOV filter based on the specified FOV and height (stackoverflow helped me with the numpy on this one but hopefully this makes sense)
fov_filter = np.abs(np.degrees(np.arctan2(height, np.sqrt((x_grid - x)**2 + (y_grid - y)**2))) <= (fov_degrees / 2))

# calculate azimuth 
angle_with_x_axis = np.degrees(np.arctan2(y, x))
if angle_with_x_axis < 0:
    azimuth = np.radians(angle_with_x_axis + 180)
else:
    azimuth = np.radians(angle_with_x_axis + 180)
#TODO change 1.0 to smth else once we figure out intensities

# get satellite to sun distance vector in spherical coordinates 
sat_to_sun = vm.sphVec3(1.0, azimuth, np.arccos(height/np.sqrt(x**2 + y**2 + height**2)))

# get the satellites relative position to earth in spherical coordinates 
sat_pos = vm.cart_to_sph(vm.cartVec3(1, 1, 1))

dist_sat_to_sun = vm.sph_to_cart(sat_to_sun) # s
dist_earth_to_sat = vm.sph_to_cart(sat_pos)
total_dist_cart = vm.add_cart_vec(dist_earth_to_sat, dist_sat_to_sun)

print(f'Spherical Vector (Satellite to Sun): {(spoint := sat_to_sun).r, np.degrees(spoint.theta), np.degrees(spoint.phi)}')
print(f'Cartesian Vector (Satellite to Sun): {(point := vm.sph_to_cart(sat_to_sun)).x, point.y, point.z}')
print(f'Estimated azimuth angle of the heat source within {fov_degrees} degrees FOV at a height of {height} mm: {azimuth} degrees')

current_orientation = vm.cartVec3(0, 1, 0) # b
rotation_axis = vm.cross(current_orientation, dist_sat_to_sun)
rot_angle = np.arccos(vm.dot(current_orientation,rotation_axis)/(vm.magnitude(current_orientation) * vm.magnitude(dist_sat_to_sun)))

QuaternionY = Quaternion(
    1, 
    0, 
    1, 
    0
)
QuaternionRotation = Quaternion(
    np.cos(rot_angle/2), 
    (sin:=np.sin(rot_angle/2))*rotation_axis.x, 
    sin*rotation_axis.y,
    sin*rotation_axis.z)

print(QuaternionRotation)

# QuaternionY = Quaternion(
#     np.cos((np.radians(90-np.degrees(spoint.phi)))/2), 
#     (sin:=np.sin((np.radians(90-np.degrees(spoint.phi)))/2))*0, 
#     sin*1, 
#     sin*0)
# QuaternionZ = Quaternion(
#     np.cos(np.degrees(np.radians(spoint.theta)/2)), 
#     (sin:=np.sin(np.radians(np.degrees(spoint.theta))/2))*0,
#     sin*0, 
#     sin*1)

def generate_cube_vertices(side_length):
    half_length = side_length / 2
    vertices = np.array([
        [-half_length, -half_length, -half_length],
        [half_length, -half_length, -half_length],
        [half_length, half_length, -half_length],
        [-half_length, half_length, -half_length],
        [-half_length, -half_length, half_length],
        [half_length, -half_length, half_length],
        [half_length, half_length, half_length],
        [-half_length, half_length, half_length]
    ])
    return vertices

fig = plt.figure(2)
ax = fig.add_subplot(111, projection='3d')

# Define the initial cube vertices
side_length = 2.0
cube_vertices = generate_cube_vertices(side_length)
rotated_vertices = [QuaternionY.rotate_point(vertex) for vertex in cube_vertices]
rotated_vertices = [QuaternionRotation.rotate_point(vertex) for vertex in cube_vertices]
#rotated_vertices = [QuaternionY.rotate_point(vertex) for vertex in rotated_vertices]
#rotated_vertices = [QuaternionZ.rotate_point(vertex) for vertex in rotated_vertices]

# Plot the rotated cube
rotated_vertices = np.array(rotated_vertices)
ax.scatter(rotated_vertices[:, 0], rotated_vertices[:, 1], rotated_vertices[:, 2])

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

colors = ['r', 'g', 'b', 'c', 'm', 'y']
cube_faces = [
    [rotated_vertices[0], rotated_vertices[1], rotated_vertices[2], rotated_vertices[3], colors[0]],
    [rotated_vertices[4], rotated_vertices[5], rotated_vertices[6], rotated_vertices[7], colors[1]],
    [rotated_vertices[0], rotated_vertices[4], rotated_vertices[7], rotated_vertices[3], colors[2]],
    [rotated_vertices[1], rotated_vertices[5], rotated_vertices[6], rotated_vertices[2], colors[3]],
    [rotated_vertices[0], rotated_vertices[1], rotated_vertices[5], rotated_vertices[4], colors[4]],
    [rotated_vertices[3], rotated_vertices[2], rotated_vertices[6], rotated_vertices[7], colors[5]]
]

# Plot the rotated cube faces
for face in cube_faces:
    vertices = face[:-1]
    color = face[-1]
    vertices = np.array(vertices)
    ax.add_collection3d(Poly3DCollection([vertices], alpha=0.25, facecolor=color))

ax.quiver(0, 0, 0, 2*point.x, 2*point.y, 2*point.z, color='r', label='Sat to Sun')

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title(f'{np.degrees(spoint.theta)}* Azimuth, {np.degrees(spoint.phi)}* Elevation CubeSat')


# # visualize data 
plt.figure(1)
plt.imshow(solar_intensity_at_location, cmap='hot', extent=(-sensor_width / 2, sensor_width / 2, -sensor_width / 2, sensor_width / 2), origin='lower')
plt.xlabel('X Position (mm)')
plt.ylabel('Y Position (mm)')
plt.title(f'Solar Intensity at ({x}, {y}) mm in Sensor Frame with {fov_degrees} degrees FOV at Height {height} mm')
plt.colorbar(label='Solar Intensity')
plt.show()


## PLS READ
# only use x and y values in the ranges -4, 4, since anything more will give odd results at the moment as they are 
# out of the frame of the sensor
