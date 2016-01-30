package main

import "github.com/gopherjs/gopherjs/js"

func main() {
	word := js.Global.Get("document").Call("getElementById", "word")
	word.Set("value", "sacca")
}
