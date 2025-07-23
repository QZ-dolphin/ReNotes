# 开发记录
## 初始化项目
### goframe安装
```sh
go install github.com/gogf/gf/cmd/gf/v2@latest
```
> 注意：需要将 `$GOPATH/bin` 加入到系统环境变量中，通过 `go env GOPATH` 查看。
后端（GoFrame）通用初始化方式
```bash
gf init 项目名 -u
# -u 代表最新框架版本更新

cd 项目名
gf run main.go # 运行
```
后端项目名此处设置为zeal_be
```bash
gf init zeal_be
```
删除已有关于hello的api, logic, controller, cmd中代码文件内容
```bash
rm -rf api/hello/
rm -rf internal/controller/hello/
```
## 创建跨域中间件
在后端项目中，跨域（Cross-Origin）指的是浏览器出于安全考虑，限制从一个源加载的文档或脚本如何与来自另一个源的资源进行交互。这里的“源”指的就是协议、域名和端口的组合。例如，一个源可以是`http://example.com:8080`，而另一个源可以是`http://api.example.com:8080`或`https://example.com:8080`。

当你的前端应用运行在`http://example.com:3000`，而它尝试通过AJAX请求与`http://api.example.com:8080`进行通信时，这就会被认为是跨域请求。浏览器默认会阻止这种请求，除非后端服务器明确允许这种跨域请求。

跨域中间件的作用就是配置服务器以允许特定的跨域请求。这通常包括设置响应头，如Access-Control-Allow-Origin、Access-Control-Allow-Methods、Access-Control-Allow-Headers等，来告诉浏览器哪些源可以访问该资源，以及允许使用的HTTP方法和请求头等。
```bash
mkdir -p internal/logic/middleware
```
后续创建文件夹步骤部分内容省略，体现在代码文件注释中。
```go
// internal/logic/middleware/middleware.go

package middleware

import "github.com/gogf/gf/v2/net/ghttp"

type sMiddleware struct{}

func New() *sMiddleware {
	return &sMiddleware{}
}

func (s *sMiddleware) CORS(r *ghttp.Request) {
	r.Response.CORSDefault()
	r.Middleware.Next()
}
```
创建service
```bash
gf gen service
```
并修改middleware.go文件如下
```go
// internal/logic/middleware/middleware.go

package middleware

import (
	"zeal_be/internal/service"

	"github.com/gogf/gf/v2/net/ghttp"
)

type sMiddleware struct{}

func init() {
	service.RegisterMiddleware(New())
} // 用于服务初始化注册

func New() service.IMiddleware {
	return &sMiddleware{}
}

func (s *sMiddleware) CORS(r *ghttp.Request) {
	r.Response.CORSDefault()
	r.Middleware.Next()
}
```
后续只给出最终的logic代码文件，省略生成service与修改logic代码文件的步骤。

添加至cmd.go文件中
```go
// internal/cmd/cmd.go
s := g.Server() // 该行以上代码省略
s.Use(service.Middleware().CORS) // 添加该行，以全局使用跨域中间件，也可更细粒度配置
// ...
```
## mysql配置
**1、安装MySql库**
```bash
go get "github.com/gogf/gf/contrib/drivers/mysql/v2"
```
**2、导入包**
在main.go文件中添加
```go
// main.go
import (
	_ "zeal_be/internal/logic" // 该行以上代码省略
	_ "github.com/gogf/gf/contrib/drivers/mysql/v2" // 添加该行，以导入包
	// ...
)
```
3、配置数据库config文件
- 用于 `gf gen dao` 生成数据对象
所根据的配置文件存放于`/hack/config.yaml`中
```yaml
# /hack/config.yaml
gfcli:
  gen:
    dao:
    - link: "mysql:root:123dqz@tcp(192.168.56.102:3306)/zeal_be?loc=Local&parseTime=true"
      tables: "userdata" # 指定当前数据库中需要执行代码生成的数据表。如果为空，表示数据库的所有表都会生成。
      debug: true
      jsonCase: "CamelLower" # JSON字段命名方式，如CamelLower、SnakeLower等
```
- 程序启动时读取的配置文件。
该数据库配置文件存放于`/manifest/config/config.yaml`
```yaml
# /manifest/config/config.yaml
database:
  default:
  - link: "mysql:root:123dqz@tcp(192.168.56.102:3306)/zeal_be?loc=Local&parseTime=true"
    debug: true
```

