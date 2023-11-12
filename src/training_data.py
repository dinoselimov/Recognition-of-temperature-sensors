import numpy as np
import matplotlib.pyplot as plt

def fit_linear_model(data):
    # Extracting x and y values from the data
    x = np.array([item[0] for item in data])
    y = np.array([item[1] for item in data])

    # Formulate the Objective Function for a Linear Model (y = mx + b)
    X = np.vstack([np.ones_like(x), x]).T

    # Compute Coefficients using the least squares method
    coefficients = np.linalg.inv(X.T @ X) @ X.T @ y

    # Extracting coefficients
    intercept, slope = coefficients

    # Make Predictions
    predictions = X @ coefficients

    # Plotting the data and the fitted linear model
    plt.scatter(x, y, label='Original Data')
    plt.plot(x, predictions, label='Fitted Linear Model', color='red')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Fitted Linear Model')
    plt.show()

    print("Coefficients (intercept, slope):", intercept, slope)

    return coefficients, predictions
def fit_exponential_model(data):
    # Extracting x and y values from the data
    x = np.array([item[0] for item in data])
    y = np.array([item[1] for item in data])

    # Formulate the Objective Function for an Exponential Model (y = a * e^(bx))
    X = np.vstack([np.ones_like(x), x]).T

    # Take the natural logarithm of y to linearize the model
    y_log = np.log(y)
    print(y)
    print(np.var(y))

    # Define weights based on the variance of y
    weights = 1.0 / np.var(y)

    weights = np.asanyarray(weights)
    print(weights)

    # Compute Coefficients using the weighted least squares method
    coefficients = np.linalg.inv(X.T @ (weights * X)) @ X.T @ (weights * y_log)
    # Extracting coefficients
    a = np.exp(coefficients[0])
    b = coefficients[1]

    # Make Predictions
    predictions = a * np.exp(b * x)

    # Plotting the data and the fitted exponential model
    plt.scatter(x, y, label='Original Data')
    plt.plot(x, predictions, label='Fitted Exponential Model', color='red')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Fitted Exponential Model')
    plt.show()

    print("Coefficients (a, b):", a, b)

    return coefficients, predictions


# Data for PT1000
PT1000_data = [
    (1338.52, 90.3), (1317.77, 85.7), (1305.82, 80.9 ), (1284.32, 76.1),
    (1266.25, 70.6), (1243.30, 64.9), (1237.81, 61.8), (1224.01, 59.5),
    (1205.98, 54.9), (1186.31, 50.5), (1175.15, 47), (1161.72, 44.3),
    (1158.16, 41.4), (1142.70, 37.5), (1133.50, 34.7), (1115.42, 30.2),
    (1093.64, 26.4), (1078.88, 23.8), (1069.71, 20.4)
]

PT100_data = [
    (133.52, 90.3), (131.69, 85.7), (129.7, 80.9), (127.37, 76.1),
    (125.21, 70.6), (122.79, 64.9), (121.98, 61.8), (121.49, 59.5),
    (119.61, 54.9), (117.81, 50.5), (116.43, 47), (114.24, 44.3), 
    (113.9, 41.4), (113.6, 37.5), (112.69, 34.7), (110.82, 30.2), 
    (107.93, 26.4), (108.43, 23.8), (105.63, 20.4)
]

TH5K_data = [ 
    (423.29, 90.3), (501.13, 85.7), (566.12, 80.9), (676.16, 76.1),
    (797.03, 70.6), (983.13, 64.9), (1099.89, 61.8), (1171.01, 59.5),
    (1389.92, 54.9), (1633.51, 50.5), (1865.77, 47), (2073.57, 44.3),
    (2331.95, 41.4), (2746.31, 37.5), (3083.75, 34.7), (3771.01, 30.2), 
    (4422.23, 26.4), (4753.61, 23.8), (5775.77, 20.4)
]

TH10K_data = [
    (819.23, 90.3), (946.3, 85.7), (1098.63, 80.9), (1315.35, 76.1),
    (1567.23, 70.6), (1921.97, 64.9), (2196.79, 61.8), (2324.57, 59.5),
    (2739.86, 54.9), (3221.64, 50.5), (3720.86, 47), (4192.23, 44.3),
    (4671.2, 41.4), (5504.18, 37.5), (6197.8, 34.7), (7580.4, 30.2),
    (8624.0, 26.4), (11773.03, 20.4)]

coefficients_1, predictions_1 = fit_linear_model(PT1000_data)

coefficients_2, predictions_2 = fit_linear_model(PT100_data)

coefficients_3, predictions_3 = fit_exponential_model(TH5K_data)

coefficients_4, predictions_4 = fit_exponential_model(TH10K_data)

# Define functions for fitted models with obtained coefficients
def linear_model(x, coefficients):
    intercept, slope = coefficients
    return intercept + slope * x

def exponential_model(x, coefficients):
    a, b = coefficients
    return a * np.exp(b * x)

# Coefficients for PT1000, PT100, TH5K, and TH10K
coefficients_pt1000 = (-260.3306800607545, 0.2615414383832818)
coefficients_pt100 = (-255.31709799311022, 2.5952727740633916)
coefficients_th5k = (86.21388153379931, -0.00027533588193951527)
coefficients_th10k = (85.72497612351752, -0.00013692860706152927)

'''
# New resistances and temperatures for recognition
new_data = [
    (800, 90),
    (2400, 60),
    (10500, 25)
    # Add more data points as needed
]
'''
def recognize_instrument(new_data):
    differences = {'PT1000': 0, 'PT100': 0, 'TH5K': 0, 'TH10K': 0}

    for data_point in new_data:
        resistance, temperature = data_point
        # Make predictions for each sensor type
        predictions_pt1000 = linear_model(resistance, coefficients_pt1000)
        predictions_pt100 = linear_model(resistance, coefficients_pt100)
        predictions_th5k = exponential_model(resistance, coefficients_th5k)
        predictions_th10k = exponential_model(resistance, coefficients_th10k)

        differences['PT1000'] += abs(predictions_pt1000 - float(temperature))
        differences['PT100'] += abs(predictions_pt100 - float(temperature))
        differences['TH5K'] += abs(predictions_th5k - float(temperature))
        differences['TH10K'] += abs(predictions_th10k - float(temperature))

    identified_sensor = min(differences, key=differences.get)

    print(differences)
    print(f"The identified sensor is: {identified_sensor}")
    
    return identified_sensor 