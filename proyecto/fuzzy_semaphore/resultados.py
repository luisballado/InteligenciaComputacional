import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

#%
#linea1 = [0,31,78,78,78,87,78,78,78,78,78]
#tiempo
linea1 = [30,11,44,44,44,44,44,44,44,44,44]

mean = np.mean(linea1)
std_dev = np.std(linea1)

# Create a range of x values
x = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 100)

# Use the normal distribution to calculate y values
y = norm.pdf(x, mean, std_dev)

# Plot the data
plt.plot(x, y)
plt.xlabel('LINEA1 t')
plt.ylabel('Probability density')
plt.savefig('linea1t.png')
plt.clf()

#linea2 = [25,55,92,99,99,85,99,99,99,99,99]
linea2 = [7,28,44,44,44,44,44,44,44,44,44]
mean = np.mean(linea2)
std_dev = np.std(linea2)

# Create a range of x values
x = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 100)

# Use the normal distribution to calculate y values
y = norm.pdf(x, mean, std_dev)

# Plot the data
plt.plot(x, y)
plt.xlabel('LINEA2 t')
plt.ylabel('Probability density')
plt.savefig('linea2t.png')
plt.clf()

#linea3 = [33,55,99,99,99,92,99,99,99,92,99]
linea3 = [12,27,44,44,44,44,44,44,44,44,44]
mean = np.mean(linea3)
std_dev = np.std(linea3)

# Create a range of x values
x = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 100)

# Use the normal distribution to calculate y values
y = norm.pdf(x, mean, std_dev)

# Plot the data
plt.plot(x, y)
plt.xlabel('LINEA3 t')
plt.ylabel('Probability density')
plt.savefig('linea3t.png')
plt.clf()

linea4 = [8,33,44,44,44,44,44,44,44,44,44]
#linea4 = [25,63,100,85,85,100,100,85,92,87,92]
mean = np.mean(linea4)
std_dev = np.std(linea4)

# Create a range of x values
x = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 100)

# Use the normal distribution to calculate y values
y = norm.pdf(x, mean, std_dev)

# Plot the data
plt.plot(x, y)
plt.xlabel('LINEA4 t')
plt.ylabel('Probability density')
plt.savefig('linea4t.png')
plt.clf()

