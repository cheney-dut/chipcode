// server
package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
)

func handleConnection(conn net.Conn) {
	data, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		log.Fatal("get client data error:", err)
	}
	fmt.Printf("%#v\n", data)
	fmt.Fprintf(conn, "hello client\n")
	conn.Close()
}

func main() {
	ln, err := net.Listen("tcp", "127.0.0.1:6010")
	if err != nil {
		panic(err)
	}
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Fatal("get client connection error:", err)
		}
		go handleConnection(conn)
	}
}
