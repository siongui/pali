package main

import "net/http"

func httpGetWordJson(w string) {
	resp, err := http.Get(HttpWordJsonPath(w))
	if err != nil {
		mainContent.Set("textContent", "Not Found")
		return
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		mainContent.Set("textContent", "Not Found")
		return
	}

	wi := DecodeHttpRespWord(resp.Body)
	showWordByTemplate(wi)
}
