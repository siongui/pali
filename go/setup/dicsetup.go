package main

import (
	"flag"
	"github.com/siongui/gopalilib/dicutil"
	"os"
)

const localeDir = "../common/locale"
const htmlTemplateDir = "theme/template"
const tipitakaURL = "http://tipitaka.sutta.org/"

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

	if *action == "html" {
		data := dicutil.TemplateData{
			SiteUrl:     "http://dictionary.online-dhamma.net",
			TipitakaURL: "http://tipitaka.online-dhamma.net",
			OgImage:     "https://upload.wikimedia.org/wikipedia/commons/d/df/Dharma_Wheel.svg",
			OgUrl:       "http://dictionary.online-dhamma.net/",
			OgLocale:    "en_US",
		}

		if *isdev {
			data.SiteUrl = ""
		}

		err := dicutil.CreateHTML(os.Stdout, "index.html", &data, localeDir, htmlTemplateDir)
		if err != nil {
			panic(err)
		}
	}
}
