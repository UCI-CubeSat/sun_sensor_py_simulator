import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cart_sph_vec as csv 
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

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

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the initial cube vertices
side_length = 2.0
cube_vertices = generate_cube_vertices(side_length)
elev_axis = csv.Quaternion(0.9238795325112867, 0.2705980500730985, 0.2705980500730985, 0.0)
azi_axis = csv.Quaternion(0.9238795325112867, 0.0, 0.2209423826903945, 0.3124597141037825)
rotated_vertices = [elev_axis.rotate_point(vertex) for vertex in cube_vertices]
rotated_vertices = [azi_axis.rotate_point(vertex) for vertex in rotated_vertices]

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


# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('45 Degree Elevation CubeSat')

plt.show()