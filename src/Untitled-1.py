import numpy as np
import matplotlib.pyplot as plt


#x = np.array([0.165, 0.407, 0.562, 0.597, 0.622, 0.656, 0.694, 0.759, 0.816, 0.870, 0.929, 0.974, 1.011, 1.048, 1.075, 1.103, 1.137, 1.177, 1.242, 1.250, 1.266, 1.303, 1.326, 1.390, 1.405, 1.456, 1.520, 1.543, 1.600, 1.606, 1.640, 1.675, 1.702, 1.738, 1.796, 1.833, 1.860, 1.910, 2.029, 2.094, 2.107, 2.128, 2.855, 2.894, 2.945])
#y = np.array([0.287, 0.540, 0.693, 0.730, 0.760, 0.788, 0.828, 0.897, 0.955, 1.006, 1.062, 1.106, 1.148, 1.183, 1.211, 1.241, 1.273, 1.315, 1.380, 1.389, 1.400, 1.442, 1.466, 1.530, 1.541, 1.595, 1.661, 1.684, 1.740, 1.745, 1.783, 1.817, 1.846, 1.886, 1.941, 1.982, 2.009, 2.058, 2.176, 2.236, 2.250, 2.272, 2.889, 2.914, 2.945])


x = np.array([0.165, 0.407, 0.427, 0.475, 0.515, 0.562, 0.597, 0.622, 0.656, 0.694, 0.759, 0.816, 0.870, 0.929, 0.974, 1.011, 1.048, 1.075, 1.103, 1.137, 1.177, 1.242, 1.250, 1.266, 1.303, 1.326, 1.390, 1.405, 1.456, 1.520, 1.543, 1.600, 1.606, 1.640, 1.675, 1.702, 1.738, 1.796, 1.833, 1.860, 1.910, 2.029, 2.094, 2.107, 2.128, 2.855, 2.894, 2.915, 2.945])
y = np.array([0.287, 0.540, 0.557, 0.606, 0.645, 0.693, 0.730, 0.760, 0.788, 0.828, 0.897, 0.955, 1.006, 1.062, 1.106, 1.148, 1.183, 1.211, 1.241, 1.273, 1.315, 1.380, 1.389, 1.400, 1.442, 1.466, 1.530, 1.541, 1.595, 1.661, 1.684, 1.740, 1.745, 1.783, 1.817, 1.846, 1.886, 1.941, 1.982, 2.009, 2.058, 2.176, 2.236, 2.250, 2.272, 2.889, 2.914, 2.930, 2.945])
# Degree of the polynomial 0.693     2.855, 2.894, 2.915, 2.945
# Degree of the polynomial 0.693     2.889, 2.914, 2.930, 2.945

x_precise = np.array([2.821, 2.834, 2.837, 2.849, 2.855, 2.880, 2.894, 2.901, 2.913, 2.915, 2.942, 2.945, 2.949])
y_precise = np.array([2.878, 2.880, 2.881, 2.885, 2.889, 2.906, 2.914, 2.919, 2.927, 2.930, 2.936, 2.945, 2.948])
degree = 4
# Perform polynomial regression
coeffs = np.polyfit(x, y, degree)
# Create a polynomial function using the fitted coefficients
polynomial = np.poly1d(coeffs)

# Generate x values for the fitted curve
x_fit = np.linspace(min(x), max(x), 100)

# Calculate corresponding y values using the polynomial function
y_fit = polynomial(x_fit)

# Plot the original data points and the fitted curve
plt.scatter(x, y, label='Original Data')
plt.plot(x_fit, y_fit, label='Fitted Curve', color='red')

# Display the polynomial equation
equation = np.poly1d(coeffs)
equation_str = equation.__str__().replace('\n', '').replace('*', ' * ').replace(' + ', ' +\n').replace(' - ', ' -\n')
plt.text(1, 2, f'Equation:\n{equation_str}', fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

plt.xlabel('x')
plt.ylabel('y')
plt.title('Curve Fitting')
plt.legend()
plt.show()

print("Coefficients:", coeffs)
print("Equation:", equation)



