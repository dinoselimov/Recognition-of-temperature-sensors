import numpy as np
import matplotlib.pyplot as plt

x = np.array([1.41, 2.949, 0.340, 0.125, 1.24, 2.10, 1.605, 2.82, 1.256, 1.98, 1.460, 2.837])
y = np.array([1.560, 2.948, 0.468, 0.250, 1.378, 2.222, 1.743, 2.88, 1.393, 2.133, 1.615, 2.881])



x = np.array([0.165, 0.407, 0.694, 0.929, 1.177, 1.242, 1.303, 1.326, 1.405, 1.456, 1.606, 2.107, 2.855, 2.880, 2.901, 2.945])
y = np.array([0.287, 0.540, 0.828, 1.062, 1.315, 1.380, 1.442, 1.466, 1.541, 1.595, 1.745, 2.250, 2.889, 2.906, 2.919, 2.945])

# Degree of the polynomial
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



