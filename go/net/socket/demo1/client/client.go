// client
package main

import (
	"bufio"
	"fmt"
	"net"
)

func main() {
	conn, err := net.Dial("tcp", "127.0.0.1:6010")
	if err != nil {
		panic(err)
	}
	defer conn.Close()

	msg := "hello server"
	//fmt.Println(os.Args)
	//if len(os.Args) > 1 {
	//	msg = os.Args[1]
	//}
	//fmt.Println("msg:", msg)

	fmt.Fprintf(conn, msg)
	data, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		panic(err)
	}
	fmt.Printf("%#v\n", data)
}
