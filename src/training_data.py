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

    # Formulate the Objective Function for a Steinhart-Hart equation
    X = np.vstack([np.ones_like(x), np.log(x), np.log(x)**3]).T

    coefficients = np.linalg.inv(X.T @ X) @ X.T @ y

    A, B, C = coefficients
    # Make Predictions
    predictions = X @ coefficients
    
    # Plotting the data and the fitted exponential model
    plt.scatter(x, y, label='Pomerjeni podatki')
    plt.plot(x, predictions, label='Prilagojen Steinhart-Hart model', color='red')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Steinhart-Hart Model')
    plt.show()
    print("Coefficients (A, B, C):", A, B, C)

    return coefficients, predictions

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


# Define the Steinhart-Hart equation
def steinhart_hart_equation(x, A, B, C):
    return (A + B * np.log(x) + C * (np.log(x))**3)

#Corrected coefficients
coefficients_pt1000 = (-253.58764550253449, 0.2535439569327526)
coefficients_pt100 = (-255.31162871251036, 2.5278962517294774)
coefficients_th5k = ( 297.29153084495874, -37.92062011369887, 0.08199604438012592)
coefficients_th10k = ( 315.98834354026803, -37.40210606159289, 0.0678906892369372)

def recognize_instrument(new_data):
    differences = {'PT1000': 0, 'PT100': 0, 'TH5K': 0, 'TH10K': 0}

    x = np.array([item[0] for item in new_data])
    y = np.array([item[1] for item in new_data])
    
    pt100 = linear_model(x, coefficients_pt100)
    pt1000 = linear_model(x, coefficients_pt1000)
    th5k = steinhart_hart_equation(x, coefficients_th5k[0], coefficients_th5k[1], coefficients_th5k[2])
    th10k = steinhart_hart_equation(x, coefficients_th10k[0], coefficients_th10k[1], coefficients_th10k[2])

    y = np.array(y, dtype=float)  #  Dtype must be float, in case we insert integer 

    differences['PT100'] = np.sum(np.abs(pt100 - (y)))
    differences['PT1000'] = np.sum(np.abs(pt1000 - (y)))


    differences['TH5K'] = np.sum(np.abs(th5k - (y)))
    differences['TH10K'] = np.sum(np.abs(th10k - (y)))

    identified_sensor = min(differences, key=differences.get)

    print(differences)
    print(f"The identified sensor is: {identified_sensor}")
    
    return identified_sensor

fit_linear_model(PT100_data)
fit_linear_model(PT1000_data)
fit_exponential_model(TH5K_data)
fit_exponential_model(TH10K_data)