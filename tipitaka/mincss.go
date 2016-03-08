package main

import (
	"github.com/siongui/mincss"
	"io/ioutil"
)

func main() {
	cssPathes := []string{
		"tipitaka/app/css/tipitaka-latn.css",
		"tipitaka/app/css/app.css",
	}
	minifiedCss := mincss.MinifyCSS(cssPathes)
	println(minifiedCss)
	if err := ioutil.WriteFile("tipitaka/app/css/app.min.css", []byte(minifiedCss), 0644); err != nil {
		panic(err)
	}
}
