package main

import "github.com/siongui/pali/go/lib"
import "html/template"
import "bytes"

const tplWord = `
{{range $word := .}}
<article class="word-explanation">
  <header>{{$word.BookInfo}}</header>
  <p>{{$word.Explanation}}</p>
</article>
{{end}}
`

type tplWordData struct {
	BookInfo    string
	Explanation template.HTML
}

func showWordByTemplate(wi lib.WordInfo) {
	RemoveAllChildNodes(mainContent)

	var tmp []tplWordData
	for bookId, explanation := range wi {
		tmp = append(tmp, tplWordData{
			BookInfo:    dicIndex[bookId].Author,
			Explanation: template.HTML(explanation),
		})
	}

	t1, _ := template.New("wordExplanation").Parse(tplWord)
	// Google Search: go html template output string
	// https://groups.google.com/forum/#!topic/golang-nuts/dSFHCV-e6Nw
	var buf bytes.Buffer
	t1.Execute(&buf, tmp)
	mainContent.Set("innerHTML", buf.String())
}
