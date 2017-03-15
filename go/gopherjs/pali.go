package main

import (
	"github.com/gopherjs/gopherjs/js"
	imepali "github.com/siongui/go-online-input-method-pali"
	bits "github.com/siongui/go-succinct-data-structure-trie"
	. "github.com/siongui/godom"
	jsgettext "github.com/siongui/gopherjs-i18n"
	sg "github.com/siongui/gopherjs-input-suggest"
)

var mainContent *js.Object
var bookIdAndInfos = GetBookIdAndInfos()
var isDev = (js.Global.Get("location").Get("hostname").String() == "localhost")
var frozenTrie bits.FrozenTrie
var navigatorLanguages = js.Global.Get("navigator").Get("languages").String()

func HttpWordJsonPath(word string) string {
	if isDev {
		return "/json/" + word + ".json"
	}
	return "/xemaauj9k5qn34x88m4h/" + word + ".json"
}

func handleInputKeyUp(e Event) {
	switch keycode := e.KeyCode(); keycode {
	case 13:
		// user press enter key
		w := e.Target().Value()
		e.Target().Blur()
		go httpGetWordJson(w)
	default:
	}
}

func main() {
	// add pali input method to input text element
	imepali.BindPaliInputMethodToInputTextElementById("word")

	// init variables
	mainContent = js.Global.Get("document").Call("getElementById", "main-content")

	// init trie for words suggestion
	bits.SetAllowedCharacters("abcdeghijklmnoprstuvyāīūṁṃŋṇṅñṭḍḷ…'’° -")
	frozenTrie = bits.FrozenTrie{}
	frozenTrie.Init(succinctTrieDataBlob, rankDirectoryDataBlob, succinctTrieNodeCount)

	// input suggest menu
	sg.BindSuggest("word", func(w string) []string {
		return frozenTrie.GetSuggestedWords(w, 30)
	})

	setupNavbar()
	setupSetting()

	// show language according to NavigatorLanguages API
	supportedLocales := []string{"en_US", "zh_TW", "vi_VN", "fr_FR"}
	initialLocale := jsgettext.DetermineLocaleByNavigatorLanguages(navigatorLanguages, supportedLocales)
	if initialLocale != "en_US" {
		jsgettext.Translate(initialLocale)
		langSelect := js.Global.Get("document").Call("getElementById", "lang-select")
		langSelect.Set("value", initialLocale)
	}

	Document.GetElementById("word").AddEventListener("keyup", handleInputKeyUp)
}
