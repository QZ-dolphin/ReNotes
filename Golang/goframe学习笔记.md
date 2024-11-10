# goframe学习笔记
## 项目初始化
```batch
gf init 项目名 -u
REM -u 代表最新框架版本更新

cd 项目名
gf run main.go
```

## 路由注册
在`cmd.go`文件下

基本用法
```go
s := g.Server()
s.BindHandler("访问路径", 处理函数)
```
- 访问路径为`/.../...`类型
- 处理函数
  ``` go
  func(r *ghttp.Request){
    r.Response.Writeln("Hello")
  }
  ```

函数绑定：可以直接绑定匿名函数，也可以定义函数后进行传入。
```go
func handler(r *ghttp.Request){
    r.Response.Writeln("Hello")
}
s.BindHandler("/he", handler)
```

对象方法绑定：在controller文件夹中的.go文件中定义对象和对象方法。
```go
// hello.go
type Hello struct{}

// 定义初始化方法
func NewHello() *Hello {
	return &Hello{}
}

func (c *Hello) SayHello(r *ghttp.Request) {
	r.Response.Writeln("Hello GoFrame")
}
```

定义实例化对象，再传入对象方法
```go
hello := hello.NewHello()
s.BindHandler("/say", hello.SayHello)
```

### 指定方法
修改路由注册的访问路径为`方法:路径`

### 批量绑定
控制器`controller`中的对象
```go
s.BindObject("上层访问路径", 对象地址) // 绑定对象所有方法
s.BindObject("上层访问路径", 对象地址, "对象方法，逗号隔开") // 绑定对象部分方法
s.BindObjectMethod("访问路径", 对象地址, "对象单个方法") // 绑定对象该方法至访问路径上
s.BindObjectRest("访问路径", 对象地址) // 只绑定http原有方法，通过 `方法:路径` 访问
```
### 分组路由
在分组中绑定对象的所有方法，用的是group.Bind(初始化对象)，与批量绑定中的方法s.BindObject()不同

```go
s.Group("/user", func(group *ghttp.RouterGroup) {
	group.Middleware(ghttp.MiddlewareHandlerResponse)
	group.Bind(
		user.New(),
                hello.NewHello(),
    )
})
// "/user"为路由分组路径
// user.New() 为分组绑定的对象
// 可以绑定多个对象
```
嵌套分组
```go
s.Group("/api", func(group *ghttp.RouterGroup) {
	group.Middleware(ghttp.MiddlewareHandlerResponse)
	group.Group("/hello", func(group1 *ghttp.RouterGroup) {
		group1.Bind(
			hello.NewHello(),
		)
	})
	group.Group("/user", func(group1 *ghttp.RouterGroup) {
		group1.Bind(
			user.New(),
		)
	})
})
```

可以在分组中单独注册 Get, Post方法等
```go
s.Group("/api", func(group *ghttp.RouterGroup) {
	group.Middleware(ghttp.MiddlewareHandlerResponse)
	group.GET("访问路径", 处理函数)
        group.POST("访问路径", 处理函数)
})
```
### 规范路由
处理函数的另一种写法
```go
func Handler(ctx context.Context, req *Request)(res *Response err error)
```
可以定义返回的数据结构`Response`
```go
type AddReq struct {
	g.Meta `path:"adduser" method:"get"` // 不写path直接用调用函数的方法名作为路由，加path标签则给方法绑定路由地址
}
type AddRes struct {
	// 返回类型结构体
	Name string
	Age  int
}

// 请求和返回结构应写在api中

func (c *Controller) Add(ctx context.Context, req *AddReq) (res *AddRes, err error) {
	res = &AddRes{
		Name: "dongqingzhen",
		Age:  10,
	} // 为返回的json数据中的data
	g.RequestFromCtx(ctx).Response.Writeln("Hello")
	// 返回自定义的数据，与json数据返回冲突
	return
}
```
自动转换通过中间件实现

在api中通常定义请求和返回的结构体

