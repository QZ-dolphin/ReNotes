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

## 空值处理
用到`dao`与`entity`两个包
```go
// internal/controller/hello/hello.go
func (c *Hello) Db(req *ghttp.Request) {
	md := dao.Book.Ctx(req.Context())

	book := entity.Book{
		Author: "王强",
		Price:  88.88,
	}
	// req.Response.WriteJsonExit(book) 查看book内容
	// 更新完后，其他字段变成空`NULL`值。

	result, err := md.Where("id", 16).Data(book).Update()

	if err == nil {
		req.Response.WriteJson(result)
	} else {
		req.Response.Writeln("发生错误：" + err.Error())
	}
}
// 函数修改 将字段更新
book := entity.Book{
		Name: "Go语言从入门到精通",
		Id:   25,
	}
result, err := md.Where("id", 0).Fields("id", "name").Data(book).Update()

// 更新时忽略空值，即没有给出值的字段
book := entity.Book{
		Price: 65.55,
	}
result, err := md.OmitEmpty().Data(book).Update()

// 使用do.Book，更新后其他字段不会变成空值
book := do.Book{
		Price: 66.66,
	}
result, err := md.Where(do.Book{Id: 25}).Data(book).Update() // 查询条件字段可以有多个
```

## 关联查询
### 一对一
```go
// internal/controller/hello/hello.go
func (c *Hello) Db(req *ghttp.Request) {
	md := dao.Emp.Ctx(req.Context())

	var emps []entity.Emp

	err := md.With(entity.Dept{}).Scan(&emps) // With表示要关联Dept表，可以用,分隔多个关联的表

	if err == nil {
		req.Response.WriteJson(emps)
	} else {
		req.Response.Writeln("发生错误：" + err.Error())
	}
}
```
```go
// internal/model/entity/emp.go
type Emp struct {
	Id     uint   `json:"id"      orm:"id"      ` // ID
	DeptId uint   `json:"dept_id" orm:"dept_id" ` // 所属部门
	Name   string `json:"name"    orm:"name"    ` // 姓名
	Gender int    `json:"gender"  orm:"gender"  ` // 性别: 0=男 1=女
	Phone  string `json:"phone"   orm:"phone"   ` // 联系电话
	Email  string `json:"email"   orm:"email"   ` // 邮箱
	Avatar string `json:"avatar"  orm:"avatar"  ` // 照片

	Dept *Dept	`json:"dept" orm:"with:id=dept_id"` // 新增字段关联，让被关联的表中id=当前表中dept_id
	// 可以增加多个关联字段
}

```
### 一对多
```go
// internal/model/entity/dept.go
type Dept struct {
	Id     uint   `json:"id"     orm:"id"     ` // ID
	Pid    uint   `json:"pid"    orm:"pid"    ` // 上级部门ID
	Name   string `json:"name"   orm:"name"   ` // 部门名称
	Leader string `json:"leader" orm:"leader" ` // 部门领导
	Phone  string `json:"phone"  orm:"phone"  ` // 联系电话

	Emps []Emp `json:"emps" orm:"with:dept_id=id"`
}
```
```go
// internal/controller/hello/hello.go
func (c *Hello) Db(req *ghttp.Request) {
	md := dao.Dept.Ctx(req.Context())

	var depts []entity.Dept

	err := md.With(entity.Emp{}, entity.Hobby{}).Scan(&depts) 
	// 可以嵌套关联，但要防止无限循环套死

	if err == nil {
		req.Response.WriteJson(depts)
	} else {
		req.Response.Writeln("发生错误：" + err.Error())
	}
}
```
可自定义查询字段
```go
// internal/controller/hello/hello.go
func (c *Hello) Db(req *ghttp.Request) {
	type MyDept struct {
		g.Meta `orm:"table:dept"` // 指定对应的表
		Id     uint               `json:"id"`   // ID
		Name   string             `json:"name"` // 部门名称
	}

	type MyEmp struct {
		g.Meta `orm:"table:emp"`
		Id     uint   `json:"id"`      // ID
		DeptId uint   `json:"dept_id"` // 所属部门
		Name   string `json:"name"`    // 姓名
		Phone  string `json:"phone"`   // 联系电话

		Dept *MyDept `orm:"with:id=dept_id" json:"dept"`
	}

	md := dao.Emp.Ctx(req.Context())

	var emps []MyEmp

	err := md.With(MyDept{}).Scan(&emps)

	if err == nil {
		req.Response.WriteJson(emps)
	} else {
		req.Response.Writeln("发生错误：" + err.Error())
	}
}
```
## service与logic目录使用
差不多一个entity对应一个service

