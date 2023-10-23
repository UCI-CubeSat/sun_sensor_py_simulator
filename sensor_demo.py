import numpy as np
import matplotlib.pyplot as plt


width = 10.0  # Width of the quad photodiode (assumed square for simplicity (changing this later))
num_pixels = 4  # num_photodiodes 
pixel_size = width / num_pixels  # Size of each photodiode element
incident_angle_rad = np.radians(float(input("Incident Angle in Deg: ")))

# Photodiode positions (gotta work this out a bit more)
x_positions = np.linspace(-width / 2, width / 2, num_pixels)
y_positions = np.linspace(-width / 2, width / 2, num_pixels)


responses = np.zeros((num_pixels, num_pixels))

# response of each diode to incident angle 
for i in range(num_pixels):
    for j in range(num_pixels):
        x_pixel = x_positions[i]
        y_pixel = y_positions[j]
        
        angle_to_normal_rad = np.arctan2(y_pixel, x_pixel)
        
        response = np.cos(incident_angle_rad - angle_to_normal_rad)
        responses[i, j] = response

# display 
plt.imshow(responses, cmap='viridis', extent=(-width / 2, width / 2, -width / 2, width / 2))
plt.xlabel('X Position (mm)')
plt.ylabel('Y Position (mm)')
plt.title(f'Quad Photodiode When Incident Angle is: {round(np.degrees(incident_angle_rad), 3)} degrees')
plt.colorbar(label='Response')
plt.show()
