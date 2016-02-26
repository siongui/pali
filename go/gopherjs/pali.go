package main

import (
	"github.com/gopherjs/gopherjs/js"
	imepali "github.com/siongui/go-online-input-method-pali"
	bits "github.com/siongui/go-succinct-data-structure-trie"
	jsgettext "github.com/siongui/gopherjs-i18n"
)

var word *js.Object
var mainContent *js.Object
var bookIdAndInfos = GetBookIdAndInfos()
var isDev = (js.Global.Get("location").Get("hostname").String() == "localhost")
var frozenTrie bits.FrozenTrie

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
	} else {
		// show words suggestion
		w := word.Get("value").String()
		suggestedWords := frozenTrie.GetSuggestedWords(w, 30)
		showSuggestedWords(suggestedWords)
	}
}

func main() {
	// add pali input method to input text element
	imepali.BindPaliInputMethodToInputTextElementById("word")

	// init variables
	word = js.Global.Get("document").Call("getElementById", "word")
	mainContent = js.Global.Get("document").Call("getElementById", "main-content")
	//word.Set("value", "sacca")

	// init trie for words suggestion
	bits.SetAllowedCharacters("abcdeghijklmnoprstuvyāīūṁṃŋṇṅñṭḍḷ…'’° -")
	frozenTrie = bits.FrozenTrie{}
	frozenTrie.Init(succinctTrieDataBlob, rankDirectoryDataBlob, succinctTrieNodeCount)

	setupNavbar()
	setupSetting()

	// show language according to NavigatorLanguages API
	languages := js.Global.Get("navigator").Get("languages").String()
	supportedLocales := []string{"en_US", "zh_TW", "vi_VN", "fr_FR"}
	initialLocale := jsgettext.DetermineLocaleByNavigatorLanguages(languages, supportedLocales)
	if initialLocale != "en_US" {
		jsgettext.Translate(initialLocale)
		langSelect := js.Global.Get("document").Call("getElementById", "lang-select")
		langSelect.Set("value", initialLocale)
	}

	word.Call("addEventListener", "keyup", handleInputKeyUp, false)
}
