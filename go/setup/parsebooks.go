package main
/*
In this script, we will parse information about dictionaries and build the type
"DicIndex" struct, and save the infomation in JSON file.

References:
https://www.google.com/search?q=golang+read+csv
*/

import "os"
import "encoding/csv"
import "io"
import "github.com/siongui/go-opencc"
import "encoding/json"
import "github.com/siongui/pali/go/lib"

var c *opencc.Converter

func parseRecord(record []string) (id string, dict lib.DictInfo) {
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
	c = opencc.NewConverter("zhs2zht.ini")
	defer c.Close()

	// open csv file
	fcsv, err := os.Open(lib.BookCsvPath)
	if err != nil {
		panic(err)
	}
	defer fcsv.Close()

	// read csv
	di := lib.DicIndex{}
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
	fo, err := os.Create(lib.BookJsonPath)
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
