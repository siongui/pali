package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"os"
	"path/filepath"
	"github.com/chai2010/gettext-go/gettext"
)

type templateData struct {
	TipitakaURL   string
	OgImage       string
	OgUrl         string
	OgLocale      string
}

func setupLocale(locale string, domain string, dir string) {
	gettext.SetLocale(locale)
	gettext.Textdomain(domain)

	gettext.BindTextdomain(domain, dir, nil)
}

func changeLocale(locale string) {
	gettext.SetLocale(locale)
}

func translate(input string) string {
	return gettext.PGettext("", input)
}

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

	data := templateData{
		TipitakaURL:   tipitakaURL,
		OgImage:       "https://upload.wikimedia.org/wikipedia/commons/d/df/Dharma_Wheel.svg",
		OgUrl:         "https://siongui.github.io/pali-dictionary/",
		OgLocale:      "en_US",
	}
	setupLocale("zh_TW", "messages", localeDir)
	setupLocale("vi_VN", "messages", localeDir)
	setupLocale("fr_FR", "messages", localeDir)
	funcMap := template.FuncMap{
		"gettext": translate,
	}

	changeLocale(data.OgLocale)
	tpl := template.Must(template.New("pali").Funcs(funcMap).Parse(alltmpl))
	err := tpl.Execute(os.Stdout, &data)
	if err != nil {
		fmt.Println(err)
	}
}
