package main

import "github.com/gopherjs/gopherjs/js"

var word *js.Object
var mainContent *js.Object
var dicIndex = GetDicIndex()
var isDev = (js.Global.Get("location").Get("hostname").String() == "localhost")

func HttpWordJsonPath(word string) string {
	if isDev {
		return "/json/" + word + ".json"
	}
	return "/xemaauj9k5qn34x88m4h/" + word + ".json"
}

func handleInputKeyUp(event *js.Object) {
	if keycode := event.Get("keyCode").Int(); keycode == 13 {
		// user press enter key
		w := word.Get("value").String()
		//xhrGetWordJson(w)
		go httpGetWordJson(w)
	}
}

func main() {
	word = js.Global.Get("document").Call("getElementById", "word")
	mainContent = js.Global.Get("document").Call("getElementById", "main-content")
	word.Set("value", "sacca")

	word.Call("addEventListener", "keyup", handleInputKeyUp, false)
}
