import cv2


def showpic(image):
    cv2.imshow("test.jpg", image)
    cv2.waitKey()
    cv2.destroyAllWindows()


image = cv2.imread("./pics/Shooting-Star-Dragon.jpg", 0)

showpic(image)

image = cv2.imread("./pics/Shooting-Star-Dragon.jpg")
showpic(image)

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
showpic(hsv_image)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
showpic(gray_image)

b, g, r = cv2.split(image)
showpic(b)

bgra_image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
b, g, r, a = cv2.split(bgra_image)
a[:, :] = 172 # 半透明
bgra_0 = cv2.merge([b, g, r, a])
cv2.imshow("A=172", bgra_0)
cv2.waitKey()
cv2.destroyAllWindows()
