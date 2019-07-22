import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread("splash.jpg")
img_sum = np.sum(img, 2)
x, y = np.where(img_sum > 130*3)
img[x,y,:] = np.array([255,255,255])

cv2.imwrite("splash_clean.png", img)