// stringer
package main

import (
	"fmt"
	"math"
)

// 定义Abser接口
type Abser interface {
	Abs() float64
}

type MyFloat float64

// 为float64类型添加Abs方法，因而MyFloat类型实现了Abser接口
func (f MyFloat) Abs() float64 {
	if f < 0 {
		return float64(-f)
	}
	return float64(f)
}

type Stringer interface {
	String() string
}

func main() {
	var v Abser
	v = MyFloat(-math.Sqrt2)
	if sv, ok := v.(Stringer); ok {
		// note: sv, not v
		fmt.Printf("v implements String(): %s\n", sv.String())
	} else {
		fmt.Println("v does not implement String(): ", v.Abs())
	}
}
