package main

import "html/template"
import "os"
import "fmt"

func main() {
	tpl := template.Must(template.ParseFiles(indexTpl, navbarTpl, imeTpl))
	err := tpl.Execute(os.Stdout, nil)
	if err != nil {
		fmt.Println(err)
	}
}
