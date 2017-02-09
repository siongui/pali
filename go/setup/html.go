package main

import (
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
	gossg.SetupMessagesDomain(localeDir)
	data := templateData{
		SiteUrl:     "https://siongui.github.io/pali-dictionary",
		TipitakaURL: tipitakaURL,
		OgImage:     "https://upload.wikimedia.org/wikipedia/commons/d/df/Dharma_Wheel.svg",
		OgUrl:       "https://siongui.github.io/pali-dictionary/",
		OgLocale:    "en_US",
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
