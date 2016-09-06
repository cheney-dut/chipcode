// filesize
package main

import (
	"fmt"
	"os"
	"path/filepath"
	"reflect"
)

// 获取文件或文件夹大小
func getFilelist(path string) {
	var folderSize int64

	err := filepath.Walk(path, func(filename string, fi os.FileInfo, err error) error {
		if fi.IsDir() { // 忽略目录
			return nil
		}

		folderSize = folderSize + fi.Size()
		fmt.Printf("%v \t %v \n", formateSize(fi.Size()), filename)
		return nil
	})

	if err != nil {
		fmt.Printf("filepath.Walk() returned %v \n", err)
	} else {
		fmt.Printf("folderSize: %s \n", formateSize(folderSize))
	}
}

func formateSize(size int64) string {
	//var g int64
	var g, result float64
	g = 1024
	result = float64(size)

	index := 0

	for result > g {
		result = result / g
		index++
	}

	switch index {
	case 0:
		return fmt.Sprintf("%v B", result)
	case 1:
		return fmt.Sprintf("%.2f K", result)
	case 2:
		return fmt.Sprintf("%.2f M", result)
	case 3:
		return fmt.Sprintf("%.2f G", result)
	default:
		return fmt.Sprintf("%v B", size)
	}
}

func main() {
	// file := "D:\\BaiduYunDownload"
	file := "D:\\BaiduYunDownload\\viso.ISO"
	fmt.Println(file)
	fmt.Println("Hello World!")

	var g int64
	g = 1024

	if fileInfo, err := os.Stat(file); err == nil {
		fmt.Printf("Size: %d byte \n", fileInfo.Size())
		fmt.Printf("Size: %d k \n", (fileInfo.Size() * 1.0 / g))
		fmt.Printf("Size: %v M \n", (fileInfo.Size() * 1.0 / g / g))
		fmt.Println("IsDir: ", fileInfo.IsDir())

		fmt.Println(reflect.TypeOf(fileInfo.Sys()))
	}
	fmt.Println("-----------------------------------------")
	getFilelist(file)
}
