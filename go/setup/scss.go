package main

import (
	libsass "github.com/wellington/go-libsass"
	"os"
)

func main() {
	// open input sass/scss file to be compiled
	fi, err := os.Open(scssPath)
	if err != nil {
		panic(err)
	}
	defer fi.Close()

	// create output css file
	fo, err := os.Create(cssPath)
	if err != nil {
		panic(err)
	}
	defer fo.Close()

	// options for compilation
	p := libsass.IncludePaths([]string{scssDir})
	s := libsass.OutputStyle(libsass.COMPRESSED_STYLE)

	// create a new compiler with options
	comp, err := libsass.New(fo, fi, p, s)
	if err != nil {
		panic(err)
	}

	// start compile
	if err := comp.Run(); err != nil {
		panic(err)
	}
}