service文件定义
```go
// internal/service/book.go
package service

import (
	"context"
	"demo/internal/model/do"
	"demo/internal/model/entity"
)

// 1.定义接口
type IBook interface {
	GeList(ctx context.Context) (books []entity.Book, err error)
	Add(ctx context.Context, book do.Book) (err error)
	Edit(ctx context.Context, book do.Book) (err error)
	Del(ctx context.Context) (err error)
}

// 2.定义接口变量
var localBook IBook

// 3.定义一个获取接口实例的函数
func Book() IBook {
	if localBook == nil {
		panic("IBook接口未实现或未注册")
	}
	return localBook
}

// 4.定义一个接口实现的注册方法
func RegisterBook(i IBook) {
	localBook = i
}

```
在logic中定义方法实现，在logic文件夹下习惯将每一个文件放在对应文件夹下。
```go
// internal/logic/book/book.go
package book

import (
	"context"
	"demo/internal/dao"
	"demo/internal/model/do"
	"demo/internal/model/entity"
	"demo/internal/service"
)

type sBook struct {
}

// Add implements service.IBook.
func (s *sBook) Add(ctx context.Context, book do.Book) (err error) {
	panic("unimplemented")
}

// Del implements service.IBook.
func (s *sBook) Del(ctx context.Context) (err error) {
	panic("unimplemented")
}

// Edit implements service.IBook.
func (s *sBook) Edit(ctx context.Context, book do.Book) (err error) {
	panic("unimplemented")
}

// GeList implements service.IBook.
func (s *sBook) GeList(ctx context.Context) (books []entity.Book, err error) {
	err = dao.Book.Ctx(ctx).Scan(&books)
	return
}

func init() {
	service.RegisterBook(&sBook{})
}
```
分别在`internal/logic/logic.go`文件与`main.go`文件中导入定义的包，以初始化
```go
// internal/logic/logic.go
import (
	_ "demo/internal/logic/book"
)
```
```go
// main.go
import (
	_ "demo/internal/logic"
)
```
## 模板输出
```go
// internal/controller/hello/hello.go
func (c *Hello) Tpl(req *ghttp.Request) {
	data := g.Map{
		"name":   "王也道长",
		"lesson": "GoFrame入门课程",
		"num":    5,
		"what":   "模板引擎使用示例",
	}

	req.Response.WriteTpl("hello/index.html", data)
	// 第一个参数为文件路径
}
```
html文件存放于`resource/template/hello/index.html`
```html
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>

    <div>
        <h1>你好， {{.name}}</h1>
        <h2>欢迎来到{{.lesson}}的学习课程</h2>
        <p>本课程共{{.num}}小节，现在学习的是{{.what}}</p >
    </div>

</body>
</html>
```
对应的替换内容的格式为`{{.名称}}`

## 模板条件判断与循环
在html文件中可写入
```html
{{if .condition}}
条件满足时显示内容
{{else}}
条件不满足时显示内容
{{end}}
```
可以嵌套写，也可以写多个`{{else if .condition}}`

当`.condition`为空值，即0、""、nil这类值时，条件判断为假，其他值均为真（条件满足）。

大小判断用`eq nq lt le gt ge`
如`{{if eq .num 200}}`等价于`if .num==200`
注意判断关键字在两个值之前。

逻辑判断`and or not`，嵌套判断用括号隔离

### 循环
`range ... end`
对于数组变量`.slice`
两种方式：
```html
{{range .slice}}
<span>{{.}}</span>  
<!-- .用于输出简单类型变量 -->
{{end}}


{{range $index, $value := .slice}}
<p>index = {{$index}}, value = {{$value}}</p >
{{end}}
```
## 模板其他内容
将`css js image`等资源放置于`resource/public/resource/`下的对应文件夹。

