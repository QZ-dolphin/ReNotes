## Gin
### 安装
```bash
go install github.com/gin-gonic/gin@latest
```
```go
import "github.com/gin-gonic/gin" // 导入
```
### 初步使用
```bash
mkdir GinProject
cd GinProject
go mod init GinProject
touch example.go
```
```go
// example.go
package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
)

func main() {
    //1.创建路由
    r := gin.Default()
    //2.绑定路由规则，执行的函数
    r.GET("/", func(context *gin.Context) {
        context.String(http.StatusOK, "Hello World!")
    })
    //3.监听端口，默认8080
    r.Run(":8000")
}
```
```bash
go mod tidy
go run example.go
```
### 初步讲解
```go
router.GET("/json", func(c *gin.Context) {
  c.JSON(200, gin.H{
    "html": "<b>Hello, world!</b>",
  })
})
```
`gin.H`是一个结构体的别名，用于快速创建`map[string]interface{}`对象。

**增加页面头像**
```bash
go get "github.com/thinkerou/favicon"
```
```go
import "github.com/thinkerou/favicon"

r := gin.Default()
r.Use(favicon.New("./favicon.ico"))
```
RESTful API Representational State Transfer 表现层状态转化，一种互联网应用程序的API设计理念：URL定位资源，用HTTP描述操作
get /user
post /user
put /user
delete /user

加载静态页面

i.(type) ​专门用于 switch 的类型断言，作用是判断接口变量 i 的底层动态类型。这是 Go 语言中唯一可以使用 . (type) 的场合

