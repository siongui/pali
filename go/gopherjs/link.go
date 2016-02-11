package main

import "github.com/gopherjs/gopherjs/js"

func setupLinks() {
	d := js.Global.Get("document")
	about := d.Call("getElementById", "about")
	punch := d.Call("getElementById", "punch")

	nodeList := d.Call("querySelectorAll", ".about-link")
	length := nodeList.Get("length").Int()
	for i := 0; i < length; i++ {
		link := nodeList.Call("item", i)
		link.Call("addEventListener", "click", func() {
			RemoveAllChildNodes(mainContent)
			mainContent.Set("innerHTML", about.Get("innerHTML").String())
			// close toggle window on mobile device
			punch.Set("checked", true)
		})
	}
}
