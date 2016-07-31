// web1
package main

import (
	"fmt"
	"io"
	"net/http"
)

func hell(rw http.ResponseWriter, req *http.Request) {
	io.WriteString(rw, "hello world")
}

func HandleFunc(pattern string, handler func(ResponseWriter, *Request)) {
	DefaultServeMux.HandleFunc(pattern, handler)
}

func main() {
	fmt.Println("Hello World!")
}
