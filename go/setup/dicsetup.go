package main

import (
	"flag"
	"github.com/siongui/gopalilib/dicutil"
)

func main() {
	action := flag.String("action", "", "What kind of action?")
	isdev := flag.Bool("isdev", false, "Is development?")
	flag.Parse()

	if *action == "symlink" {
		sroot := "src/github.com/siongui/pali-dictionary"
		if *isdev {
			sroot = "website"
		}
		err := dicutil.SymlinkToRootIndexHtml("website/json", sroot)
		if err != nil {
			panic(err)
		}
	}
}
