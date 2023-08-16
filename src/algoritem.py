import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Iz datasheetov
x_data_pt100 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
y_data_pt100 = [100, 103.903, 107.794, 111.673, 115.541, 119.397, 123.242, 127.075, 130.897, 134.707, 138.505]

x_data_pt1000 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
y_data_pt1000 = [1000.00, 1039.00, 1077.90, 1116.70, 1155.40, 1194.00, 1232.40, 1270.80, 1309.00, 1347.10, 1385.10]

x_data_5k = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
y_data_5k = [14066, 11305, 9128, 7438, 6083, 5000, 4128, 3423, 2850, 2382, 2035, 1684, 1423, 1207, 1082, 878, 752, 647, 558, 482, 419]

x_data_10k = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
y_data_10k = [32330, 25194, 19785, 15651, 12468, 10000, 8072, 6556, 5356, 4401, 3635, 3019, 2521, 2115, 1781, 1509, 1284, 1097, 941, 810, 701]

def recognizeInstrument(upornost, temperatura):
    cs_pt100 = CubicSpline(x_data_pt100, y_data_pt100)
    x_interp_pt100 = np.linspace(min(x_data_pt100), max(x_data_pt100), 100)
    y_interp_pt100 = cs_pt100(x_interp_pt100)

    cs_pt1000 = CubicSpline(x_data_pt1000, y_data_pt1000)
    x_interp_pt1000 = np.linspace(min(x_data_pt1000), max(x_data_pt1000), 100)
    y_interp_pt1000 = cs_pt1000(x_interp_pt1000)

    cs_5k = CubicSpline(x_data_5k, y_data_5k)
    x_interp_5k = np.linspace(min(x_data_5k), max(x_data_5k), 100)
    y_interp_5k = cs_5k(x_interp_5k)

    cs_10k = CubicSpline(x_data_10k, y_data_10k)
    x_interp_10k = np.linspace(min(x_data_10k), max(x_data_10k), 100)
    y_interp_10k = cs_10k(x_interp_10k)

    # Calculate the sum of squared differences for each sensor type
    pt100_diff = np.sum((upornost - cs_pt100(temperatura)) ** 2)
    pt1000_diff = np.sum((upornost - cs_pt1000(temperatura)) ** 2)
    th5k_diff = np.sum((upornost - cs_5k(temperatura)) ** 2)
    th10k_diff = np.sum((upornost - cs_10k(temperatura)) ** 2)
   
    print(pt100_diff)
    print(pt1000_diff)
    print(th5k_diff)
    print(th10k_diff)

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
