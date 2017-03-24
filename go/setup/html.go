package main

import (
	"flag"
	"github.com/siongui/gotemplateutil"
	"os"
)

type templateData struct {
	SiteUrl     string
	TipitakaURL string
	OgImage     string
	OgUrl       string
	OgLocale    string
}

func main() {
	isdev := flag.Bool("isdev", false, "Is development?")
	flag.Parse()

	gossg.SetupMessagesDomain(localeDir)
	data := templateData{
		SiteUrl:     "http://dictionary.online-dhamma.net",
		TipitakaURL: tipitakaURL,
		OgImage:     "https://upload.wikimedia.org/wikipedia/commons/d/df/Dharma_Wheel.svg",
		OgUrl:       "http://dictionary.online-dhamma.net/",
		OgLocale:    "en_US",
	}

	if *isdev {
		data.SiteUrl = ""
	}

	tmpl, err := gossg.ParseDirectoryWithGettextFunction(htmlTemplateDir)
	if err != nil {
		panic(err)
	}

	gossg.SetLocale(data.OgLocale)
	err = tmpl.ExecuteTemplate(os.Stdout, "index.html", &data)
	if err != nil {
		panic(err)
	}
}
