package main

import "github.com/gopherjs/gopherjs/js"
import "github.com/siongui/pali/go/lib"

func showWord(wi lib.WordInfo) {
	// remove all children of mainContent
	for mainContent.Call("hasChildNodes").Bool() {
		mainContent.Call("removeChild", mainContent.Get("lastChild"))
	}

	for bookId, explanation := range wi {
		book := js.Global.Get("document").Call("createElement", "div")
		book.Set("textContent", dicIndex[bookId].Author)
		mainContent.Call("appendChild", book)
		exp := js.Global.Get("document").Call("createElement", "div")
		exp.Set("innerHTML", explanation)
		mainContent.Call("appendChild", exp)
	}
}
