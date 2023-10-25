import numpy as np
import matplotlib.pyplot as plt
import json 


width = 10.0  # Width of the quad photodiode (assumed square for simplicity (changing this later))
num_pixels = 4  # num_photodiodes 
pixel_size = width / num_pixels  # Size of each photodiode element
elevation_angle_deg = (float(input("elevation Angle in Deg: ")))
elevation_angle_rad = np.radians(elevation_angle_deg)

data: dict = {}

# Photodiode positions (gotta work this out a bit more)
x_positions = np.linspace(-width / 2, width / 2, num_pixels)
#print(x_positions)
y_positions = np.linspace(-width / 2, width / 2, num_pixels)

responses = np.zeros((num_pixels, num_pixels))
#print(responses)

# response of each diode to elevation angle 
for i in range(num_pixels):
    for j in range(num_pixels):
        x_pixel = x_positions[i]
        y_pixel = y_positions[j]
        
        angle_to_normal_rad = np.arctan2(y_pixel, x_pixel)
        print(f'({x_pixel}, {y_pixel}), norm: {np.degrees(angle_to_normal_rad)}')
        
        response = np.cos(elevation_angle_rad - angle_to_normal_rad)
        pos = {'norm': np.degrees(angle_to_normal_rad), 'response': np.degrees(response)}
        data.update({f'({i}, {j})':pos})
        responses[i, j] = response

# display and save data
with open(f'details_{elevation_angle_deg}.json','w') as f:
    f.write(json.dumps(data, indent=4))


plt.imshow(responses, cmap='plasma', extent=(-width / 2, width / 2, -width / 2, width / 2))
plt.xlabel('X Position (mm)')
plt.ylabel('Y Position (mm)')
plt.title(f'Quad Photodiode When elevation Angle is: {round(np.degrees(elevation_angle_rad), 3)} degrees')
plt.colorbar(label='Response')
plt.show()
