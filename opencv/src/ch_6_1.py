# 创造掩模mask
import cv2
import numpy as np

mask = np.zeros((416, 416, 3), np.uint8)
mask[50:100, 20:80, :] = 255
cv2.imshow("mask1", mask)

mask[:, :, :] = 255
mask[50:100, 20:80, :] = 0
cv2.imshow("mask2", mask)

cv2.waitKey()
cv2.destroyAllWindows()
