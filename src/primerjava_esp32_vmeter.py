import matplotlib.pyplot as plt

# Data points
v_meter = [0, 0.178, 0.374, 0.636, 0.834, 1.062, 1.198, 1.462, 1.681, 1.863, 2.037, 2.238, 2.424, 2.657, 2.822, 3.075, 3.288]
esp = [0, 0.06, 0.24, 0.51, 0.71, 0.93, 1.07, 1.34, 1.55, 1.72, 1.9, 2.1, 2.29, 2.56, 2.8, 3.25, 3.3]

# Create a plot for v_meter and esp
plt.plot(v_meter, esp, marker='o', linestyle='-', color='b')

# Set labels and title
plt.xlabel('Voltmeter / V')
plt.ylabel('ESP / V')
plt.title('Primerjava odčitanja ESP in voltmetra')

# Display the plot
plt.grid()
plt.show()
