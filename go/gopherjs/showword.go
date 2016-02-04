package main

import "github.com/gopherjs/gopherjs/js"
import "github.com/siongui/pali/go/lib"

func showWord(wi lib.BookIdWordExps) {
	RemoveAllChildNodes(mainContent)

	for bookId, explanation := range wi {
		a := js.Global.Get("document").Call("createElement", "article")
		a.Get("classList").Call("add", "word-explanation")

		book := js.Global.Get("document").Call("createElement", "header")
		book.Set("textContent", bookIdAndInfos[bookId].Author)
		a.Call("appendChild", book)

		exp := js.Global.Get("document").Call("createElement", "p")
		exp.Set("innerHTML", explanation)
		a.Call("appendChild", exp)

		mainContent.Call("appendChild", a)
	}
}

func showSuggestedWords(words []string) {
	RemoveAllChildNodes(mainContent)

	for _, word := range words {
		w := js.Global.Get("document").Call("createElement", "div")
		w.Set("textContent", word)

		mainContent.Call("appendChild", w)
	}
}
