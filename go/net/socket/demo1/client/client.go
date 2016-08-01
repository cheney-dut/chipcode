// client
package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
)

func main() {
	msg := "hell server\n"
	fmt.Println(os.Args)
	if len(os.Args) > 1 {
		msg = os.Args[1]
	}
	fmt.Println("msg:", msg)

	conn, err := net.Dial("tcp", "127.0.0.1:6010")
	if err != nil {
		panic(err)
	}
	fmt.Fprintf(conn, msg)
	data, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		panic(err)
	}
	fmt.Printf("%#v\n", data)
}
