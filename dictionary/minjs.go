package main

import (
	"io/ioutil"
	"net/http"
	"net/url"
	"path"
)

func minjs(baseDir string, jsFiles []string, outputPath string) {
	var jsCode []byte
	for _, file := range jsFiles {
		jsPath := path.Join(baseDir, file)
		println("concatenating " + jsPath + " ...")
		b, err := ioutil.ReadFile(jsPath)
		if err != nil {
			panic(err)
		}
		jsCode = append(jsCode, b...)
	}

	params := url.Values{}
	//params.Set("code_url", "https://github.com/twnanda/twnanda/raw/master/theme/javascript/tongwen_core.js")
	//params.Set("code_url", "https://github.com/twnanda/twnanda/raw/master/theme/javascript/tongwen_table_ps2t.js")
	//params.Set("code_url", "https://github.com/twnanda/twnanda/raw/master/theme/javascript/tongwen_table_pt2s.js")
	//params.Set("code_url", "https://github.com/twnanda/twnanda/raw/master/theme/javascript/tongwen_table_s2t.js")
	//params.Set("code_url", "https://github.com/twnanda/twnanda/raw/master/theme/javascript/tongwen_table_t2s.js")
	params.Set("js_code", string(jsCode))
	params.Set("compilation_level", "SIMPLE_OPTIMIZATIONS")
	params.Set("language", "ECMASCRIPT5")
	params.Set("output_format", "text")
	params.Set("output_info", "compiled_code")

	println("\nCompressing combined js online ...")
	resp, err := http.PostForm("https://closure-compiler.appspot.com/compile", params)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()
	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	ioutil.WriteFile(path.Join(baseDir, outputPath), b, 0644)
}

func main() {
	baseDir := "dictionary"
	jsFiles := []string{
		"common/app/scripts/services/data/dicBooks.js",
		"common/app/scripts/services/data/succinctTrie.js",
		"common/app/scripts/services/data/i18nStrings.js",
		"app/scripts/app.js",
		"app/scripts/controllers.js",
		"app/scripts/directives/inputSuggest.js",
		"app/scripts/directives/draggableAndEvents.js",
		"common/app/scripts/services/paliWordJson.js",
		"common/app/scripts/services/shortExp.js",
		"common/app/scripts/services/ngBits.js",
		"common/app/scripts/services/wordSearch.js",
		"common/app/scripts/directives/dropdown.js",
		"common/app/scripts/filters/expOrder.js",
		"common/app/scripts/i18n.js",
	}
	minjs(baseDir, jsFiles, "app/all_compiled.js")
}
