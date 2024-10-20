# 图像加法运算

import cv2
import numpy as np

img = cv2.imread("./pics/Shooting-Star-Dragon.jpg")
sum1 = img + img
sum2 = cv2.add(img, img)

cv2.imshow("img", img)
cv2.imshow("sum1", sum1)
cv2.imshow("sum2", sum2)

cv2.waitKey()
cv2.destroyAllWindows()

rows, cols, c = img.shape
img_key = np.random.randint(0, 256, (rows, cols, c), np.uint8)
cv2.imshow("img_key", img_key)
cv2.waitKey()
cv2.destroyAllWindows()

img1 = cv2.bitwise_xor(img, img_key)
img2 = cv2.bitwise_xor(img1, img_key)
cv2.imshow("img_1", img1)
cv2.imshow("img_2", img2)
cv2.waitKey()
cv2.destroyAllWindows()
