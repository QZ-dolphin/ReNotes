## Golang
#### Go 基础-指针
> 内容来源：https://www.topgoer.com/go%E5%9F%BA%E7%A1%80/%E6%8C%87%E9%92%88.html

取变量指针的语法
```go
ptr := &v    // v的类型为T
// ptr的类型就为*T，称做T的指针类型。*代表指针。
```
在Go语言中对于引用类型的变量，我们在使用的时候<u>不仅要声明它，还要为它分配内存空间</u>，否则我们的值就没办法存储。而对于值类型的声明不需要分配内存空间，是因为它们在声明的时候已经默认分配好了内存空间。

指针作为引用类型需要初始化后才会拥有内存空间，才可以给它赋值。

**new**
new是一个内置的函数，它的函数签名如下：
```go
func new(Type) *Type
```
new函数不太常用，使用new函数得到的是一个类型的指针，并且该指针对应的值为该类型的零值。

```go
func main() {
    var a *int
    a = new(int)
    *a = 10
    fmt.Println(*a)
}
```
**make**
make也是用于内存分配的，区别于new，它只用于slice、map以及chan的内存创建，而且它返回的类型就是这三个类型本身，而不是他们的指针类型，因为这三种类型就是引用类型，所以就没有必要返回他们的指针了。函数签名如下：

```go
func make(t Type, size ...IntegerType) Type

func main() {
    var b map[string]int
    b = make(map[string]int, 10)
    b["测试"] = 100
    fmt.Println(b)
}
```


**new与make的区别**
1. 二者都是用来做内存分配的。
2. make只用于slice、map以及channel的初始化，返回的还是这三个引用类型本身；
3. 而new用于类型的内存分配，并且内存对应的值为类型零值，返回的是指向类型的指针。

#### Go 基础-数组
> 内容来源 https://www.topgoer.com/go%E5%9F%BA%E7%A1%80/%E6%95%B0%E7%BB%84Array.html

- 指针数组 `[n]*T`，数组指针 `*[n]T`。
- 数组长度必须是常量，且是类型的组成部分。一旦定义，长度不能变。


```go
a := [3]int{1, 2}           // 未初始化元素值为 0。
b := [...]int{1, 2, 3, 4}   // 通过初始化值确定数组长度。
c := [5]int{2: 100, 4: 200} // 使用引号初始化元素。
d := [...]struct {
  name string
  age  uint8
}{
  {"user1", 10}, // 可省略元素类型。
  {"user2", 20}, // 别忘了最后一行的逗号。
}

// 多维数组
a := [2][3]int{{1, 2, 3}, {4, 5, 6}}
b := [...][2]int{{1, 1}, {2, 2}, {3, 3}} // 第 2 纬度不能用 "..."。

// 多维数组遍历
var f [2][3]int = [...][3]int{{1, 2, 3}, {7, 8, 9}}

for k1, v1 := range f {
   for k2, v2 := range v1 {
      fmt.Printf("(%d,%d)=%d ", k1, k2, v2)
   }
}
```
#### Go 基础-切片
> 内容来源 https://www.topgoer.com/go%E5%9F%BA%E7%A1%80/%E5%88%87%E7%89%87Slice.html

1、通过make创建切片，需要指定长度len
```go
var slice []type = make([]type, len)
slice  := make([]type, len) // 省略 cap，相当于 cap = len
slice  := make([]type, len, cap)
```
读写操作实际目标是底层数组

2、从数组切片

```go
arr := [5]int{1, 2, 3, 4, 5}
s := arr[1:4]
```

3、通过初始化表达式构造
```go
s1 := []int{0, 1, 2, 3, 8: 100} // s1 = [0 1 2 3 0 0 0 0 100], len = 9, cap = 9 
```

直接创建 slice 对象，自动分配底层数组

二维切片， `[][]T`，是指元素类型为 `[]T`

```go
data := [][]int{
  []int{1, 2, 3},
  []int{100, 200},
  []int{11, 22, 33, 44},
}
```
- 超出原 slice.cap 限制，就会重新分配底层数组，即便原数组并未填满。
- 通常以 2 倍容量重新分配底层数组。

`slice := data[6:8]` len为2，cap为`len(data)-6`

`slice := data[:6:8]` 每个数字前都有个冒号， slice内容为data从0到第6位，长度len为6，最大扩充项cap设置为8

`a[x:y:z]` 切片内容 `[x:y]` 切片长度: y-x 切片容量:z-x

#### Go 基础-map
> 内容来源 https://www.topgoer.com/go%E5%9F%BA%E7%A1%80/Map.html

map类型的变量默认初始值为nil，需要使用make()函数来分配内存。语法为：

```go
make(map[KeyType]ValueType, [cap])
```
## 标签页
### 后端开发
- [Golang安装](https://blog.csdn.net/s17856147699/article/details/127576375)
- [Go 学习中文文档](https://www.topgoer.com/gin%E6%A1%86%E6%9E%B6/%E7%AE%80%E4%BB%8B.html)
- [Go圣经](https://gopl-zh.github.io/index.html)
- [Go学习路线](https://www.nowcoder.com/discuss/578745918955012096)
- [GoFrame框架](https://goframe.org/display/gf)
- [GoFrame入门视频](https://www.bilibili.com/video/BV1Uu4y1u7kX/?vd_source=6dd7a82fffa3da77eb93865bdea4b98b)
- [gfast入门视频](https://www.bilibili.com/video/BV1gM411i7gw/?spm_id_from=333.337.search-card.all.click&vd_source=6dd7a82fffa3da77eb93865bdea4b98b)
- [Go Package官方文档](https://pkg.go.dev/fmt#pkg-functions)
- [控制台输出符号图像](https://patorjk.com/arial-ascii-art/#image=dolphin)
- [Beego官网](https://beegodoc.com/zh/v2.2.x/#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)
- [MongoDB教程1](https://blog.csdn.net/qq_45173404/article/details/114260970)