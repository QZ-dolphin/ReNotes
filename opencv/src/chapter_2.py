import numpy as np
import cv2

n1 = np.array([0.1, 0.2, 0.3])
n2 = np.array([[1, 2, 3], [2, 3, 4]])

list = [1, 2, 3]
n3 = np.array(list, dtype=np.float64)  # 或者 n3 = np.array(list, dtype=float)
print(n3)
print(n3.dtype)
print(type(n3))
print(type(n3[0]))

n4 = np.array(list, ndmin=3)
print(n4)

n5 = np.empty([2, 3])  # 里面数字代表维度，会取随机值，可用dtype指定类型
print(n5)

width = 200
height = 100
# 创建单通道、像素值都为0的纯黑图像
img = np.zeros((height, width), np.uint8)
cv2.imshow("black", img)
cv2.waitKey()
cv2.destroyAllWindows()

# 创建单通道、像素值都为255的纯白图像
img = np.ones((height, width), np.uint8) * 255
cv2.imshow("white", img)
cv2.waitKey()
cv2.destroyAllWindows()

# 修改像素值
img[25:75, 50:100] = 0
cv2.imshow("pic1", img)
cv2.waitKey()
cv2.destroyAllWindows()


def showpic(image, name="test.jpg"):
    cv2.imshow(name, image)
    cv2.waitKey()
    cv2.destroyAllWindows()


img = np.zeros((height, width), np.uint8)
for i in range(0, width, 40):
    img[:, i : i + 20] = 255
showpic(img)

# 创建纯蓝图像
img = np.zeros((height, width, 3), np.uint8)
blue = img.copy()
blue[:, :, 0] = 255
showpic(blue)

# 创建随机彩色图像
img = np.random.randint(256, size=(height, width, 3), dtype=np.uint8)
showpic((img))
