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
   ```
2. 显示图像
   ```python
   cv2.show(winname, image)
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
1. 通道
   OpenCV读取的image通道为BGR顺序
   ```python
   print(image[100, 100])
   ```