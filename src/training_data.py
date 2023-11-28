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
    plt.scatter(x, y, label='Pomerjene točke')
    plt.plot(x, predictions, label='Prilagojen linearen model', color='red')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Linearni Model')
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

    # Define weights based on the variance of y
    #weights = 1.0 / np.var(y)
    weights = y
    weights = np.asanyarray(weights)
    print(weights)

    # Compute Coefficients using the weighted least squares method
    #coefficients = np.linalg.inv(X.T @ (weights * X)) @ X.T @ (weights * y_log)
    coefficients = np.linalg.inv(X.T @ (weights[:, None] * X)) @ X.T @ (weights * y_log)    # Extracting coefficients
    ln_a = (coefficients[0])
    b = coefficients[1]
    a = np.exp(ln_a)
    # Make Predictions
    predictions = a * np.exp(b * x)
    
    # Plotting the data and the fitted exponential model
    plt.scatter(x, y, label='Pomerjeni podatki')
    plt.plot(x, predictions, label='Prilagojen eksponencijalen model', color='red')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Eksponencijalni Model')
    plt.show()
    print("Coefficients (a, b):", a, b)

    return coefficients, predictions

'''
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
'''

# Corrected and better training data
PT1000_data = [
    (1342.52, 86.5), (1326.27, 83), (1306.25, 77 ), (1287.08, 72.5),
    (1276.46, 69.5), (1258.97, 66), (1242.84, 61.5), (1221.23, 57.4),
    (1202.36, 53.3), (1185.58, 49), (1175.11, 46), (1170.43, 43.3),
    (1162.36, 40.2), (1154.63, 36.6), (1111.84, 29.3),
    (1102.54, 27.3), (1097.12, 24.5), (1084.36, 21.8)
]
TH5K_data = [
    (423.52, 86.5), (481.50, 83), (573.90, 77 ), (676.75, 72.5),
    (747.15, 69.5), (854.51, 66), (994.25, 61.5), (1265.42, 57.4),
    (1470.54, 53.3), (1736.24, 49), (1928.19, 46), (2179.77, 43.3),
    (2468.17, 40.2), (2880.47, 36.6), (3408.46, 33), (3960.12, 29.3),
    (4421.77, 27.3), (4851.93, 24.5), (6164.58, 21.8)
]
PT100_data = [
    (134.84, 86.5), (134, 83), (132.09, 77 ), (129.95, 72.5),
    (128.52, 69.5), (126.91, 66), (124.76, 61.5), (123.49, 57.4),
    (120.88, 53.3), (119.39, 49), (118.65, 46), (118.98, 43.3),
    (118.08, 40.2), (116.58, 36.6), (114.80, 33), (112.16, 29.3),
    (110.60, 27.3), (111.22, 24.5), (109.82, 21.8)
]
TH10K_data = [
    (810.56, 86.5), (901.21, 83), (1121.89, 77 ), (1299.39, 72.5),
    (1440.27, 69.5), (1615.75, 66), (1926.24, 61.5), (2448.05, 57.4),
    (2909.00, 53.3), (3406.25, 49), (3811.06, 46), (4152.41, 43.3),
    (4763.95, 40.2), (5664.58, 36.6), (6728.23, 33), (7822.26, 29.3),
    (8629.05, 27.3), (9511.03, 24.5), (12006.66, 21.8)
]

# Define functions for fitted models with obtained coefficients
def linear_model(x, coefficients):
    intercept, slope = coefficients
    return intercept + slope * x


def exponential_model(x, coefficients):
    a, b = coefficients
    print("coefficients:", coefficients)
    predictions = a * np.exp(b * x)
    
    # Don't include in program, because starting a MatplotGUI outside of the main thread will likely fall
    '''
    # Plotting the data and the fitted exponential model
    plt.scatter(x, predictions, label='Fitted Exponential Model', color='red')
    plt.xlabel('x')
    plt.ylabel('Predictions')
    plt.title('Fitted Exponential Model')
    plt.legend()
    plt.show()
    '''
    return predictions
'''
# Coefficients for PT1000, PT100, TH5K, and TH10K
coefficients_pt1000 = (-260.3306800607545, 0.2615414383832818)
coefficients_pt100 = (-255.31709799311022, 2.5952727740633916)
coefficients_th5k = (86.21388153379931, -0.00027533588193951527)
coefficients_th10k = (85.72497612351752, -0.00013692860706152927)
'''

#Corrected coefficients
coefficients_pt1000 = (-253.58764550253449, 0.2535439569327526)
coefficients_pt100 = (-255.31162871251036, 2.5278962517294774)
coefficients_th5k = (85.23508764589549, -0.0002677961726906676)
coefficients_th10k = (84.94632442583986, -0.00013643613903726272)


def recognize_instrument(new_data):
    differences = {'PT1000': 0, 'PT100': 0, 'TH5K': 0, 'TH10K': 0}

    x = np.array([item[0] for item in new_data])
    y = np.array([item[1] for item in new_data])
    
    pt100 = linear_model(x, coefficients_pt100)
    pt1000 = linear_model(x, coefficients_pt1000)
    th5k = exponential_model(x, coefficients_th5k)
    th10k = exponential_model(x, coefficients_th10k)

    y = np.array(y, dtype=float)  #  Dtype must be float, in case we insert integer 

    differences['PT100'] = np.sum(np.abs(pt100 - (y)))
    differences['PT1000'] = np.sum(np.abs(pt1000 - (y)))
    differences['TH5K'] = np.sum(np.abs(th5k - (y)))
    differences['TH10K'] = np.sum(np.abs(th10k - (y)))

    print(differences)

    identified_sensor = min(differences, key=differences.get)

    print(differences)
    print(f"The identified sensor is: {identified_sensor}")
    
    return identified_sensor

fit_linear_model(PT100_data)
fit_linear_model(PT1000_data)
fit_exponential_model(TH5K_data)
fit_exponential_model(TH10K_data)