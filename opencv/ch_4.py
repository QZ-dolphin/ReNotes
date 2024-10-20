import cv2

img = cv2.imread("./pics/Shooting-Star-Dragon.jpg")
print(img.shape)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, dst1 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
_, dst2 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
_, dst3 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_TOZERO)
_, dst4 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_TOZERO_INV)
_, dst5 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_TRUNC)

cv2.imshow("GRAY", img_gray)
cv2.imshow("BINARY", dst1)
cv2.imshow("BINARY_INV", dst2)
cv2.imshow("TOZERO", dst3)
cv2.imshow("TOZERO_INV", dst4)
cv2.imshow("TRUNC", dst5)

cv2.waitKey()
cv2.destroyAllWindows()
