package main

import (
	"flag"
	libsass "github.com/wellington/go-libsass"
	"os"
)

func main() {
	scssPath := flag.String("scsspath", "default value", "Path of SCSS file to be compiled")
	scssDir := flag.String("scssdir", "default value", "Include Dir of SCSS files")
	cssPath := flag.String("csspath", "default value", "Path of output CSS file")
	flag.Parse()

	// open input sass/scss file to be compiled
	fi, err := os.Open(*scssPath)
	if err != nil {
		panic(err)
	}
	defer fi.Close()

	// create output css file
	fo, err := os.Create(*cssPath)
	if err != nil {
		panic(err)
	}
	defer fo.Close()

	// options for compilation
	p := libsass.IncludePaths([]string{*scssDir})
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
