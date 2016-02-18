package main

/*
References:
https://github.com/go-humble/locstor
https://www.google.com/search?q=localstorage
https://developer.mozilla.org/en-US/docs/Web/API/Storage
https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API/Using_the_Web_Storage_API
*/

import "github.com/gopherjs/gopherjs/js"
import "github.com/siongui/pali/go/lib"

var localStorage = js.Global.Get("localStorage")

func savePaliDictionarySetting(setting lib.PaliDictionarySetting) {
	str := PaliDictionarySetting2JsonString(setting)
	localStorage.Set("PaliDictionarySetting", str)
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

	setting := lib.PaliDictionarySetting{
		IsShowWordPreview: false,
		P2en:              true,
		P2ja:              true,
		P2zh:              true,
		P2vi:              true,
		P2my:              true,
		DicLangOrder:      "hdr",
	}
	// check if there is saved setting in user browser
	if localStorage.Get("PaliDictionarySetting") == js.Undefined {
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
		//localStorage.Call("getItem", "PaliDictionarySetting").String()
		setting = JsonString2PaliDictionarySetting(localStorage.Get("PaliDictionarySetting").String())
		isPreview.Set("checked", setting.IsShowWordPreview)
		p2en.Set("checked", setting.P2en)
		p2ja.Set("checked", setting.P2ja)
		p2zh.Set("checked", setting.P2zh)
		p2vi.Set("checked", setting.P2vi)
		p2my.Set("checked", setting.P2my)
		dicLangOrder.Set("value", setting.DicLangOrder)
	}

	isPreview.Call("addEventListener", "click", func(event *js.Object) {
		setting.IsShowWordPreview = isPreview.Get("checked").Bool()
		savePaliDictionarySetting(setting)
	})
	// http://stackoverflow.com/questions/4471401/getting-value-of-html-checkbox-from-onclick-onchange-events
	p2en.Call("addEventListener", "click", func(event *js.Object) {
		setting.P2en = p2en.Get("checked").Bool()
		savePaliDictionarySetting(setting)
	})
	p2ja.Call("addEventListener", "click", func(event *js.Object) {
		setting.P2ja = p2ja.Get("checked").Bool()
		savePaliDictionarySetting(setting)
	})
	p2zh.Call("addEventListener", "click", func(event *js.Object) {
		setting.P2zh = p2zh.Get("checked").Bool()
		savePaliDictionarySetting(setting)
	})
	p2vi.Call("addEventListener", "click", func(event *js.Object) {
		setting.P2vi = p2vi.Get("checked").Bool()
		savePaliDictionarySetting(setting)
	})
	p2my.Call("addEventListener", "click", func(event *js.Object) {
		setting.P2my = p2my.Get("checked").Bool()
		savePaliDictionarySetting(setting)
	})
	dicLangOrder.Call("addEventListener", "change", func(event *js.Object) {
		setting.DicLangOrder = dicLangOrder.Get("options").Call("item",
			dicLangOrder.Get("selectedIndex").Int()).Get("value").String()
		savePaliDictionarySetting(setting)
	})
}
