import cv2
image = cv2.imread("./pics/Shooting-Star-Dragon.jpg")

cv2.imshow("test.jpg", image)
cv2.waitKey()
cv2.destroyAllWindows()