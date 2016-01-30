package main

import "github.com/gopherjs/gopherjs/js"
import "github.com/siongui/pali/go/lib"

var word *js.Object
var mainContent *js.Object
var dicIndex = lib.GetDicIndex()

func handleInputKeyUp(event *js.Object) {
	if keycode := event.Get("keyCode").Int(); keycode == 13 {
		// user press enter key
		w := word.Get("value").String()
		mainContent.Set("textContent", w)
	}
}

func main() {
	word = js.Global.Get("document").Call("getElementById", "word")
	mainContent = js.Global.Get("document").Call("getElementById", "main-content")
	word.Set("value", "sacca")

	word.Call("addEventListener", "keyup", handleInputKeyUp, false)
}
