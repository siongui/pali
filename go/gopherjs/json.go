package main

import "github.com/siongui/pali/go/lib"
import "encoding/json"
import "io"

func DecodeHttpRespWord(respBody io.ReadCloser) (wi lib.BookIdWordExps) {
	dec := json.NewDecoder(respBody)
	// handle err here?
	dec.Decode(&wi)
	return
}

func DecodeWordJson(w string) lib.BookIdWordExps {
	wi := lib.BookIdWordExps{}
	err := json.Unmarshal([]byte(w), &wi)
	if err != nil {
		panic(err)
	}
	return wi
}

func GetBookIdAndInfos() lib.BookIdAndInfos {
	di := lib.BookIdAndInfos{}
	err := json.Unmarshal(bookIdAndInfosJsonBlob, &di)
	if err != nil {
		panic(err)
	}
	return di
}
