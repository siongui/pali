package main

import "github.com/gopherjs/gopherjs/js"
import "github.com/siongui/gopherjs-i18n"

func setupNavbar() {
	jsgettext.SetupTranslationMapping(string(poJsonBlob))

	d := js.Global.Get("document")
	about := d.Call("getElementById", "about")
	punch := d.Call("getElementById", "punch")
	settingMenu := d.Call("querySelector", ".setting-menu")

	// about link
	nodeList := d.Call("querySelectorAll", ".about-link")
	length := nodeList.Get("length").Int()
	for i := 0; i < length; i++ {
		link := nodeList.Call("item", i)
		link.Call("addEventListener", "click", func(event *js.Object) {
			// prevent follow link to #
			event.Call("preventDefault")

			// load about content
			RemoveAllChildNodes(mainContent)
			mainContent.Set("innerHTML", about.Get("innerHTML").String())

			// close toggle window on mobile device
			punch.Set("checked", true)
		})
	}

	// setting link
	nodeList = d.Call("querySelectorAll", ".setting-link")
	length = nodeList.Get("length").Int()
	for i := 0; i < length; i++ {
		link := nodeList.Call("item", i)
		link.Call("addEventListener", "click", func(event *js.Object) {
			// prevent follow link to #
			event.Call("preventDefault")

			// toggle arrow
			downArrow := link.Get("firstChild")
			downArrow.Get("classList").Call("toggle", "invisible")
			// right arrow
			downArrow.Get("nextSibling").Get("classList").Call("toggle", "invisible")
			// setting menu
			settingMenu.Get("classList").Call("toggle", "invisible")

			// close toggle window on mobile device
			punch.Set("checked", true)
		})
	}

	// language select
	ls := d.Call("getElementById", "lang-select")
	ls.Call("addEventListener", "change", func(event *js.Object) {
		locale := ls.Get("options").Call("item", ls.Get("selectedIndex").Int()).Get("value").String()
		jsgettext.Translate(locale)
	})

	// mobile language select
	nodeList = d.Call("querySelectorAll", ".mobile-lang-select")
	length = nodeList.Get("length").Int()
	for i := 0; i < length; i++ {
		link := nodeList.Call("item", i)
		link.Call("addEventListener", "click", func(event *js.Object) {
			// prevent follow link to #
			event.Call("preventDefault")

			locale := link.Get("dataset").Get("lang").String()
			jsgettext.Translate(locale)

			// close toggle window on mobile device
			punch.Set("checked", true)
		})
	}
}
