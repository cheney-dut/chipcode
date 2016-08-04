// http1
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
)

// 在请求的时候设置头参数、cookie之类的数据，就可以使用http.Do方法。
// 必须要设定Content-Type为application/x-www-form-urlencoded，post参数才可正常传递。
// 如果要发起head请求可以直接使用http client的head方法
func main() {
	client := &http.Client{}

	req, err := http.NewRequest("POST", "https://www.baidu.com", strings.NewReader("name=cjb"))
	if err != nil {
		log.Fatal("http error:", err)
	}

	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.Header.Set("Cookie", "name=anny")

	resp, err := client.Do(req)

	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal("http body error:", err)
	}

	fmt.Println(string(body))
}
