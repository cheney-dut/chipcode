// post2
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
)

func main() {
	resp, err := http.PostForm("https://www.baidu.com", url.Values{"key": {"Value"}, "id": {"123"}})
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
