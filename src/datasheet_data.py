from scipy import interpolate
import matplotlib.pyplot as plt

y_data_pt100 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
x_data_pt100 = [100, 103.903, 107.794, 111.673, 115.541, 119.397, 123.242, 127.075, 130.897, 134.707, 138.505]

x_data_pt1000 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
y_data_pt1000 = [1000.00, 1039.00, 1077.90, 1116.70, 1155.40, 1194.00, 1232.40, 1270.80, 1309.00, 1347.10, 1385.10]

y_data_5k = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
x_data_5k = [14066, 11305, 9128, 7438, 6083, 5000, 4128, 3423, 2850, 2382, 2035, 1684, 1423, 1207, 1082, 878, 752, 647, 558, 482, 419]

x_data_10k = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
y_data_10k = [32330, 25194, 19785, 15651, 12468, 10000, 8072, 6556, 5356, 4401, 3635, 3019, 2521, 2115, 1781, 1509, 1284, 1097, 941, 810, 701]

left_voltage = 1918
volt = left_voltage * (3.3/(pow(2,12)-1))
volt = 2.992
target_resistance = 980*((3.3/volt) - 1)
# Resistance value to find the corresponding temperature
target_resistance = 112
# Perform linear interpolation
interp_func = interpolate.interp1d(x_data_pt100, y_data_pt100, kind='linear')

# Find the interpolated temperature value
temperature = interp_func(target_resistance)

print("Temperature:", temperature, "°C")




#plt.plot(x_data_pt100, y_data_pt100, label='PT100')
plt.plot(x_data_pt100, y_data_pt100, label='Pt100', color = 'red')
plt.xlabel('Upornost (R)')
plt.ylabel('Temperatura (°C)')
plt.title('Pt100 R(T)')
plt.legend()
plt.grid()
plt.show()


#plt.plot(x_data_pt100, y_data_pt100, label='PT100')
plt.plot(x_data_5k, y_data_5k, label='Th5k', color = 'red')
plt.xlabel('Upornost (R)')
plt.ylabel('Temperatura (°C)')
plt.title('Th5K R(T)')
plt.legend()
plt.grid()
plt.show()