我们创建的数据库名为zeal_be，用户信息存放于userdata表中。

用户信息应有：
- user_id 用户id
- user_name 用户名
- password  密码
- email_adress  邮箱地址
- ip_adress 登录ip地址，可以用于校验常用登录地址，保存5个 Json
- avatar_url    头像文件链接
- created_time   创建时间
- last_login_time   上次登录时间

其他数据可后续修改表，或者使用分表的方法。
```sql
-- 创建数据库
CREATE DATABASE zeal_be;

-- 使用数据库
USE zeal_be;

-- 创建userdata表
CREATE TABLE userdata (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email_adress VARCHAR(255) NOT NULL,
    ip_adress JSON,
    avatar_url VARCHAR(255),
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

准备好后，运行生成数据对象
```bash
gf gen dao
```
## 添加utility log工具
方便定位输出log的代码在文件中的位置。
```go
// utility/logTool.go
package utility

import (
	"context"

	"github.com/gogf/gf/v2/os/glog"
)

func Clog(v ...interface{}) {
	glog.Skip(1).Line(true).Info(context.TODO(), v...)
}
```


## 通用工具文件
```sh
zeal_be/utility/
├── cyptTool.go
├── fileTool.go
├── logTool.go
├── mongoTool.go
└── randCodes.go
```
## API
### admin
```sh
zeal_be/api/admin/v1/
├── get_self_privilege.go
├── get_user_list.go
├── get_user_privilege.go
└── update_user_privilege.go
```
```go
// get_self_privilege.go
package v1

import "github.com/gogf/gf/v2/frame/g"

type GetSelfPrivsReq struct {
	g.Meta `path:"/admin/get_self_privs" method:"get"`
}

type GetSelfPrivsRes struct {
	Privs []string `json:"privs_list"`
}
```

```go
// get_user_list.go
package v1

import "github.com/gogf/gf/v2/frame/g"

type UserListReq struct {
	g.Meta `path:"/admin/get_user_list" method:"post"`
	ULReqInfo
}

type ULReqInfo struct {
	PageSize  int    `p:"pageSize "`
	PageIndex int    `p:"pageIndex"`
	Order     string `p:"order"`
	OrderItem string `p:"orderItem"`
	NeedCount int    `p:"needCount"`
}

type UserInfo struct {
	User_ID         int    `json:"user_ID"`
	User_name       string `json:"user_name"`
	Email_address   string `json:"email_address"`
	Password        string `json:"password"`
	Created_time    string `json:"created_time"`
	Last_login_time string `json:"last_login_time"`
	Avatar_url      string `json:"avatar_url"`
	Ip_address      string `json:"ip_address"`
}

type UserListRes struct {
	User_list  []UserInfo `json:"user_list"`
	Count_num  int        `json:"count_num"`
}
```

```go
// get_user_privilege.go
package v1

import "github.com/gogf/gf/v2/frame/g"

type GetUserPrivsReq struct {
	g.Meta  `path:"/admin/get_user_privs" method:"post"`
	T_email string `p:"target_email"`
}

type GetUserPrivsRes struct {
	Privs []string `json:"privs_list"`
}
```

```go
// update_user_privilege.go
package v1

import "github.com/gogf/gf/v2/frame/g"

type UpdateUserPrivsReq struct {
	g.Meta  `path:"/admin/update_user_privs" method:"post"`
	T_email string   `p:"target_email"`
	Privs   []string `p:"privs_list"`
}

