package main

import (
	"encoding/csv"
	"flag"
	"github.com/siongui/gojianfan"
	"github.com/siongui/pali/go/lib"
	"io"
	"os"
	"strings"
)

func isChineseDictionary(id string) bool {
	// id of Chinese Dictionary: D G Z X H W F T J M
	switch id {
	case "D", "G", "Z", "X", "H", "W", "F", "T", "J", "M":
		return true
	default:
		return false
	}
}

func processWord(record []string, wordsJsonDir string) {
	// number of the word, useless
	num := record[0]

	// id of the book which the word belongs to
	bookId := record[2]

	// word (The first character of the cell may be upper-case)
	// Google search: golang lowercase
	word := strings.ToLower(record[4])

	// explanation of the pali word in one dictionary
	explanation := record[6]

	println(num + " " + word)
	// Google search: golang check if file exists
	path := GetWordPath(word, wordsJsonDir)
	if _, err := os.Stat(path); err == nil {
		// append new data to existing json file
		wi := GetBookIdWordExps(word, wordsJsonDir)
		if isChineseDictionary(bookId) {
			// convert simplified chinese to traditional chinese
			wi[bookId] = gojianfan.S2T(explanation)
		} else {
			wi[bookId] = explanation
		}
		SaveJsonFile(wi, path)
	} else {
		// create new json file
		wi := lib.BookIdWordExps{}
		if isChineseDictionary(bookId) {
			// convert simplified chinese to traditional chinese
			wi[bookId] = gojianfan.S2T(explanation)
		} else {
			wi[bookId] = explanation
		}
		SaveJsonFile(wi, path)
	}
}

func processWordsCSV(csvPath, wordsJsonDir string) {
	// open csv file
	fcsv, err := os.Open(csvPath)
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
		processWord(record, wordsJsonDir)
	}
}

func main() {
	dicDataDir := flag.String("dic", "data/dictionary", "Directory of Dictioanry Data")
	wordsJsonDir := flag.String("outputdir", "website/json", "Output Directory of Parsed Words")

	flag.Parse()
	WordsCSV1Path := *dicDataDir + "/dict_words_1.csv"
	WordsCSV2Path := *dicDataDir + "/dict_words_2.csv"

	processWordsCSV(WordsCSV1Path, *wordsJsonDir)
	processWordsCSV(WordsCSV2Path, *wordsJsonDir)
}
