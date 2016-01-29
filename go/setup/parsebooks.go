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
import "encoding/json"

type dictInfo struct {
	Lang      string `json:"lang"`
	Separator string `json:"separator"`
	Name      string `json:"name"`
	Author    string `json:"author"`
}

type dicIndex map[string]dictInfo

var c *opencc.Converter

func parseRecord(record []string) (id string, dict dictInfo) {
	// language of the dictionary,
	// "C" means Chinese and Japanese dictionary,
	// "E" means non-Chinese dictionary.
	lang := record[0]
	// id of the dictionary. Each dictionary has a unique value.
	id = record[1]
	// short name of the dictionary.
	name := record[2]
	// name and author of the dictionary.
	author := record[3]

	switch lang {
	case "C":
		// Chinese and Japanese dictionaries
		switch id {
		case "A":
			// Japanese dictionary
			dict.Lang = "ja"
			dict.Separator = " -"
			dict.Name = "《パーリ語辞典》"
			dict.Author = "増補改訂パーリ語辞典  水野弘元著"
		case "S":
			// Japanese dictionary
			dict.Lang = "ja"
			dict.Separator = " -"
			dict.Name = "《パーリ語辞典》"
			dict.Author = "パーリ語辞典  水野弘元著"
		default:
			// Chinese dictionary
			dict.Lang = "zh"

			switch id {
			case "D":
				dict.Separator = "~"
			case "H":
				dict.Separator = " -"
			case "T":
				dict.Separator = " -"
			default:
				dict.Separator = "。"
			}

			dict.Name = c.Convert(name)
			dict.Author = c.Convert(author)
		}
	case "E":
		// English, Vietnam, Myanmar dictionaries
		switch id {
		case "U", "Q", "E":
			// Vietnamese dictionary
			dict.Lang = "vi"
			// FIXME: is "。" correct separator?
			dict.Separator = "。"
		case "B", "K", "O", "R":
			// Burmese(Myanmar) dictionary
			dict.Lang = "my"
			// FIXME: is "。" correct separator?
			dict.Separator = "。"
		default:
			// English dictionary
			dict.Lang = "en"
			switch id {
			case "N":
				dict.Separator = "<br>"
			case "C":
				dict.Separator = "<br>"
			case "P":
				dict.Separator = "<i>"
			default:
				dict.Separator = "。"
			}
		}
		dict.Name = name
		dict.Author = author
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
	di := dicIndex{}
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
		di[id] = dict
	}

	// save in JSON file
	const jsonPath = "website/json/dicIndex.json"
	fo, err := os.Create(jsonPath)
	if err != nil {
		panic(err)
	}
	defer fo.Close()
	e := json.NewEncoder(fo)
	if err := e.Encode(di); err != nil {
		panic(err)
	}

	// print JSON indent
	b, _ := json.MarshalIndent(di, "", "  ")
	println(string(b))
}
