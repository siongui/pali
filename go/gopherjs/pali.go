package main

import "github.com/gopherjs/gopherjs/js"
import "github.com/siongui/pali/go/lib"

var word *js.Object
var mainContent *js.Object
var dicIndex = lib.GetDicIndex()

func handleWordLoad(json string) {
	wi := DecodeWordJson(json)
	print(wi)
	mainContent.Set("textContent", json)
}

func handleWordError() {
	mainContent.Set("textContent", "Not Found")
}

var readyStateChange = js.MakeFunc(func(this *js.Object, arguments []*js.Object) interface{} {
	if this.Get("readyState").Int() == 4 {
		if this.Get("status").Int() == 200 {
			handleWordLoad(this.Get("responseText").String())
		} else {
			handleWordError()
		}
	}
	return nil
})

func getWordInfo(w string) {
	req := js.Global.Get("XMLHttpRequest").New()
	req.Call("addEventListener", "readystatechange", readyStateChange)
	req.Call("open", "GET", lib.HttpWordJsonPath(w), true)
	req.Call("send")
}

func handleInputKeyUp(event *js.Object) {
	if keycode := event.Get("keyCode").Int(); keycode == 13 {
		// user press enter key
		w := word.Get("value").String()
		getWordInfo(w)
	}
}

func main() {
	word = js.Global.Get("document").Call("getElementById", "word")
	mainContent = js.Global.Get("document").Call("getElementById", "main-content")
	word.Set("value", "sacca")

	word.Call("addEventListener", "keyup", handleInputKeyUp, false)
}
