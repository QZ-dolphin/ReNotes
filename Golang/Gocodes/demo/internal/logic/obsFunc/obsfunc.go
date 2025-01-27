package obsfunc

import (
	"context"
	"demo/internal/service"
	"fmt"
)

type sObsfunc struct{}

func init() {
	service.RegisterObsfunc(New())
}

func New() *sObsfunc {
	return &sObsfunc{}
}

func (s *sObsfunc) GetList(ctx context.Context) {
	fmt.Println("This is GetList")
}
