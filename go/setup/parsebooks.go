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
import "fmt"

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
		fmt.Println(record)
	}
}
