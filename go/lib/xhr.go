package lib

import "net/http"
import "encoding/json"

func HttpWordJsonPath(word string) string {
	return "/json/" + word + ".json"
}

func XhrGetWordInfo(word string) (w WordInfo, err error) {
	resp, err := http.Get(HttpWordJsonPath(word))
	if err != nil {
		return
	}
	defer resp.Body.Close()

	dec := json.NewDecoder(resp.Body)
	err = dec.Decode(&w)
	return
}
