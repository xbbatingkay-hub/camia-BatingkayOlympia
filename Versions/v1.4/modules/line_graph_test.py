import matplotlib.pyplot as plt
import numpy as np
import random

# 1. Prepare data for the x-axis and y-axis
while True:
    xpoints = np.array([random.randint(1,10), random.randint(1,10), random.randint(1,10), random.randint(1,10)])
    ypoints = np.array([random.randint(1,10), random.randint(1,10), random.randint(1,10), random.randint(1,10)])

    # 2. Plot the line chart
    plt.plot(xpoints, ypoints)

    # 3. Add labels and title for clarity
    plt.xlabel("X-axis Label")
    plt.ylabel("Y-axis Label")
    plt.title("My First Line Graph")

    # 4. Display the graph
    plt.show()