import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

def computePriorityAtPoint(samplingLocation, closeRangePriority, smallAnglePriority, blindSpotSize):
    unnormalized_distance = max(np.linalg.norm(samplingLocation - centerLocation), eps)

    if(unnormalized_distance > maxRange or unnormalized_distance == eps):
        return 0

    normalized_distance = unnormalized_distance / maxRange

    direction = (samplingLocation - centerLocation) / unnormalized_distance

    # angle is arccos of dot product (and then convert to degrees for consistency)
    angle = max(np.abs(np.arccos(np.dot(direction, forwardVector))) / np.pi, eps)

    if(angle > 1 - blindSpotSize):
        return 0

    val = ((1.0 / np.float_power(closeRangePriority, normalized_distance))) * ((1.0 /np.float_power(smallAnglePriority, angle)))
    return val

#print(computePriorityAtPoint(np.array([1, 1]), np.array([0, 0]), np.array([1, 0]), 0.1, 0.1, 0.1, 0.1))

width = 10
x_start = -width/2
height = width
y_start = -height/2

x_samples = 40
y_samples = x_samples

maxRange = 5

eps = 1e-8

centerLocation = np.array([0.0, 0.0])
forwardVector =  np.array([1.0, 0.0])
forwardVector = forwardVector / np.linalg.norm(forwardVector)

def update(val):
    closeRangePriority = slider_a.val
    smallAnglePriority = slider_b.val
    blindSpotSize = slider_c.val
    #blindSpotSize = slider_c.val
    pdf = []
    #find non-normalized values
    for x in range(x_samples):
        x_coord = x_start + x * (width / x_samples)
        pdf.append([])
        for y in range(y_samples):
            y_coord = y_start + y * (height / y_samples)
            pdf[-1] += [computePriorityAtPoint(np.array([x_coord, y_coord]), closeRangePriority, smallAnglePriority, blindSpotSize)]


    #normalize so cdf sums up to 1
    pdf = np.array(pdf)
    #print(f"Before normalizing: {pdf}")
    pdf += pdf.min()
    sum = pdf.sum()
    pdf /= sum

    #print(f"After normalizing: {pdf}")

    max = pdf.max()
    #print(f"Max is {max}")
    ax.cla()
    ax.imshow(np.rot90(pdf.reshape(x_samples, y_samples), k=2), cmap='inferno')
    plt.show()

fig, ax = plt.subplots()
# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.2, bottom=0.35)

slider_ax = fig.add_axes([0.3, 0.25, 0.6, 0.03])  # [left, bottom, width, height]
slider_a = Slider(ax=slider_ax, label='Close-Range priority', valmin=0.01, valmax=10, valinit=1)
slider_bx = fig.add_axes([0.3, 0.15, 0.6, 0.03])  # [left, bottom, width, height]
slider_b = Slider(ax=slider_bx, label='Small Angle Priority', valmin=0.01, valmax=10, valinit=1)
slider_cx = fig.add_axes([0.3, 0.05, 0.6, 0.03])  # [left, bottom, width, height]
slider_c = Slider(ax=slider_cx, label='Blind Spot Size', valmin=0, valmax=0.999, valinit=0)

slider_a.on_changed(update)
slider_b.on_changed(update)
slider_c.on_changed(update)

update(0)


