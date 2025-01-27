package main

import (
	_ "demo/internal/logic"

	"github.com/gogf/gf/v2/frame/g"
	"github.com/gogf/gf/v2/net/ghttp"
)

type Controller struct{}

func (c *Controller) Init(r *ghttp.Request) {
	r.Response.Writeln("Init")
}

func (c *Controller) Shut(r *ghttp.Request) {
	r.Response.Writeln("Shut")
}

func (c *Controller) Hello(r *ghttp.Request) {
	r.Response.Writeln("Hello")
}

func main() {
	s := g.Server()
	c := new(Controller)
	s.BindObject("/object", c)
	s.SetPort(8199)
	s.Run()
}
