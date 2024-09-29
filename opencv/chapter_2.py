import numpy as np

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
