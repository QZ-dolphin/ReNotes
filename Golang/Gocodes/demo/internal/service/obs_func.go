// ================================================================================
// Code generated and maintained by GoFrame CLI tool. DO NOT EDIT.
// You can delete these comments if you wish manually maintain this interface file.
// ================================================================================

package service

import (
	"context"
)

type (
	IObsfunc interface {
		GetList(ctx context.Context)
	}
)

var (
	localObsfunc IObsfunc
)

func Obsfunc() IObsfunc {
	if localObsfunc == nil {
		panic("implement not found for interface IObsfunc, forgot register?")
	}
	return localObsfunc
}

func RegisterObsfunc(i IObsfunc) {
	localObsfunc = i
}
