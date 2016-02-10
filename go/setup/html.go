package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"os"
	"path/filepath"
)

func main() {
	var alltmpl string

	filepath.Walk(htmlTemplateDir, func(path string, info os.FileInfo, err error) error {
		name := info.Name()
		if !info.IsDir() && name[len(name)-5:] == ".html" {
			b, err := ioutil.ReadFile(path)
			if err != nil {
				panic(err)
			}
			alltmpl += string(b)
		}
		return nil
	})

	tpl := template.Must(template.New("pali").Parse(alltmpl))
	err := tpl.Execute(os.Stdout, nil)
	if err != nil {
		fmt.Println(err)
	}
}
