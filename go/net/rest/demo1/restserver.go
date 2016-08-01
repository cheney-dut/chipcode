// restserver
// routes其实是个路由框架，当你使用Get请求或Post请求请求转发好的地址时，它会根据相应路径，进行值拆分。不同的请求方式，将使用不同的路由去拆分。
// 可手动安装：
// go get github.com/drone/routes
// https://github.com/drone/routes
// 需提前配置git：
// Path: C:\Users\HongPan\AppData\Local\GitHub\PortableGit_d76a6a98c9315931ec4927243517bc09e9b731a0\mingw32\bin;
package main

import (
	"fmt"
	"net/http"
	"net/url"

	"github.com/drone/routes"
)

func getuser(w http.ResponseWriter, r *http.Request) {
	var params url.Values = r.URL.Query()
	var uid string = params.Get(":uid")
	fmt.Fprintln(w, "get a user", uid, "success!")
}

func getuserAndAge(w http.ResponseWriter, r *http.Request) {
	var params url.Values = r.URL.Query()
	var uid string = params.Get(":uid")
	var age string = params.Get(":age")
	fmt.Fprintln(w, "get a user", uid, "success! age is", age)
}

func edituser(w http.ResponseWriter, r *http.Request) {
	var params url.Values = r.URL.Query()
	var uid string = params.Get(":uid")
	fmt.Fprintln(w, "edit a user", uid, "success!")
}

/*
启动后访问示例：
http://127.0.0.1:8088/user/song
http://127.0.0.1:8088/user/song/32
http://127.0.0.1:8088/user/song
可用Poster插件发送post请求
*/
func main() {
	fmt.Println("正在启动WEB服务...")
	var mux *routes.RouteMux = routes.New()
	mux.Get("/user/:uid", getuser)
	mux.Get("/user/:uid/:age", getuserAndAge)
	mux.Post("/user/:uid", edituser)

	http.ListenAndServe(":8088", mux)
	fmt.Println("服务已停止")
}