## GET 请求参数获取
在goframe中接受传过来的参数
```go
func (c *Hello) Params(ctx context.Context, req *hello.ParamsReq) (res *hello.ParamsRes, err error) {
	r := g.RequestFromCtx(ctx)
	name := r.GetQuery("name") // 返回类型gvar.Var范型
	r.Response.Writeln(name)
	return
}
```
gvar.Var范型 在运算时需要进行类型转换
```go
func (c *Hello) Params(ctx context.Context, req *hello.ParamsReq) (res *hello.ParamsRes, err error) {
	r := g.RequestFromCtx(ctx)
	name := r.GetQuery("name", "dongqingzhen") // 获取指定传入参数，第二个参数为默认值
	// name := r.GetQuery("name")
	r.Response.Writeln(name.String() + "你好")
        
    // 获取全部传入参数
	data := r.GetQueryMap() 
	r.Response.Writeln(data)
	// 获取指定部分值
	// data1 := r.GetQueryMap(map[string]interface{}{"name": "李四", "age": 100})
	data1 := r.GetQueryMap(g.Map{"name": "李四", "age": 100})
	// g.Map为map[string]interface{}的简写形式
	r.Response.Writeln(data1)
	return
}
```

## 非Get 请求参数
html文件放置在`resource/public/html`路径下
绑定静态资源服务`s.SetServerRoot("resource/public")`

在浏览器输入 http://127.0.0.1:8000/html/form.html 即可访问。
```HTML
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <form action="/api/hello/params" method="POST">
            用户名：<input type="text" name="user_name"/> <br/>
            密码：<input type="password" name="password"/> <br/>
            年龄：<input type="number" name="age"/> <br/>
            <input type="submit" text="提交">
        </form>
    </body>
</html>
```
注意action路径为绑定的路由。
```go
func (c *Hello) Params(ctx context.Context, req *hello.ParamsReq) (res *hello.ParamsRes, err error) {
	r := g.RequestFromCtx(ctx)
	data := r.GetForm("user_name") // 获取单个值
	r.Response.Writeln(data)
	data1 := r.GetFormMap() // 获取全部值
	r.Response.Writeln(data1)
	return
}
```
定义结构体获取
```go
func (c *Hello) Params(ctx context.Context, req *hello.ParamsReq) (res *hello.ParamsRes, err error) {
	r := g.RequestFromCtx(ctx)
	type user struct {
		UserName string
		Age      int
		Password string
	}

	var u user

	err = r.ParseForm(&u) // 传入结构体
	if err == nil {
		r.Response.Writeln(u)
	}
	return
}
```
## 动态路由参数
```go
// api/hello/hello.go
type ParamsReq struct {
	g.Meta `path:"/params/{name}/{id}.html" method:"all"`
}
```
```go
func (c *Hello) Params(ctx context.Context, req *hello.ParamsReq) (res *hello.ParamsRes, err error) {
	r := g.RequestFromCtx(ctx)
	name := r.GetRouter("name") // 获取单个路由参数，与动态路由名匹配
	r.Response.Writeln(name)
	name1 := r.GetRouterMap() // 获取所有路由参数
	r.Response.Writeln(name1)
	return
}
```
## 所有请求参数获取
```go
func (c *Hello) Params(ctx context.Context, req *hello.ParamsReq) (res *hello.ParamsRes, err error) {
	r := g.RequestFromCtx(ctx)
	data := r.GetRequestMap() // 获取所有请求参数 r.GetMap()为其简写形式 r.Get("参数名")获取单个参数
	r.Response.Writeln(data)

	type user struct {
		UserName string
		Age      int
		Password string
	}

	var u user
	err = r.Parse(&u) // 传入结构体，解析所有参数
	if err == nil {
		r.Response.Writeln(u)
	}
	return
}
```

## API 参数
```go
// api/hello/hello.go
type ParamsReq struct {
	g.Meta `path:"/params" method:"all"`

	UserName string
	Password string
	Age      int
}

// internal/controller/hello/hello.go
func (c *Hello) Params(ctx context.Context, req *hello.ParamsReq) (res *hello.ParamsRes, err error) {
	r := g.RequestFromCtx(ctx)
	r.Response.Writeln(req) // 结构体直接接受数据
	return
}
```
对于有格式差别的参数名也能实现转换，但可以指定结构体中参数对应的标签名
```go
// api/hello/hello.go
type ParamsReq struct {
	g.Meta `path:"/params" method:"all"`

	UserName string `param:"name" d:"张三"` // param可简写为p， d为默认值
	Password string
	Age      int
}
```

