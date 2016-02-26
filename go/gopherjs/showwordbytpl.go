package main

import "github.com/siongui/pali/go/lib"
import "html/template"
import "bytes"

func showWordByTemplate(wi lib.BookIdWordExps) {
	RemoveAllChildNodes(mainContent)

	bnwes := lib.BookIdWordExps2BookNameWordExpsAccordingToSetting(wi, bookIdAndInfos, getSetting())
	t1, _ := template.New("wordExplanation").Parse(lib.HtmlTemplateBookNameWordExps)
	// Google Search: go html template output string
	// https://groups.google.com/forum/#!topic/golang-nuts/dSFHCV-e6Nw
	var buf bytes.Buffer
	t1.Execute(&buf, bnwes)
	mainContent.Set("innerHTML", buf.String())
}
