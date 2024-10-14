import cv2
import time
import numpy as np

width, height = 200, 200
r = 20
x = r + 20
y = r + 100
x_offer = y_offer = 4

while cv2.waitKey(1) == -1:
    if x > width - r or x < r:
        x_offer *= -1
    if y > height - r or y < r:
        y_offer *= -1
    x += x_offer
    y += y_offer
    img = np.ones((width, height, 3), np.uint8) * 255
    cv2.circle(img, (x, y), r, (255, 0, 0), -1)
    cv2.imshow("img", img)
    # 只要窗口的名称相同，OpenCV 就会在同一个窗口中更新显示的内容，
    # 而不会创建新的窗口。这样可以保证窗口不会累积，也不会出现很多重复的窗口。
    # cv2.destroyAllWindows()
    # 会导致每一帧图像显示后，窗口立即被关闭，因此你将无法看到任何图像的持续显示，窗口会在每一帧中快速打开和关闭。
    time.sleep(1 / 60)

cv2.destroyAllWindows()
