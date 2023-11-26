import numpy as np

# Given data
sensor_values = {
    'PT1000': {'PT1000': 24.86, 'PT100': 811.53, 'TH5K': 3479.59, 'TH10K': 1546.26},
    'PT100': {'PT1000': 8398.10, 'PT100': 82.45, 'TH5K': 41523.97, 'TH10K': 19496.36},
    'TH5K': {'PT1000': 74.67, 'PT100': 95.84, 'TH5K': 50.11, 'TH10K': 17.30},
    'TH10K': {'PT1000': 83.66, 'PT100': 99.30, 'TH5K': 16.95, 'TH10K': 37.50}
}

# Extract values of recognized sensor
recognized_sensor = 'PT1000'
recognized_values = np.array(list(sensor_values[recognized_sensor].values()))

# Calculate differences for recognized sensor against all other sensors in its array
differences = {}
for other_sensor, other_values in sensor_values[recognized_sensor].items():
    if other_sensor != recognized_sensor:
        difference = np.abs(recognized_values - other_values)
        differences[other_sensor] = difference

# Print differences
for other_sensor, difference in differences.items():
    print(f'Difference to {other_sensor}: {difference}')
