######### create a histogram showing the hsv values of a given frame #########
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def image_histogram(img_dir):
    """
    In order to detect smoke, there is a need to threshold the smokes hsv values. This function gets an image as an input and creates a histogram of hsv values.
    These values can be entered to the detect function.

    :param img_dir: directory of the frame to be analyzed
    :return: histogram of hsv values to enter in the threshold
    """
    img = cv2.imread(img_dir)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')
    for x, c, z in zip([h, s, v], ['r', 'g', 'b'], [10, 20, 30]):
        xs = np.arange(256)
        ys = cv2.calcHist([x], [0], None, [256], [0, 256])
        cs = [c] * len(xs)
        cs[0] = 'c'
        ax.bar(xs, ys.ravel(), zs=z, zdir='y', color=cs, alpha=0.8)

    ax.set_xlabel('Value')
    ax.set_ylabel('')
    ax.set_zlabel('# Pixels')
    ax.set_yticks(ticks=[10,20,30])
    ax.set_yticklabels(labels = ['h', 's', 'v'])
    plt.show()


def main():
    img_dir = "smoke4.png"
    image_histogram(img_dir)


if __name__ == "__main__":
    main()
