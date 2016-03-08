package main

import (
	"github.com/siongui/mincss"
	"io/ioutil"
)

func main() {
	cssPathes := []string{"dictionary/app/css/app.css"}
	minifiedCss := mincss.MinifyCSS(cssPathes)
	println(minifiedCss)
	if err := ioutil.WriteFile("dictionary/app/css/app.min.css", []byte(minifiedCss), 0644); err != nil {
		panic(err)
	}
}
