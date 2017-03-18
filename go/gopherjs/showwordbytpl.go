package main

import (
	"bytes"
	"github.com/siongui/pali/go/lib"
	"html/template"
)

func showWordByTemplate(wi lib.BookIdWordExps) {
	mainContent.RemoveAllChildNodes()

	bnwes := lib.IdExps2BookNameWordExps(
		lib.BookIdWordExps2IdExpsAccordingToSetting(wi, bookIdAndInfos, getSetting(), navigatorLanguages),
		bookIdAndInfos)
	t1, _ := template.New("wordExplanation").Parse(lib.HtmlTemplateBookNameWordExps)
	// Google Search: go html template output string
	// https://groups.google.com/forum/#!topic/golang-nuts/dSFHCV-e6Nw
	var buf bytes.Buffer
	t1.Execute(&buf, bnwes)
	mainContent.Set("innerHTML", buf.String())
}

func showSuggestedWordsByTemplate(words []string) {
	mainContent.RemoveAllChildNodes()

	t1, _ := template.New("suggestedWords").Parse(lib.HtmlTemplateSuggestedWords)
	var buf bytes.Buffer
	t1.Execute(&buf, words)
	mainContent.Set("innerHTML", buf.String())
}
