package main

import "github.com/siongui/pali/go/lib"
import "html/template"
import "bytes"

func showWordByTemplate(wi lib.WordInfo) {
	RemoveAllChildNodes(mainContent)

	var tmp []lib.WordExplanation
	for bookId, explanation := range wi {
		tmp = append(tmp, lib.WordExplanation{
			BookInfo:    dicIndex[bookId].Author,
			Explanation: template.HTML(explanation),
		})
	}

	t1, _ := template.New("wordExplanation").Parse(lib.HtmlTemplateWordExplanations)
	// Google Search: go html template output string
	// https://groups.google.com/forum/#!topic/golang-nuts/dSFHCV-e6Nw
	var buf bytes.Buffer
	t1.Execute(&buf, tmp)
	mainContent.Set("innerHTML", buf.String())
}
