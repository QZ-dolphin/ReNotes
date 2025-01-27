## 1.3 变量声明与初始化
**局部变量**：在函数体内声明的变量称之为局部变量，它们的作用域只在函数体内，参数和返回值变量也是局部变量。

**全局变量**：在函数体外声明的变量称之为全局变量，全局变量可以在整个包甚至外部包（被导出后）使用。

1.局部变量不会一直存在，在函数被调用时存在，函数调用结束后变量就会被销毁，即生命周期。
2.Go 语言程序中全局变量与局部变量名称可以相同，但是函数内的局部变量会被优先考虑。

### 变量声明
```go
// var 变量名 变量类型
var a int
// 一次声明多个变量
var a, b int
```

### 初始化
```go
// 声明类型后初始化
var a int
a = 1
// 声明类型的同时初始化
var b, c int = 1, 2

// 自动判断类型的初始化
var a = 1 // 方法 1
b := "字符串" // 方法 2
// 出现在 := 左侧的变量不应该是已经被声明过的，否则会导致编译错误

// 如果没有初始化，则变量默认为零值
// bool 零值为 false
// 以下几种零值类型为 nil：
var a *int
var a []int
var a map[string] int
var a chan int
var a func(string) int
var a error // error 是接口
```

### 多变量声明及初始化
```go
//类型相同的多个变量, 非全局变量，平行赋值方式
var vname1, vname2, vname3 类型名
vname1, vname2, vname3 = v1, v2, v3

var vname1, vname2, vname3 = v1, v2, v3 
// 和 python 很像,不需要显示声明类型，自动推断

vname1, vname2, vname3 := v1, v2, v3 

// 这种因式分解关键字的写法一般用于声明全局变量
var (
    vname1 v_type1
    vname2 v_type2
)
```
- Go语言不支持以逗号为间隔的多个赋值语句`a := 1, b := 2`，必须使用平行赋值的方式来初始化多个变量`a, b := 1, 2`。
```go
var a, b int
var c string
a, b, c = 5, 7, "abc"
```
- 空白标识符 _ 也被用于抛弃值，如值 5 在：_, b = 5, 7 中被抛弃。
- 交换两个变量的值，则可以简单地使用 a, b = b, a，两个变量的类型必须是相同。

### 注意
1. 声明了一个局部变量却没有在相同的代码块中使用它，同样会得到编译错误。单纯地给 a 赋值也是不够的，这个值必须被使用，所以使用
    ```go
    fmt.Println("hello, world", a)
    ```
    会移除错误。
2. 全局变量允许声明但不使用。


## 1.4 变量类型
以下为 Go 内置的基础类型
### 布尔类型
关键字：bool，可赋值为预定义的true和false

$\blacksquare$ 布尔类型不接受其他类型的赋值，不支持**自动或强制**的类型转换。

### 整型 
int和int32在Go语言里被认为是两种不同的类型，编译器也不会帮你自动做类型转换。
```go
var value2 int32
value1 := 64 // value1将会被自动推导为int类型
value2 = value1 // 编译错误
// 使用强制类型转换可以解决这个编译错误：
value2 = int32(value1)
``` 
两个不同类型的整型数不能直接比较，比如int8类型的数和int类型的数不能直接比较，但各种类型的整型变量都可以直接与字面常量（literal）进行比较。

$\blacksquare$ 数值运算、比较运算、位运算与C语言都比较类似，除了取反在C语言中是~x，而在Go语言中是^x。

### 浮点型
float32和float64，自动推导的小数类型为float64 。其中float32等价于C语言的float类型，float64等价于C语言的double类型。

$\blacksquare$ 因为浮点数不是一种精确的表达方式，所以像整型那样直接用==来判断两个浮点数是否相等是不可行的，这可能会导致不稳定的结果。推荐的替代方案：
```go
import "math" 
// p为用户自定义的比较精度，比如0.00001 
func IsEqual(f1, f2, p float64) bool { 
  return math.Fdim(f1, f2) < p 
} 
```

### 数组
数组长度在定义后就不可更改，在声明时长度可以为一个常量或者一个**常量表达式**（在编译期即可计算结果的表达式）

声明方法：
```go
[32]byte // 长度为32的数组，每个元素为一个字节
[2*N] struct { x, y int32 } // 复杂类型数组
[1000]*float64 // 指针数组
[3][5]int // 二维数组
[2][2][2]float64 // 等同于[2]([2]([2]float64)) 
array := [5]int{1,2,3,4,5} // 定义并初始化一个数组
```
range具有两个返回值，第一个返回值是元素的数组下标，第二个返回值是元素的值。

### 字符串
字符串的内容可以用类似于数组下标的方式获取，但与数组不同，字符串的内容不能在初始化后被修改

字符串连接:可以通过 + 实现

### 数组切片
1. 创建
  ```go
  // 基于数组创建
  var myArray [10]int = [10]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
  var mySlice []int = myArray[:5] 
  // 基于数组切片创建数组切片
  oldSlice := []int{1, 2, 3, 4, 5} 
  newSlice := oldSlice[:3] // 基于oldSlice的前3个元素构建新数组切片
  // 选择的oldSlicef元素范围甚至可以超过所包含的元素个数，
  // 比如newSlice可以基于oldSlice的前6个元素创建，虽然oldSlice只包含5个元素。
  // 只要这个选择的范围不超过oldSlice存储能力（即cap()返回的值），
  // 那么这个创建程序就是合法的。newSlice中超出oldSlice元素的部分都会填上0。


  // 直接创建
   mySlice1 := make([]int, 5) // 创建一个初始元素个数为5的数组切片，元素初始值为0
  mySlice2 := make([]int, 5, 10) // 预留10个元素的存储空间
  mySlice3 := []int{1, 2, 3, 4, 5} // 直接创建并初始化包含5个元素的数组切片
  ```
2. 切片属性查看
  ```go
  len(mySlice)  // 查看存储数据大小
  cap(mySlice) // 查看分配空间大小
  ```
3. 添加元素
  ```go
  mySlice = append(mySlice, 1, 2, 3) // 第二个参数是不定参数，可传入多个数值
  mySlice = append(mySlice, mySlice2...) 
  // 加上省略号相当于把mySlice2包含的所有元素打散后传入
  ``` 
4. 内容复制
  内置函数copy()，用于将内容从一个数组切片复制到另一个数组切片。如果加入的两个数组切片不一样大，就会按其中较小的那个数组切片的元素个数进行复制。
  ```go
  slice1 := []int{1, 2, 3, 4, 5} 
  slice2 := []int{5, 4, 3}
  copy(slice2, slice1) // 只会复制slice1的前3个元素到slice2中
  copy(slice1, slice2) // 只会复制slice2的3个元素到slice1的前3个位置
  ```
### map
map是一堆键值对的未排序集合
```go
// 变量声明
var 变量名 map[键type] 值type
// 创建
myMap = make(map[string] PersonInfo)
myMap = make(map[string] PersonInfo, 100) //创建了一个初始存储能力为100的map
// 赋值
myMap["1234"] = PersonInfo{"1", "Jack", "Room 101,..."}
// 元素删除
delete(myMap, "1234")
// 如果“1234”这个键不存在，那么这个调用将什么都不发生，
// 也不会有什么副作用。但是如果传入的map变量的值是nil，该调用将导致程序抛出异常（panic）。

// 元素查找
value, ok := myMap["1234"]
// ok是一个返回的bool型，返回true表示找到了对应的数据
if ok { // 找到了
// 处理找到的value 
} 
```

## init 函数