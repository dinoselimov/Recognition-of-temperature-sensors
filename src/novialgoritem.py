import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit
import math

def linear_model(upornosti, temperature):
    A = np.array([[1, upornosti[0]], [1, upornosti[1]], [1, upornosti[2]]])
    y = np.array([[temperature[0]], [temperature[1]], [temperature[2]]])
    
    # QR factorization of A
    Q, R = LA.qr(A)
    QT = np.transpose(Q)

    # Solving R(theta) = Q^T(y)
    theta = LA.solve(R, QT.dot(y))

    return theta

def quadratic_model(upornosti, temperature):
    A = np.array([[1, upornosti[0], upornosti[0]**2], [1, upornosti[1], upornosti[1]**2], [1, upornosti[2], upornosti[2]**2]])
    y = np.array([[temperature[0]], [temperature[1]], [temperature[2]]])
    
    # QR factorization of A
    Q, R = LA.qr(A)
    QT = np.transpose(Q)

    # Solving R(theta) = Q^T(y)
    theta = LA.solve(R, QT.dot(y))

    return theta
'''
def exponential_model(xi, yi):
    # Calculate exponential model parameters
    sumX = sum(np.log(xi))
    sumX2 = sum(np.log(xi) * np.log(xi))
    sumY = sum(np.log(yi))
    sumXY = sum(np.log(xi) * np.log(yi))

    print(sumX)
    print(sumX2)
    print(sumY)
    print(sumXY)
    n = len(xi)
    b = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX)
    A = (sumY - b * sumX) / n

    a = np.exp(A)

    return a, b
'''

def exponential_model(xi, yi):
    # Calculate exponential model parameters
    x_p = sum((yi)*(yi)*(xi))/sum((yi)*(yi))
    zi = np.log(yi)
    z_p = sum((yi)*(yi)*(zi))/sum((yi)*(yi))

    b = sum(yi*yi*zi*(xi-x_p)) / sum(yi*yi*xi*(xi-x_p))
    lna = z_p - b*x_p
    a = np.exp(lna)
    print(a)
    print(b)
    return a, b


x0 = 14066
x1 = 5000
x2 = 419
y0 = 2
y1 = 25
y2 = 99

x0 = 100
x1 = 108
x2 = 138
y0 = 2
y1 = 25
y2 = 99


# Sample data points
upornosti = np.array([x0, x1, x2])  # Replace with your xi values
temperature = np.array([y0, y1, y2])  # Replace with your yi values

lin_params = linear_model(upornosti, temperature)
# Fit the quadratic model
quad_params = quadratic_model(upornosti, temperature)
# Fit the exponential model
exp_a, exp_b = exponential_model(upornosti, temperature)
# Print the parameters for each model

print("Linear Model Parameters:", lin_params)
print("Quadratic Model Parameters:", quad_params)
print("Exponential Model Parameters: a =", exp_a, "b =", exp_b)

# Generate x values for plotting
x_fit = np.linspace(min(upornosti), max(upornosti), 100)
# Calculate corresponding y values using the models
lin_fit = lin_params[0] + lin_params[1]*x_fit
quad_y_fit = quad_params[0] + quad_params[1] * x_fit + quad_params[2] * x_fit**2
exp_y_fit = exp_a * np.exp(x_fit*exp_b)

# Plot the original data points and the fitted curves
plt.scatter(upornosti, temperature, label='Original Data')
plt.plot(x_fit, quad_y_fit, label='Quadratic Fit', color='blue')
plt.plot(x_fit, exp_y_fit, label='Exponential Fit', color='red')
plt.plot(x_fit, lin_fit, label='Linear Fit', color='black')  # Fixed the label
plt.xlabel('upornosti')
plt.ylabel('temperature')
plt.title('Curve Fitting')
plt.legend()
plt.show()

# ... (your existing code)

# Calculate the residuals for both models
quad_residuals = temperature - (quad_params[0] + quad_params[1] * upornosti + quad_params[2] * upornosti**2)
exp_residuals = temperature - (exp_a * np.power(upornosti, exp_b))
lin_residuals =  temperature - (lin_params[0] + lin_params[1] * upornosti)

print("Quad Residuals")
print(quad_residuals)
print("Exp Residuals")
print(exp_residuals)
print("Lin Residuals")
print(lin_residuals)
# Plot the residuals
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.scatter(upornosti, quad_residuals, label='Quadratic Residuals', color='blue')
plt.axhline(y=0, color='black', linestyle='--')
plt.xlabel('upornosti')
plt.ylabel('Residuals')
plt.title('Quadratic Fit Residuals')
plt.legend()

plt.subplot(2, 1, 2)
plt.scatter(upornosti, exp_residuals, label='Exponential Residuals', color='red')
plt.axhline(y=0, color='black', linestyle='--')
plt.xlabel('upornosti')
plt.ylabel('Residuals')
plt.title('Exponential Fit Residuals')
plt.legend()


plt.subplot(2, 1, 2)
plt.scatter(upornosti, exp_residuals, label='Linear Residuals', color='black')
plt.axhline(y=0, color='black', linestyle='--')
plt.xlabel('upornosti')
plt.ylabel('Residuals')
plt.title('Linear Fit Residuals')
plt.legend()
plt.tight_layout()
plt.show()

def rmse(actual, predicted):
    return np.sqrt(np.mean((actual - predicted)**2))

# Calculate RMSE for each model
quad_rmse = rmse(temperature, quad_y_fit[temperature])
exp_rmse = rmse(temperature, exp_y_fit[temperature])
lin_rmse = rmse(temperature, lin_fit[temperature])

print("Quadratic Fit RMSE:", quad_rmse)
print("Exponential Fit RMSE:", exp_rmse)
print("Linear Fit RMSE:", lin_rmse)



#temperatura_1 = 
def recognizeInstrument(upornost, temperatura):
    # Fit the models to the data

    thermistor_params, _ = curve_fit(exponential_model, temperatura, upornost)
    pt_params, _ = curve_fit(exponential_model, temperatura, upornost)

    # Print the parameters for each model
    print("Thermistor Parameters:", thermistor_params)
    print("PT Parameters:", pt_params)

    # Compare the parameters to differentiate between the sensor types
    if thermistor_params[1] < pt_params[1]:
        print("It's likely a thermistor.")
    else:
        print("It's likely a PT sensor.")
    sensor_type = ""

    min_deff = min(pt100_diff, pt1000_diff, th5k_diff, th10k_diff)
    if min_deff == pt100_diff:
        print("PT100")
        sensor_type = "PT100"
    elif min_deff == pt1000_diff:
        print("PT1000")
        sensor_type = "PT1000"
    elif min_deff == th5k_diff:
        print("TH5K")
        sensor_type = "TH5K"
    elif min_deff == th10k_diff:
        print("TH10K")
        sensor_type = "TH10K"

    return sensor_type