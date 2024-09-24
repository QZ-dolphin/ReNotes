# opencv
## 第一章
1. 读取图像
   ```python
   image = cv2.imread(filename, flags)
   # flags 默认为 1 ，读取彩色图像；0 读取为灰度图像
   ```
2. 显示图像
   ```python
   cv2.show(winname, image)
   # winname 为显示图像的窗口名字符串，不能为中文，否则会乱码
   # image 读取的图像
   ```
   显示图像要伴随着摧毁图像，但要有等待时间