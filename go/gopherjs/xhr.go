package main

import "github.com/gopherjs/gopherjs/js"

func handleGetWordOK(json string) {
	wi := DecodeWordJson(json)
	showWord(wi)
}

func handleGetWordError() {
	mainContent.Set("textContent", "Not Found")
}

var readyStateChange = js.MakeFunc(func(this *js.Object, arguments []*js.Object) interface{} {
	if this.Get("readyState").Int() == 4 {
		if this.Get("status").Int() == 200 {
			handleGetWordOK(this.Get("responseText").String())
		} else {
			handleGetWordError()
		}
	}
	return nil
})

func xhrGetWordJson(w string) {
	req := js.Global.Get("XMLHttpRequest").New()
	req.Call("addEventListener", "readystatechange", readyStateChange)
	req.Call("open", "GET", HttpWordJsonPath(w), true)
	req.Call("send")
}