## Gin系统学习
### 安装与运行
#### 创建路由
`r := gin.Default`
`gin.Context`，封装了request和response
#### `gin.Default()`和`gin.New()`的区别
​**gin.New()**：创建一个全新的 Gin 引擎实例，不包含任何默认中间件。你需要手动添加所有你需要的中间件。
​**gin.Default()**：创建一个 Gin 引擎实例，并默认包含 Logger 和 Recovery 中间件。这两个中间件分别用于记录请求日志和在发生 panic 时恢复服务。

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    // 创建一个全新的 Gin 引擎实例
    r := gin.New()

    // 手动添加日志中间件
    r.Use(gin.Logger())

    // 手动添加错误恢复中间件
    r.Use(gin.Recovery())

    // 添加一个简单的路由
    r.GET("/", func(c *gin.Context) {
        c.String(200, "Hello, World!")
    })

    // 启动服务器
    r.Run(":8080")
}
```
### 请求处理基础
#### 1、查询字符串参数
包含在url中的参数，获取方法：
- `c.DefaultQuery('查询项名', '设置的默认值')`，若未查询到则为默认值
- `c.Query('查询项名')`，若未查询到则为空
```go
func main() {
	router := gin.Default()

	// 使用现有的基础请求对象解析查询字符串参数。
	// 示例 URL： /welcome?firstname=qingzhen&lastname=dong
	router.GET("/welcome", func(c *gin.Context) {
		firstname := c.DefaultQuery("firstname", "Guest")
		lastname := c.Query("lastname") // c.Request.URL.Query().Get("lastname") 的一种快捷方式

		c.String(http.StatusOK, "Hello %s %s", firstname, lastname)
	})
	router.Run(":8080")
}
```
#### 2、路由参数
获取路由中的动态路由参数，获取方法：
- `c.Param('查询项名')`
```go
func main() {
	router := gin.Default()

	// 此 handler 将匹配 /user/john 但不会匹配 /user/ 或者 /user
	router.GET("/user/:name", func(c *gin.Context) {
		name := c.Param("name")
		c.String(http.StatusOK, "Hello %s", name)
	})

	// 此 handler 将匹配 /user/john/ 和 /user/john/send
	// 如果没有其他路由匹配 /user/john，它将重定向到 /user/john/
	router.GET("/user/:name/*action", func(c *gin.Context) {
		name := c.Param("name")
		action := c.Param("action")
		message := name + " is " + action
		c.String(http.StatusOK, message)
	})

	router.Run(":8080")
}
```
在 Gin 框架中，路由参数中的 : 和 * 是用来定义动态路由参数的符号，分别用于定义必选参数和可选参数。
`:` 用于定义一个**必选**的路由参数，表示该位置必须有一个值，并且该值会被捕获并存储到 gin.Context 的 Params 中。
`*` 用于定义一个可选的路由参数，表示该位置可以有0个或多个值，并且这些值会被捕获并存储到 gin.Context 的 Params 中。`*` 必须放在路由的最后一个部分。

Gin 允许在 `:` 定义的必选参数后面附加一个正则表达式，用于限制参数的格式。
```go
:参数名(正则表达式)
```
#### 3、使用 HTTP 方法
`r.HTTP方法名("路由", 对应执行函数)`
```go
func main() {
	// 禁用控制台颜色
	// gin.DisableConsoleColor()

	// 使用默认中间件（logger 和 recovery 中间件）创建 gin 路由
	router := gin.Default()

	router.GET("/someGet", getting)
	router.POST("/somePost", posting)
	router.PUT("/somePut", putting)
	router.DELETE("/someDelete", deleting)
	router.PATCH("/somePatch", patching)
	router.HEAD("/someHead", head)
	router.OPTIONS("/someOptions", options)

	// 默认在 8080 端口启动服务，除非定义了一个 PORT 的环境变量。
	router.Run()
	// router.Run(":3000") hardcode 端口号
}
```
参数`执行函数`可以是直接定义的匿名函数，也可以是在外面定义的全局函数的函数名。
#### 4、从Reader读取数据
没啥好学的0.0，不如去看http包文档。
### 响应格式
#### 1、JSON/XML/YAML响应，ProtoBuf序列化
返回对应格式的响应
```go
c.JSON(http.StatusOK, msg)
c.XML(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
c.YAML(http.StatusOK, gin.H{"message": "hey", "status": http.StatusOK})
c.ProtoBuf(http.StatusOK, data) // 数据在响应中变为二进制数据
```
在 Gin 框架中，​ProtoBuf 序列化 是一种使用 ​Protocol Buffers（Protobuf）​ 协议进行数据序列化和反序列化的方式。Protobuf 是 Google 开发的一种轻量级、高效的二进制数据交换格式，广泛用于网络通信和数据存储。Gin 提供了对 Protobuf 的原生支持，可以方便地将数据序列化为 Protobuf 格式或从 Protobuf 格式反序列化数据。
#### 2、PureJSON与AsciiJSON的区别
在 Gin 框架中，PureJSON 和 AsciiJSON 都是用于返回 JSON 数据的方法
```go
c.AsciiJSON(http.StatusOK, data)
c.PureJSON(200, gin.H{
  "html": "<b>Hello, world!</b>",
})
```
- PureJSON 返回的 JSON 数据是原始格式的，不会对特殊字符（如 Unicode 字符、HTML 标签等）进行转义或编码。这意味着返回的 JSON 数据会保留原始字符，包括非 ASCII 字符（如中文、表情符号等）。
- AsciiJSON 返回的 JSON 数据会将非 ASCII 字符转义为 \uXXXX 格式的 Unicode 编码。这样可以确保返回的 JSON 数据只包含 ASCII 字符，适合某些不支持非 ASCII 字符的客户端或系统。

#### 3、SecureJSON的安全特性
SecureJSON 的实现非常简单，就是在 JSON 数据前添加一个固定的前缀。Gin 框架默认使用 while(1); 作为前缀。
```go
c.SecureJSON(http.StatusOK, data)
```
SecureJSON 是一种简单而有效的防止 JSON 劫持的机制。通过在 JSON 数据前添加不可解析的前缀，可以阻止恶意脚本窃取敏感数据。在需要高安全性的 Web 应用程序中，建议使用 SecureJSON 来保护 JSON 数据。
如果客户端需要解析 SecureJSON 返回的数据，需要手动去掉前缀。
```js
fetch('/securejson')
    .then(response => response.text())
    .then(data => {
        // 去掉前缀
        const jsonData = data.replace('while(1);', '');
        // 解析 JSON
        const obj = JSON.parse(jsonData);
        console.log(obj);
    });
```
### 表单处理
#### Multipart/Urlencoded表单绑定
从提交的表单中获取数据
```go
message := c.PostForm("message")
nick := c.DefaultPostForm("nick", "anonymous")
```

一种用于处理客户端提交的表单数据的机制。具体来说，它用于解析和绑定以下两种常见的表单数据格式：
1. ​**multipart/form-data**：通常用于文件上传，表单数据会被分割成多个部分（parts），每个部分包含一个字段或文件。
2. ​**application/x-www-form-urlencoded**：通常用于普通表单提交，表单数据会被编码为键值对（key-value pairs），类似于 URL 查询参数。

Gin 提供了方便的方法来解析和绑定这两种表单数据，并将其映射到 Go 的结构体或变量中。
```go
package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
)

type UploadForm struct {
    Name  string `form:"name"`
    Email string `form:"email"`
    File  *multipart.FileHeader `form:"file"`
}

func main() {
    r := gin.Default()

    r.POST("/upload", func(c *gin.Context) {
        var form UploadForm
        if err := c.ShouldBind(&form); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        // 保存文件
        if form.File != nil {
            c.SaveUploadedFile(form.File, "./uploads/"+form.File.Filename)
        }

        c.JSON(http.StatusOK, gin.H{
            "name":  form.Name,
            "email": form.Email,
            "file":  form.File.Filename,
        })
    })

    r.Run(":8080")
}
```
multipart/form-data 表单通常用于文件上传，但也可以用于普通字段。application/x-www-form-urlencoded 表单用于普通字段提交，数据会被编码为键值对。如果需要显式指定绑定类型，可以使用 c.ShouldBindWith 方法，并传入 binding.Form 或 binding.FormMultipart。
​**binding 包**：提供了表单数据的解析和验证功能。