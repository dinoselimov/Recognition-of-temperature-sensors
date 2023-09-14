import numpy as np
import matplotlib.pyplot as plt
# Define the data
v_meter = [0, 0.178, 0.374, 0.636, 0.834, 1.062, 1.198, 1.462, 1.681, 1.863, 2.037, 2.238, 2.424, 2.657, 2.822, 3.075, 3.288]
esp = [0, 0.06, 0.24, 0.51, 0.71, 0.93, 1.07, 1.34, 1.55, 1.72, 1.9, 2.1, 2.29, 2.56, 2.8, 3.25, 3.3]

# Calculate differences
differences = np.array(esp) - np.array(v_meter)

# Calculate errors (absolute differences)
errors = np.abs(differences)

# Calculate statistics
average_error = np.mean(errors)
max_error = np.max(errors)
min_error = np.min(errors)

print("Differences:", differences)
print("Errors:", errors)
print("Average Error:", average_error)
print("Max Error:", max_error)
print("Min Error:", min_error)


# Plot errors
plt.plot(errors, marker='o')
plt.xlabel('Data Point')
plt.ylabel('Error')
plt.title('Errors between v-meter and esp')
plt.grid(True)
plt.show()