## vector 类

若返回的数据类型为`vector<int>`类，且类似坐标格式，可以直接返回数组`{a, b}`

创建二维向量方式
```vector<vector<int>> dp(n, vector<int>(n));```

## 折半查找

求中值防越界`int mid = ((right - left) >> 1) + left;`

## 动态规划
用迭代不如用循环