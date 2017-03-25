package main

import (
	"encoding/json"
	"github.com/siongui/gopalilib/lib"
	"io"
)

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

func PaliDictionarySetting2JsonString(setting lib.PaliDictionarySetting) string {
	b, err := json.Marshal(setting)
	if err != nil {
		panic(err)
	}
	return string(b)
}

func JsonString2PaliDictionarySetting(jsonStr string) lib.PaliDictionarySetting {
	setting := lib.PaliDictionarySetting{}
	err := json.Unmarshal([]byte(jsonStr), &setting)
	if err != nil {
		panic(err)
	}
	return setting
}