## 响应输出
不指定结构体path，那么多个方法可以共用同一套请求和响应的结构体
```go
type ParamsReq struct {
	g.Meta `method:"all"`

	UserName string `param:"name" d:"张三"`
	Password string
	Age      int
}
```
```go
func (c *Hello) Respons(ctx context.Context, req *hello.ParamsReq) (res *hello.ParamsRes, err error) {
	r := g.RequestFromCtx(ctx)
	r.Response.Writef("<h1>hello %s, age %d</h1>", req.UserName, req.Age)
	return
}
```
`r.Response.WritelnExit()`表示输出后退出，不执行后续输出。
`r.Response.WriteJson(req)`返回json数据

## API 响应输出
```go
type ParamsRes struct {
	UserName string `json:"user_name"`
	Password string `json:"pwd"`
	Age      int    `json:"age"`
}
```
```go
func (c *Hello) Respons(ctx context.Context, req *hello.ParamsReq) (res *hello.ParamsRes, err error) {
	res = &hello.ParamsRes{
		UserName: "东东",
		Password: "123456",
		Age:      10,
	}
	return
}
```
通过中间件实现`group.Middleware(ghttp.MiddlewareHandlerResponse)`
只要err不为空，则code错误码和message不为0

## 数据库准备工作
配置文件存放于`/manifest/config/config.yaml`
```yaml
database:
  type: "mysql"
  host: "127.0.0.1"
  port: "3306"
  user: "root"
  pass: "123dqz"
  name: "goframe"
  timezone: "Asia/Shanghai"
  debug: true
```
简写形式
type:user:password@tcp(host:prot)/dbname?param1=value1&..
```yaml
database:
  debug: true
  link: "mysql:root:root@tcp(127.0.0.1:3306)/goframe?loc=Local&parseTime=true"
```
添加数据库驱动
```batch
go get -u github.com/gogf/gf/contrib/drivers/mysql/v2
```
导入
```go
// main.go
_ "github.com/gogf/gf/contrib/drivers/mysql/v2"
```

使用
```go
func (c *Hello) Db(req *ghttp.Request){
	req.Response.Writeln(g.Model("book"))
}
```

## 查询一条数据
```go
func (c *Hello) Db(req *ghttp.Request) {
	md := g.Model("book")
	book, err := md.One() // 返回的是map[string]Value 类型的Record数据
	if err == nil {
		req.Response.Writeln(book["id"])
	}
}
```
## 查询所有数据
```go
func (c *Hello) Db(req *ghttp.Request) {
	md := g.Model("book")
	books, err := md.All() // 查询所有数据，返回的是Record切片
	if err == nil {
		req.Response.WriteJson(books)
		req.Response.WriteJson(books[0]["name"])
	}
}
```
## 查询字段与常用设计
```go
func (c *Hello) Db(req *ghttp.Request) {
	md := g.Model("book")
	books, err := md.Fields("id,name").All() // Fields查询字段数据，里面内容可分开写"id","name"
	//FieldsEx("id,name") 排除对应字段
	if err == nil {
		req.Response.WriteJson(books)
	}
}

books, err := md.Value("name") // 查询该字段的一条数据
books, err := md.Array("name") // 查询该字段的所有数据
```

