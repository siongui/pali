package main

import (
	"encoding/json"
	"github.com/siongui/pali/go/lib"
	"os"
)

func SaveJsonFile(v interface{}, path string) {
	fo, err := os.Create(path)
	if err != nil {
		panic(err)
	}
	defer fo.Close()
	e := json.NewEncoder(fo)
	if err := e.Encode(v); err != nil {
		panic(err)
	}
}

func PrettyPrint(v interface{}) {
	b, _ := json.MarshalIndent(v, "", "  ")
	println(string(b))
}

func GetBookIdAndInfos(BookJsonPath string) lib.BookIdAndInfos {
	f, err := os.Open(BookJsonPath)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	dec := json.NewDecoder(f)
	d := lib.BookIdAndInfos{}
	if err := dec.Decode(&d); err != nil {
		panic(err)
	}
	return d
}

func GetWordPath(word, wordsJsonDir string) string {
	return wordsJsonDir + "/" + word + ".json"
}

func GetBookIdWordExps(word, wordsJsonDir string) lib.BookIdWordExps {
	f, err := os.Open(GetWordPath(word, wordsJsonDir))
	if err != nil {
		panic(err)
	}
	defer f.Close()

	dec := json.NewDecoder(f)
	w := lib.BookIdWordExps{}
	if err := dec.Decode(&w); err != nil {
		panic(err)
	}
	return w
}
