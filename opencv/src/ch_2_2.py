import numpy as np
import cv2


def showpic(image, name="test.jpg"):
    cv2.imshow(name, image)
    cv2.waitKey()
    cv2.destroyAllWindows()


img = cv2.imread("./pics/Shooting-Star-Dragon.jpg")

img_h = np.hstack((img, img))
img_v = np.vstack((img, img))

showpic(img_h)

showpic(img_v)
