// implements-demo1
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

// 自定义Vertex类型
type Vertex struct {
	X, Y float64
}

// 实现Abs()方法，导致 *Vertex实现了Abser接口
// 指针传递Vertex类型，若以非指针方式（func (v Vertex) Abs()）定义，Vertex也实现了Abser接口
func (v *Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
	var a Abser
	f := MyFloat(-math.Sqrt2)
	fmt.Println("f =", f)

	v := Vertex{X: 3, Y: 4}

	a = f // a MyFloat implements Abser
	fmt.Println(a.Abs())

	a = &v // a *Vertex implements Abser
	fmt.Println(a.Abs())

	// a = v // a Vertex, does NOT implement Abser
	// fmt.Println(a.Abs())
}
