# opencv
## 预备知识
0. 创建conda环境
   ```batch
   conda create -n 环境名 python=3.6
   REM 创建python版本为3.6的 环境

   activate myenv 
   REM 进入创建的虚拟环境

   REM 使用清华源下载包
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 包名
   ```
1. 安装opencv包
   部分函数设计专利问题，如SIFT和SURF，所以需要使用opencv-python==3.4.1.15版本的，并且python需要3.6才能支持安装。
   ```batch
   pip install opencv-python==3.4.1.15
   REM 安装opencv
   pip install opencv-contrib-python==3.4.1.15
   REM 安装opencv的其他包
   ```
2. 导入
   ```python
   import cv2
   ```
## 第一章
1. 读取图像
   ```python
   image = cv2.imread(filename, flags)
   # flags 默认为 1 ，读取彩色图像；0 读取为灰度图像
   # filename如果为中文也会导致无法读取
   ```
2. 显示图像
   ```python
   cv2.imshow(winname, image)
   # winname 为显示图像的窗口名字符串，不能为中文，否则会乱码
   # image 读取的图像
   ```
   显示图像要伴随着摧毁图像，但要有等待时间
   ```python
   retval = cv2.waitKey(delay)
   # delay 等待时间 ms 当 delay <= 0 或为空时，表示无限等待
   # 当用户按下任意按键，执行waitKey()方法。返回值为按键对应的ASCII码

   # 销毁所有显示图像的窗口
   cv2.destoryAllWindows()
   ```

3. 保存图像
   ```python
   cv2.imwrite(保存的文件路径+文件名, image)
   cv2.imwrite("D:/pics/1.jpg", image)
   ```

4. 图像属性
   ```python
   image.shape # 图像形状 像素行数（高）、像素列数（长）、通道数
   image.size # 像素个数
   image.dtype # 数据类型 uint8
   ```

## 第二章
### 通道基础
1. 通道
   
   OpenCV读取的image通道为BGR顺序
   ```python
   print(image[100, 100])
   ```
---
> 20240927
2. 色彩空间
   
   GRAY色彩空间：灰度级[0, 255]，0纯黑，255纯白

   HSV色彩空间：
      - 色调[0, 180] 红色：0 黄色：30 绿色：60 蓝色 120
      - 饱和度S [0, 255] 颜色深浅
      - 亮度V [0, 255] 光的明暗
  
  色彩空间转换：
  ```python
  image1 = cv2.cvtColor(image0, code)
  # image0 原图像 image1 转换后图像
  # code 色彩空间转换码
  ```
  - cv2.COLOR_BGR2GRAY
  - cv2.COLOR_RGB2GRAY  灰度图像无法转换为彩色图像，因为丢失了颜色比例
  - cv2.COLOR_BGR2HSV
  - cv2.COLOR_RGB2HSV

3. 通道拆分
   
   > 拆分BGR图像
   ```python
   b, g, r = cv2.split(bgr_image)
   h, s, v = cv2.split(hsv_image)
   ```
   其中b, g, r同样为图像数据，但通道值分别为[B, B, B] [G, G, G] [R, R, R]：都是灰度图像，亮度有所区别。

   对于BGR图像，只要B=G=R，数值相等就是灰度图像。

4. 合并通道

   ```python
   bgr_image = cv2.merge([b, g, r])
   hsv_image = cv2.merge([h, s, v])
   # 通道合并顺序不能变，否则得不到原图
   ```
5. 修改某一通道的值
   ```python
   b[:, :] = x # 将通道分量的所有值修改为x
   ```
6. 透明度alhpa通道
   
   [0, 255] 0：全透明，255：不透明
   ```python
   # 将bgr图像转换为bgra图像，再修改透明度a通道
   bgra_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2BGRA)
   b, g, r, a = cv2.split(bgra_image)
   a[:, :] = 172 # 半透明
   bgra_0 = cv2.merge([b, g, r, a])
   cv2.imshow("A=172", bgra_0)
   ```
---
> 20240929

### Numpy 数组
1. 创建一维和二维数组
   
   ```python
   import numpy as np
   n1 = np.array([0.1, 0.2, 0.3])
   n2 = np.array([[1, 2, 3], [2, 3, 4]])
   ```
2. 指定数组的数据类型
   
   ```python
   list = [1, 2, 3]
   n3 = np.array(list, dtype=np.float64) # 或者 n3 = np.array(list, dtype=float)
   print(n3)
   print(n3.dtype)
   print(type(n3))
   ```   
3. 创建3维数组
   
   ```python
   list = [1, 2, 3]
   n4 = np.array(list, ndmin=3)
   print(n4)
   ```   

4. 创建未初始化数组
   ```python
   n5 = np.empty([2, 3]) # 里面数字代表维度，会取随机值，可用dtype指定类型
   print(n5)
   ``` 

> 2024/10/11
- 创建纯0数组
```python
n = np.zeros((3, 3), np.uint8)
```

- 创建纯1数组
```python
n = np.ones((3, 3), np.uint8)
```

- 复制数组
```python
# 方法 1
n2 = np.array(n1, copy=True)
# 方法 2
n2 = n1.copy()
```
创建副本，修改副本不会影响原数组。

- 索引方式
```python
n1 = np.array([[1, 2, 3], [2, 3, 4]])
print(n1[1])
print(n1[0, 1])
```
`n1[0, 1]`对比于`n1[0][1]`，后者是先索引一个维度得到一个数组，在在此基础上再索引。

### 创建图像
数组维度顺序：高、宽、通道
```python
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
```

### 拼接图像
拼接多个图像数组元组，数组形状需相同
```python
array1 = np.hstack(tup) # 水平拼接
array2 = np.vstack(tup) # 垂直拼接
```

## 绘制图形