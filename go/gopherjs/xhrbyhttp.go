package main

import "net/http"

func httpGetWordJson(w string) {
	resp, err := http.Get(HttpWordJsonPath(w))
	if err != nil {
		handleGetWordError()
		return
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		handleGetWordError()
		return
	}

	wi := DecodeHttpRespWord(resp.Body)
	//showWord(wi)
	showWordByTemplate(wi)
}