开启静态文件服务，于`cmd/cmd.go`中添加`s.SetServerRoot("resource/public")`
或者用配置开启，于`manifest/config/config.yaml`中的`server: serverRoot:`添加路径。

## 文件上传
`public/html/form.html`
```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="ufile" id="">
            <input type="submit" text="提交">
        </form>
    </body>
</html>
```

```go
// internal/controller/hello/hello.go
func (c *Hello) Upload(req *ghttp.Request) {
	file := req.GetUploadFile("ufile")
	if file != nil {
		file.Filename = "111.png"                            
		// 自定义保存的文件名
		filename, err := file.Save("resource/public/upload") 
		// 自定义存放的路径
		if err == nil {
			req.Response.Writeln("upload"+filename)
		}
	}
}
```
### 获取多文件
修改html中
```html
<input type="file" name="ufiles" id="" multiple>
```

```go
// internal/controller/hello/hello.go
func (c *Hello) Upload(req *ghttp.Request) {
	files := req.GetUploadFiles("ufiles")
	if files != nil {
		filenames, err := files.Save("resource/public/upload")
		if err == nil {
			req.Response.Writeln(filenames)
		}
	}
}
```
### 修改文件大小限制
于`manifest/config/config.yaml`中修改`server:clientMaxBodySize:`
`0`为无限制

## 文件下载
```go
// internal/controller/hello/hello.go
func (c *Hello) Download(req *ghttp.Request) {
	req.Response.ServeFile("/resource/public/upload/111.png")
}
// 图片、文本等可显示文件会显示在浏览器中，其他则download下来，文件名为download

req.Response.ServeFileDownload("/resource/public/upload/111.png")
// 直接将文件下载，可加第二个可选参数，为下载保存的文件名
```
## Cookie和Session
Cookie是保存在浏览器的一些数据，在请求的时候会放在请求头当中一同发送，通常用来保存sessionid、token等一些数据。

Session机制用于判断请求由哪一用户发起，Session数据保存在服务器。
以前常用于保存登录数据，进行登录验证，不过现在只是有些比较小的，前后端不分离的项目还在使用。
## 数据校验
```go
// api/hello/hello.go
type ValidReq struct {
	g.Meta `method:"all"`

	UserName string `p:"user_name" v:"required#user_name不能为空"`
	// v用于验证，required必填，#后加提示信息
	Password string `p:"password"`
	Age      int    `p:"age" v:"required|integer|min:0#age不能为空|age必须是整数|age不能小于0"`
	// 验证规则用|隔开，提示信息对应，用|隔开
}

type ValidRes struct {
}
```

```go
// internal/controller/hello/hello.go
func (c *Hello) Valid(ctx context.Context, req *hello.ValidReq) (res *hello.ValidRes, err error) {
	return
}
```
## 时间与随机工具
当前时间
```go
t := gtime.Now()
t := gtime.Date()
t := gtime.Datetime()
```

## 中间件
```go
// 注册中间件，对路由组进行注册，可注册多个
group.Middleware(service.Middleware().Auth)
```
Auth中间件在`internal/service/middleware.go`中
具体实现在`internal/logic/middleware/middleware.go`中

`r.Middleware.Next()`功能为路由放行
在`r.Middleware.Next()`前面的称为`前置中间件`,用于拦截请求
放在后面的为`后置中间件`，用于拦截响应

## 接口文档
生成的地址`http://127.0.0.1:8000/swagger/`，接口文档的页面，写在`api`中的文件。

可自定义接口文档页面，于`resource/template/apidoc.html`中

## 构建打包
在`hack/config.yaml`文档中
```yaml
gfcli:
  build:
    name: "hellogf"
    arch: "amd64"
    system: "linux,darwin,windows"
    mode: "none"
    cgo: 0
    packSrc: "manifest/config,resource/public,resource/template"
    version: "1.0.0"
    output: "./bin"
    extra: ""
```
- name：打包后的可执行文件名
- arch：系统架构，可以有多个，用,分隔，用all表示编译所有支持的架构
- system：编译平台，可以有多个，用,分隔，用all表示编译所有支持的系统
- packSrc：需要打包的静态资源目录
- version：版本号

打包
```shell
gf build
```
以上操作会把指定的目录一起打包进可执行文件。通常情况例如配置文件等一些需要改动的文件不用打包进可执行文件。