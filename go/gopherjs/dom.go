package main

import "github.com/gopherjs/gopherjs/js"

func RemoveAllChildNodes(elm *js.Object) {
	for elm.Call("hasChildNodes").Bool() {
		elm.Call("removeChild", elm.Get("lastChild"))
	}
}
