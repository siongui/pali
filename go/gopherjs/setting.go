package main

/*
References:
https://github.com/go-humble/locstor
https://www.google.com/search?q=localstorage
https://developer.mozilla.org/en-US/docs/Web/API/Storage
https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API/Using_the_Web_Storage_API
*/

import "github.com/gopherjs/gopherjs/js"

var localStorage = js.Global.Get("localStorage")

type paliSetting struct {
	IsShowWordPreview bool
	P2en              bool
	P2ja              bool
	P2zh              bool
	P2vi              bool
	P2my              bool
	DicLangOrder      string
}

func setupSetting() {
	d := js.Global.Get("document")
	isPreview := d.Call("getElementById", "isShowWordPreview")
	p2en := d.Call("getElementById", "p2en")
	p2ja := d.Call("getElementById", "p2ja")
	p2zh := d.Call("getElementById", "p2zh")
	p2vi := d.Call("getElementById", "p2vi")
	p2my := d.Call("getElementById", "p2my")
	dicLangOrder := d.Call("getElementById", "dicLangOrder")

	setting := paliSetting{
		IsShowWordPreview: false,
		P2en:              true,
		P2ja:              true,
		P2zh:              true,
		P2vi:              true,
		P2my:              true,
		DicLangOrder:      "hdr",
	}
	// check if there is saved setting in user browser
	if localStorage.Get("paliSetting") == js.Undefined {
		// no setting saved, use default setting
		setting.IsShowWordPreview = isPreview.Get("checked").Bool()
		setting.P2en = p2en.Get("checked").Bool()
		setting.P2ja = p2ja.Get("checked").Bool()
		setting.P2zh = p2zh.Get("checked").Bool()
		setting.P2vi = p2vi.Get("checked").Bool()
		setting.P2my = p2my.Get("checked").Bool()
		setting.DicLangOrder = dicLangOrder.Get("options").Call("item",
			dicLangOrder.Get("selectedIndex").Int()).Get("value").String()
	} else {
		// use saved setting
		//localStorage.Call("getItem", "paliSetting").String()
		//jsonString2Setting
	}

	isPreview.Call("addEventListener", "click", func(event *js.Object) {
		setting.IsShowWordPreview = isPreview.Get("checked").Bool()
		// save setting
		print("isPreview")
	})
	// http://stackoverflow.com/questions/4471401/getting-value-of-html-checkbox-from-onclick-onchange-events
	p2en.Call("addEventListener", "click", func(event *js.Object) {
		setting.P2en = p2en.Get("checked").Bool()
		// save setting
		print("p2en")
	})
	p2ja.Call("addEventListener", "click", func(event *js.Object) {
		setting.P2ja = p2ja.Get("checked").Bool()
		// save setting
		print("p2ja")
	})
	p2zh.Call("addEventListener", "click", func(event *js.Object) {
		setting.P2zh = p2zh.Get("checked").Bool()
		// save setting
		print("p2zh")
	})
	p2vi.Call("addEventListener", "click", func(event *js.Object) {
		setting.P2vi = p2vi.Get("checked").Bool()
		// save setting
		print("p2vi")
	})
	p2my.Call("addEventListener", "click", func(event *js.Object) {
		setting.P2my = p2my.Get("checked").Bool()
		// save setting
		print("p2my")
	})
	dicLangOrder.Call("addEventListener", "change", func(event *js.Object) {
		setting.DicLangOrder = dicLangOrder.Get("options").Call("item",
			dicLangOrder.Get("selectedIndex").Int()).Get("value").String()
		// save setting
		print(setting.DicLangOrder)
	})
}
