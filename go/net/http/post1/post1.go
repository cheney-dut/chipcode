// post1
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
)

// 使用这个方法的话，第二个参数要设置成”application/x-www-form-urlencoded”，否则post参数无法传递。
func main() {
	resp, err := http.Post("https://www.baidu.com", "application/x-www-form-urlencoded", strings.NewReader("name=cjb"))
	if err != nil {
		log.Fatal("http get error:", err)
	}
	defer resp.Body.Close()

	body, err1 := ioutil.ReadAll(resp.Body)
	if err1 != nil {
		log.Fatal("http get body error:", err1)
	}
	fmt.Println(string(body))
}
