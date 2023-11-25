import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a figure and axis
fig, ax = plt.subplots()
x = np.arange(1, 6)
y = [0] * 5
bars = plt.bar(x, y)

# Function to update the graph in each frame
def update(frame):
    y[0] += 0.1  # Increment the height of the first bar
    for bar, yi in zip(bars, y):
        bar.set_height(yi)
    return bars

# Create an animation object
ani = FuncAnimation(fig, update, blit=True)

plt.xlabel("Category")
plt.ylabel("Value")
plt.title("Animated Bar Graph")

plt.show()