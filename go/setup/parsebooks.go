package main

/*
In this script, we will parse information about dictionaries and build the type
"BookIdAndInfos" struct, and save the infomation in JSON file.

References:
https://www.google.com/search?q=golang+read+csv
*/

import (
	"encoding/csv"
	"flag"
	"github.com/siongui/go-opencc"
	"github.com/siongui/pali/go/lib"
	"io"
	"os"
)

// For Ubuntu 16.04 or before
//var cs2t = opencc.NewConverter("zhs2zht.ini")
// For Ubuntu 16.10
var cs2t = opencc.NewConverter("s2tw.json")

func parseRecord(record []string) (id string, dict lib.BookInfo) {
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

			dict.Name = cs2t.Convert(name)
			dict.Author = cs2t.Convert(author)
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
	defer cs2t.Close()

	dicDataDir := flag.String("dic", "data/dictionary", "Directory of Dictioanry Data")
	BookJsonPath := flag.String("output", "website/bookIdAndInfos.json", "Output Path of Parsed Dictionary Books Info")

	flag.Parse()
	BookCsvPath := *dicDataDir + "/dict-books.csv"

	// open csv file
	fcsv, err := os.Open(BookCsvPath)
	if err != nil {
		panic(err)
	}
	defer fcsv.Close()

	// read csv
	di := lib.BookIdAndInfos{}
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

	SaveJsonFile(di, *BookJsonPath)
	PrettyPrint(di)
}
