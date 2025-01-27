import numpy as np
import cv2


def showpic(image, name="test.jpg"):
    cv2.imshow(name, image)
    cv2.waitKey()
    cv2.destroyAllWindows()


canvas = np.zeros((300, 300, 3), np.uint8)
canvas = cv2.line(canvas, (50, 50), (250, 50), (255, 0, 0), 5)
canvas = cv2.line(canvas, (50, 150), (250, 150), (0, 255, 0), 10)
canvas = cv2.line(canvas, (50, 250), (250, 250), (0, 0, 255), 15)
canvas = cv2.line(canvas, (150, 50), (150, 250), (0, 255, 255), 20)

showpic(canvas)

canvas = np.ones((300, 300, 3), np.uint8) * 255
canvas = cv2.rectangle(canvas, (50, 50), (250, 250), (0, 0, 255), 40)
canvas = cv2.rectangle(canvas, (140, 140), (160, 160), (0, 255, 255), -1)
showpic(canvas)

k = np.random.randint(0, high=256, size=(3,))
print(k)
print(k.tolist())

k = np.zeros((3))
print(k)