```go
func (c *Hello) Db(req *ghttp.Request) {
	// md := g.Model("book")
	min, err := g.Model("book").Min("price")
	max, err := g.Model("book").Max("price")
	avg, err := g.Model("book").Avg("price")
	count, err := g.Model("book").Count()
	if err == nil {
		req.Response.WriteJson(
			g.Map{
				"min":   min,
				"max":   max,
				"avg":   avg,
				"count": count,
			})
	}
}
```
## 查询条件
```go
func (c *Hello) Db(req *ghttp.Request) {
	md := g.Model("book")
	books, err := md.Where("id", 3).All() // 查询id = 3的数据
	if err == nil {
		req.Response.WriteJson(books)
	}
	books, err = md.Where("id<", 3).All() // 查询id < 3的数据
	books, err = md.Where("id<?", 3).All() // 查询id < 3的数据 用占位符？填充
	books, err = md.WhereLT("id", 3).All() // 查询id < 3的数据
	books, err = md.WhereLTE("id", 3).All() // 查询id <= 3的数据
	books, err = md.WhereGT("id", 3).All() // 查询id > 3的数据 还有WhereGTE方法
	// 链式方法
	books, err = md.WhereGTE("id", 2).WhereLTE("id", 4).All()
}
```
## 排序与分组
```go
func (c *Hello) Db(req *ghttp.Request) {
	md := g.Model("book")
	books, err := md.Order("price", "DESC").All()	// price降序排列
	if err == nil {
		req.Response.WriteJson(books)
	}
	books, err = md.Order("price", "DESC").Order("id", "ASC").All() // 排序链式组合

	// 分组 Group("字段名")
}
```
## 分页
```go
func (c *Hello) Db(req *ghttp.Request) {
	md := g.Model("book")
	books, err := md.Limit(3).All() // 限制只查3条数据
	if err == nil {
		req.Response.WriteJson(books)
	}
	books, err = md.Limit(3, 4).All() // 从第3条数据查4条数据
	books, err = md.Page(1, 3).All() // 查询页数（从1开始）和每一页的数据量
}
```
## 查询结果转为结构体
```go
func (c *Hello) Db(req *ghttp.Request) {
	type Book struct {
		Id          uint `json:"id"`
		BookName    string `orm:"name"` // orm 对应数据库中的字段名
		Author      string
		Price       float64
		PublishTime *gtime.Time
	}
	var book Book

	md := g.Model("book")
	err := md.Scan(&book) // 只查询到单条数据，若book定义为数据，则能查到全部数据var book []Book
	if err == nil {
		req.Response.WriteJson(book)
	}
}
```

## 数据插入
```go
func (c *Hello) Db(req *ghttp.Request) {
	// 定义插入的数据
	data := g.Map{
		"name":         "Linux驱动开发入门与实践",
		"author":       "郑强",
		"price":        69,
		"publish_time": "2023-10-10",
	}

	md := g.Model("book")
	result, err := md.Data(data).Insert() // 或简写为 md.Insert(data)

	if err == nil {
		req.Response.WriteJson(result)
	}
	result, err = md.Replace(data) // 主键冲突则替换原数据
	result, err = md.Save(data) // 主键冲突则更新原数据

}
```

```go
func (c *Hello) Db(req *ghttp.Request) {
	type Book struct {
		Id          uint   `json:"id"`
		BookName    string `orm:"name"` // orm 对应数据库中的字段名
		Author      string
		Price       float64
		PublishTime *gtime.Time
	}
	// 定义插入的数据
	data := Book{
		Id:          11,
		BookName:    "Linux驱动开发入门与实践",
		Author:      "郑强",
		Price:       33,
		PublishTime: gtime.New("2023-10-10"),
	}

	md := g.Model("book")
	result, err := md.Insert(data) // 或简写为 md.Insert(data)

	if err == nil {
		req.Response.WriteJson(result)
	}
}

result, err := md.InsertGetId(data) // 插入后返回主键ID
```
批量插入多条数据
```go
// 插入Map 类型数据
data := g.List{
	g.Map{...},
	g.Map{...},
}
// 插入结构体数据
data := g.Array{
	Book{...},
	Book{...},
}
```
## 数据更新
```go
func (c *Hello) Db(req *ghttp.Request) {
	type Book struct {
		Id          uint   `json:"id"`
		BookName    string `orm:"name"` // orm 对应数据库中的字段名
		Author      string
		Price       float64
		PublishTime *gtime.Time
	}
	// 定义更新的数据
	data := g.Map{
		"price":        55.333,
		"publish_time": gtime.New("2023-11-11"),
	}

	md := g.Model("book")
	result, err := md.Where(g.Map{
		"author": "郑强",
		"price":  69.3,
	}).Data(data).Update() // 或直接写为 .Update(data)

	if err == nil {
		req.Response.WriteJson(result)
	} else {
		req.Response.Writeln("发生错误：" + err.Error())
	}
}

result, err := md.WhereLT("id", 10).Increment("price", 10) // 每条数据该字段都增加10
result, err = md.WhereGT("id", 10).Decrement("price", 10)
```
## 数据删除
```go
result, err := md.WhereGT("id", 10).Delete()
```

