package main

import "github.com/gopherjs/gopherjs/js"
import "github.com/siongui/pali/go/lib"

/* the following code is not working

import "html/template"
import "bytes"

const tplWord = `
{{range $book, $explanation := .}}
<article>
  <header>{{$book}}</header>
  <p>{{$explanation}}</p>
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
*/

func showWord(wi lib.WordInfo) {
	RemoveAllChildNodes(mainContent)

	for bookId, explanation := range wi {
		a := js.Global.Get("document").Call("createElement", "article")
		a.Get("classList").Call("add", "word-explanation")

		book := js.Global.Get("document").Call("createElement", "header")
		book.Set("textContent", dicIndex[bookId].Author)
		a.Call("appendChild", book)

		exp := js.Global.Get("document").Call("createElement", "p")
		exp.Set("innerHTML", explanation)
		a.Call("appendChild", exp)

		mainContent.Call("appendChild", a)
	}
}
