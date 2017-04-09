package main

import (
	imepali "github.com/siongui/go-online-input-method-pali"
	bits "github.com/siongui/go-succinct-data-structure-trie"
	. "github.com/siongui/godom"
	jsgettext "github.com/siongui/gopherjs-i18n"
	sg "github.com/siongui/gopherjs-input-suggest"
	"github.com/siongui/paliDataVFS"
)

var mainContent *Object
var bookIdAndInfos = paliDataVFS.GetBookIdAndInfos()
var frozenTrie bits.FrozenTrie
var navigatorLanguages = Window.Navigator().Languages()

func isDev() bool {
	return Window.Location().Hostname() == "localhost"
}

func HttpWordJsonPath(word string) string {
	if isDev() {
		return "/json/" + word + ".json"
	}
	return "https://siongui.github.io/xemaauj9k5qn34x88m4h/" + word + ".json"
	//return "/xemaauj9k5qn34x88m4h/" + word + ".json"
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
	mainContent = Document.GetElementById("main-content")

	// init trie for words suggestion
	bits.SetAllowedCharacters("abcdeghijklmnoprstuvyāīūṁṃŋṇṅñṭḍḷ…'’° -")
	frozenTrie = bits.FrozenTrie{}
	frozenTrie.Init(paliDataVFS.GetTrieData())

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
		langSelect := Document.GetElementById("lang-select")
		langSelect.SetValue(initialLocale)
	}

	input := Document.GetElementById("word")
	input.AddEventListener("keyup", handleInputKeyUp)
	Document.AddEventListener("keyup", func(e Event) {
		if e.KeyCode() == 9 {
			if !input.IsFocused() {
				input.Focus()
			}
		}
	})
}
