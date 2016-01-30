package main

import "github.com/siongui/pali/go/lib"
import "os"
import "encoding/csv"
import "io"
import "fmt"

var cs2t = lib.Zhs2zhtConverter()
var dicIndex = lib.GetDicIndex()

func processWordsCSV(csvPath string) {
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
		fmt.Println(record)
	}
}

func main() {
	defer cs2t.Close()
	fmt.Println(dicIndex)
	processWordsCSV(lib.WordsCSV1Path)
	processWordsCSV(lib.WordsCSV2Path)
}