type UpdateUserPrivsRes struct {
	Privs []string `json:"privs_list"`
}
```
# 实时通讯系统

## golang如何实现单例
在Go语言中实现单例模式可以通过多种方式来完成。最常见的是使用包级别的变量和初始化函数，结合互斥锁（sync.Mutex）来确保线程安全。以下是几种常见的单例模式实现方式：
### 1. 静态单例

这种方式是最简单直接的，但不是线程安全的。适用于单线程环境或已经确保线程安全的场景。

```go
package singleton

type Singleton struct {
    // 单例对象的属性
    data string
}

var instance *Singleton

func GetInstance() *Singleton {
    if instance == nil {
        instance = &Singleton{data: "initial data"}
    }
    return instance
}
```
### 2. 懒汉式单例（线程安全）
使用互斥锁确保在多线程环境下实例化对象时的安全性。
```go
package singleton

import "sync"

type Singleton struct {
    // 单例对象的属性
    data string
}

var (
    instance *Singleton
    mu       sync.Mutex
)

func GetInstance() *Singleton {
    mu.Lock()
    defer mu.Unlock()
    if instance == nil {
        instance = &Singleton{data: "initial data"}
    }
    return instance
}
```
### 3. 双重检查锁定（Double-Checked Locking）
这种方式在提高性能的同时保持线程安全。
```go
package singleton

import (
    "sync"
    "sync/atomic"
)

type Singleton struct {
    // 单例对象的属性
    data string
}

var (
    instance *Singleton
    once     sync.Once
)

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{data: "initial data"}
    })
    return instance
}
```
### 4. 初始化时创建实例（饿汉式）
这种方式在包初始化时就创建了实例，所以它是线程安全的。
```go
package singleton

type Singleton struct {
    // 单例对象的属性
    data string
}

var instance *Singleton = &Singleton{data: "initial data"}

func GetInstance() *Singleton {
    return instance
}
```
### 5. 使用init函数创建实例
这种变体也是饿汉式的方式，并且使用init函数来创建实例。
```go
package singleton

type Singleton struct {
    // 单例对象的属性
    data string
}

var instance *Singleton

func init() {
    instance = &Singleton{data: "initial data"}
}

func GetInstance() *Singleton {
    return instance
}
```
> sync.Once是Go语言中实现线程安全单例的最佳实践，因为它简洁且高效。

## init函数介绍
在Go语言中，init函数是一个特殊的函数，用于在包被导入时执行初始化任务。以下是关于init函数的详细介绍：

**基本特性**
- 自动执行：init函数在包第一次被导入时自动执行，不需要显式调用。
- 包级别：init函数是包级别的，即每个包可以包含多个init函数，它们会在包初始化时按声明顺序依次执行。
- 灵活性：init函数通常用于初始化数据、设置默认值、注册某些组件等。
- 不可调用：init函数不能被显式调用；它们由Go运行时自动管理。
- 无参数和返回值：init函数没有参数和返回值。

**多个init函数**
一个包可以包含多个init函数。这些init函数会按它们在文件中的声明顺序执行，但是不同的文件中的init函数的执行顺序是未定义的。因此，通常建议在一个文件中使用一个init函数来避免潜在的问题。

**使用场景**
- 变量初始化：对于需要复杂初始化逻辑的变量，可以在init函数中进行。
- 注册组件：在某些框架中，需要注册各种组件（如插件、处理器等），可以在init函数中完成这些注册。
- 数据库连接：初始化数据库连接，以便在包中的其他函数使用。
- 配置加载：从配置文件中加载配置信息，并在程序运行期间使用。

**注意事项**
- 文件顺序：如果一个包中有多个文件，并且每个文件都有init函数，那么这些init函数的执行顺序与文件的导入顺序无关，而是与文件的编译顺序有关。
- 多包导入：如果一个程序导入了多个包，每个包的init函数会按照导入包的顺序依次执行。
- 避免循环导入：由于init函数的自动调用特性，需要注意避免循环导入问题，否则会导致编译错误。