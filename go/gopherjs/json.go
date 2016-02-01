package main

import "github.com/siongui/pali/go/lib"
import "encoding/json"
import "io"

func DecodeHttpRespWord(respBody io.ReadCloser) (wi lib.WordInfo) {
	dec := json.NewDecoder(respBody)
	// handle err here?
	dec.Decode(&wi)
	return
}

func DecodeWordJson(w string) lib.WordInfo {
	wi := lib.WordInfo{}
	err := json.Unmarshal([]byte(w), &wi)
	if err != nil {
		panic(err)
	}
	return wi
}

func GetDicIndex() lib.DicIndex {
	di := lib.DicIndex{}
	err := json.Unmarshal(dicIndexJsonBlob, &di)
	if err != nil {
		panic(err)
	}
	return di
}
