package main

import "os"
import "encoding/json"
import "github.com/siongui/pali/go/lib"

const WebsiteDir = "website"

const BookCsvPath = "data/dictionary/dict-books.csv"
const BookJsonPath = WebsiteDir + "/json/dicIndex.json"

const WordsCSV1Path = "data/dictionary/dict_words_1.csv"
const WordsCSV2Path = "data/dictionary/dict_words_2.csv"
const wordsJsonDir = WebsiteDir + "/json"

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

func GetDicIndex() lib.DicIndex {
	f, err := os.Open(BookJsonPath)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	dec := json.NewDecoder(f)
	d := lib.DicIndex{}
	if err := dec.Decode(&d); err != nil {
		panic(err)
	}
	return d
}

func GetWordPath(word string) string {
	return wordsJsonDir + "/" + word + ".json"
}

func GetWordInfo(word string) lib.WordInfo {
	f, err := os.Open(GetWordPath(word))
	if err != nil {
		panic(err)
	}
	defer f.Close()

	dec := json.NewDecoder(f)
	w := lib.WordInfo{}
	if err := dec.Decode(&w); err != nil {
		panic(err)
	}
	return w
}
