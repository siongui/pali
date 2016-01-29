/*
In this script, we will build "dicIndex".
The format of dicIndex:
dicIndex = object of key-value pairs, where
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
https://www.google.com/search?q=golang+read+csv
http://stackoverflow.com/questions/10858787/what-are-the-uses-for-tags-in-go
*/
package main

import "os"
import "encoding/csv"
import "io"
import "github.com/siongui/go-opencc"
import "fmt"

type dictInfo struct {
	lang      string `json:"lang"`
	separator string `json:"separator"`
	name      string `json:"name"`
	author    string `json:"author"`
}

var c *opencc.Converter

func parseRecord(record []string) (id string, dict dictInfo) {
	// language of the dictionary,
	// "C" means Chinese and Japanese dictionary,
	// "E" means non-Chinese dictionary.
	lang := record[0]
	// id of the dictionary. Each dictionary has a unique value.
	id = record[1]
	// name of the dictionary.
	name := record[2]
	// name and author of the dictionary.
	author := record[3]

	switch lang {
	case "C":
		// Chinese and Japanese dictionaries
		switch id {
		case "A":
			// Japanese dictionary
			dict.lang = "ja"
			dict.separator = " -"
			dict.name = "《パーリ語辞典》"
			dict.author = "増補改訂パーリ語辞典  水野弘元著"
		case "S":
			// Japanese dictionary
			dict.lang = "ja"
			dict.separator = " -"
			dict.name = "《パーリ語辞典》"
			dict.author = "パーリ語辞典  水野弘元著"
		default:
			// Chinese dictionary
			dict.lang = "zh"

			switch id {
			case "D":
				dict.separator = "~"
			case "H":
				dict.separator = " -"
			case "T":
				dict.separator = " -"
			default:
				dict.separator = "。"
			}

			dict.name = c.Convert(name)
			dict.author = c.Convert(author)
		}
	case "E":
		// English, Vietnam, Myanmar dictionaries
		println("noncht")
	default:
		panic("wrong lang")
	}
	return
}

func main() {
	const bookCsvPath = "data/dictionary/dict-books.csv"
	c = opencc.NewConverter("zhs2zht.ini")
	defer c.Close()

	// open csv file
	fcsv, err := os.Open(bookCsvPath)
	if err != nil {
		panic(err)
	}
	defer fcsv.Close()

	// read csv
	r := csv.NewReader(fcsv)
	for {
		record, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}
		if record[0] == "b_lang" {
			continue
		}
		id, dict := parseRecord(record)
		fmt.Println(id, dict)
	}
}
