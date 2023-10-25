import numpy as np
import matplotlib.pyplot as plt

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
height = 0.01

# TODO fix this calculation as it should be function of height and 'r' according to the slides
# however the meaning of 'r' is unclear to me at this time 
## CURRENTLY CUSTOMIZABLE FOV VALUE FOR THE FILTER 
fov_degrees = 90 # degrees

# learned that spreads like this can be modeled as a normal distribution expanded to 2D 
# We can use the FOV value as a standard deviation, allowing us to see how much the 
# sun sensor readings expand when given a larger FOV. 
st_dev = np.radians(fov_degrees)
# peak intensity is right now just a variable we defined for the center 
solar_intensity_at_location = peak_intensity * np.exp(-(x_grid - x)**2 / (2 * st_dev**2) - (y_grid - y)**2 / (2 * st_dev**2))

# Calculate the FOV filter based on the specified FOV and height (stackoverflow helped me with the numpy on this one but hopefully this makes sense)
fov_filter = np.abs(np.degrees(np.arctan2(height, np.sqrt((x_grid - x)**2 + (y_grid - y)**2))) <= (fov_degrees / 2))

#TODO PROPERLY CALCULATE AZIMUTH ANGLE (right now i have it set to just calculate based on a given (x, y), but that needs to be changed)
# (obviously, the real sensor wont know the x, y values beforehand, so this should be calculated via the FOV spread)
angle_with_x_axis = np.arctan2(y, x)
azimuth = (90 - np.degrees(angle_with_x_axis)) % 360
print(f'Estimated azimuth angle of the heat source within {fov_degrees} degrees FOV at a height of {height} mm: {azimuth} degrees')


# visualize data 
plt.figure()
plt.imshow(solar_intensity_at_location, cmap='hot', extent=(-sensor_width / 2, sensor_width / 2, -sensor_width / 2, sensor_width / 2))
plt.xlabel('X Position (mm)')
plt.ylabel('Y Position (mm)')
plt.title(f'Solar Intensity at ({x}, {y}) mm in Sensor Frame with {fov_degrees} degrees FOV at Height {height} mm')
plt.colorbar(label='Solar Intensity')
plt.show()


## PLS READ
# only use x and y values in the ranges -4, 4, since anything more will give odd results at the moment as they are 
# out of the frame of the sensor
