/*
The format of DicIndex:
DicIndex = object of key-value pairs, where
  key = id of the dictionary
  value = [cell1, cell2, cell3, cell4], where
    cell1 = language of the dictionary.
            zh: Chinese
            ja: Japanese
            en: English
            vi: Vietnamese
            my: Burmese(Myanmar)
    cell2 = separator, used to get short explanation of the word.
    cell3 = short name of the dictionary
    cell4 = name and author of the dictionary

References:
http://stackoverflow.com/questions/10858787/what-are-the-uses-for-tags-in-go
*/
package lib

import "github.com/siongui/go-opencc"
import "os"
import "encoding/json"

type DictInfo struct {
	Lang      string `json:"lang"`
	Separator string `json:"separator"`
	Name      string `json:"name"`
	Author    string `json:"author"`
}

// book id <-> book info
type DicIndex map[string]DictInfo

// book id <-> word explanation
type WordInfo map[string]string

const BookCsvPath = "data/dictionary/dict-books.csv"
const BookJsonPath = "website/json/dicIndex.json"

const WordsCSV1Path = "data/dictionary/dict_words_1.csv"
const WordsCSV2Path = "data/dictionary/dict_words_2.csv"
const wordsJsonDir = "website/json/"

func Zhs2zhtConverter() *opencc.Converter {
	return opencc.NewConverter("zhs2zht.ini")
}

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

func GetDicIndex() DicIndex {
	f, err := os.Open(BookJsonPath)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	dec := json.NewDecoder(f)
	d := DicIndex{}
	if err := dec.Decode(&d); err != nil {
		panic(err)
	}
	return d
}

func GetWordPath(word string) string {
	return wordsJsonDir + word + ".json"
}

func GetWordInfo(word string) WordInfo {
	f, err := os.Open(GetWordPath(word))
	if err != nil {
		panic(err)
	}
	defer f.Close()

	dec := json.NewDecoder(f)
	w := WordInfo{}
	if err := dec.Decode(&w); err != nil {
		panic(err)
	}
	return w
}
