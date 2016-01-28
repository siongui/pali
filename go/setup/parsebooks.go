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
*/
package main

import "os"
import "encoding/csv"
import "io"

func parseRecord(record []string) {
	// language of the dictionary,
	// "C" means chinese dictionary, "E" means non-chinese dictionary.
	lang := record[0]
	// id of the dictionary. Each dictionary has a unique value.
	id := record[1]
	// name of the dictionary.
	name := record[2]
	// name and author of the dictionary.
	author := record[3]

	switch lang {
	case "C":
		print("Chinese Dic ")
	case "E":
		print("non-Chinese Dic ")
	default:
		panic("wrong lang")
	}
	println(id + name + author)
}

func main() {
	const bookCsvPath = "data/dictionary/dict-books.csv"

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
		parseRecord(record)
	}
}
