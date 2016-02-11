package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"os"
	"path/filepath"
)

type templateData struct {
	TipitakaURL   string
	OgTitle       string
	OgDescription string
	OgImage       string
	OgUrl         string
	OgLocale      string
}

func main() {
	var alltmpl string
	data := templateData{
		TipitakaURL:   tipitakaURL,
		OgTitle:       "Pāli Dictionary",
		OgDescription: "Pāli to English, Chinese, Japanese, Vietnamese, Burmese Dictionary",
		OgImage:       "https://upload.wikimedia.org/wikipedia/commons/d/df/Dharma_Wheel.svg",
		OgUrl:         "https://siongui.github.io/pali-dictionary/",
		OgLocale:      "en_US",
	}

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
	err := tpl.Execute(os.Stdout, &data)
	if err != nil {
		fmt.Println(err)
	}
}