## 时间维护与软删除
- `created_at`
- `update_at`
- `delete_at`
有了`delete_at`字段，则`delete()`则为软删除，只会增加删除时间，查询时，会过滤该字段不为空的数据。
当数据表中有deleted_at字段时，使用Delete方法时不会物理删除数据，只是更新deleted_at字段的值。查询数据时，会自动加上WHERE `deleted_at` IS NULL这一条件，过滤掉已被“删除”的数据。

如果需要查询所有数据，需要使用Unscoped方法
`ls, _ := md.Unscoped().All()`

## 事务
两种方式
一、手动提交
```go
func (c *Hello) Db(req *ghttp.Request) {
	data := g.Map{
		"name":         "Linux驱动开发入门与实践",
		"author":       "郑强",
		"price":        79.3,
		"publish_time": gtime.New("2023-10-10"),
	}

	tx, err := g.DB().Begin(req.Context()) // 开启事务
	if err != nil {
		req.Response.WritelnExit("发生错误：" + err.Error())
	}

	md := tx.Model("book")

	result, err := md.Insert(data)
	if err == nil {
		tx.Commit()	// 事务提交
		req.Response.WriteJson(result)
	} else {
		tx.Rollback()	// 事务回滚
		req.Response.Writeln("发生错误：" + err.Error())
	}
}
```
二、自动提交
```go
func (c *Hello) Db(req *ghttp.Request) {
	data := g.Map{
		"name":         "Linux驱动开发入门与实践",
		"author":       "郑强",
		"price":        79.3,
		"publish_time": gtime.New("2023-10-10"),
	}

	g.DB().Transaction(context.TODO(), func(ctx context.Context, tx gdb.TX) error {
		md := tx.Model("book")
		result, err := md.Insert(data)

		if err == nil {
			req.Response.WriteJson(result)
		} else {
			req.Response.Writeln("发生错误：" + err.Error())
		}

		return err // 只要err不为空，则会自动回滚，为空，则会自动提交
	})
}
```
## 执行sql
```go
func (c *Hello) Db(req *ghttp.Request) {
	sql := "SELECT * FROM `book` WHERE `id` > ? AND `id` < ?"
	db := g.DB()
	result, err := db.Query(req.Context(), sql, g.Array{3, 7}) // 查询语句

	if err == nil {
		req.Response.WriteJson(result)
	} else {
		req.Response.Writeln("发生错误：" + err.Error())
	}
}

sql := "INSERT INTO `book` (`name`, `author`, `price`) VALUES (?, ?, ?)"
result, err := db.Exec(req.Context(), sql, g.Array{"Go语言从入门到精通","Go语言研讨组", 99.38})	// 执行插入语句
// 只有在执行model的方法时会自动填充create,update和delete字段，执行sql时不会自动填充
```

## DAO 代码生成
在目录`/hack/config.yaml`中配置，在开发阶段用到
配置文件
```yaml
gfcli:
  gen:
    dao:
      link: "mysql:root:123dqz@tcp(127.0.0.1:3306)/goframe?loc=Local&parseTime=true"
      tables: "book, user, emp, dept, hobby"
```
运行
```batch
gf gen dao

REM 或者配置makefile环境后运行
make dao
```
service 放接口
logic 放实现

## DAO 基本应用
通过g.Model("表名")获得的model，每个条件where都会对其有影响。
```go
func (c *Hello) Db(req *ghttp.Request) {
	md := g.Model("book")

	md.WhereGT("id", 2)
	md.WhereLT("id", 6)
	// SELECT * FROM `book` WHERE ((`id` > 2) AND (`id` < 6)) AND `delete_at` IS NULL
	result, err := md.All()

	if err == nil {
		req.Response.WriteJson(result)
	} else {
		req.Response.Writeln("发生错误：" + err.Error())
	}
}
```
通过dao生成model
```go
md := dao.Book.Ctx(req.Context())
// SELECT * FROM `book` WHERE `delete_at` IS NULL
```
则前后不会有关联