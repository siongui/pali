package main

import "github.com/gopherjs/gopherjs/js"
import "github.com/siongui/pali/go/lib"

func getWordJsonData() {
	word := js.Global.Get("document").Call("getElementById", "word")
	w := word.Get("value").String()
	wi, err := lib.XhrGetWordInfo(w)

	show := js.Global.Get("document").Call("getElementById", "main-content")
	if err != nil {
		show.Set("textContent", err)
	} else {
		for bookId, explanation := range wi {
			show.Set("textContent", bookId+"<br>"+explanation)
			break
		}
	}
}

func handleInputKeyUp(event *js.Object) {
	if keycode := event.Get("keyCode").Int(); keycode == 13 {
		// user press enter key
		getWordJsonData()
	}
}

func main() {
	word := js.Global.Get("document").Call("getElementById", "word")
	word.Set("value", "sacca")

	word.Call("addEventListener", "keyup", handleInputKeyUp, false)
}
