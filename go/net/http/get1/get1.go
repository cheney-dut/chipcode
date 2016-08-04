// get1
package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	resp, err := http.Get("https://www.baidu.com")
	if err != nil {
		log.Fatal("http get error:", err)
	}
	defer resp.Body.Close()

	fmt.Println("Status =", resp.Status)
	fmt.Println("StatusCode =", resp.StatusCode)
	fmt.Println("Proto =", resp.Proto)
	fmt.Println("ProtoMajor =", resp.ProtoMajor)
	fmt.Println("ProtoMinor =", resp.ProtoMinor)
	fmt.Println("ContentLength =", resp.ContentLength)

	fmt.Println("")
	fmt.Println("cookie:")
	cookies := resp.Cookies()
	for _, cookie := range cookies {
		fmt.Printf("name=%s,\tvalue=%s,\tdomain=%s\n", cookie.Name, cookie.Value, cookie.Domain)
	}

	fmt.Println("-------------------------------------")
	body, err1 := ioutil.ReadAll(resp.Body)
	if err1 != nil {
		log.Fatal("http get body error:", err1)
	}
	fmt.Println(string(body))
}
