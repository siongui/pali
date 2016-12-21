package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"text/template"
)

type JsData struct {
	BookIdAndInfosJson    string
	SuccinctTrieData      string
	SuccinctTrieNodeCount string
	RankDirectoryData     string
	PoJson                string
}

func main() {
	BookJsonPath := flag.String("input", "website/bookIdAndInfos.json", "Input Path of Parsed Dictionary Books Info")
	flag.Parse()
	bj, err := ioutil.ReadFile(*BookJsonPath)
	if err != nil {
		fmt.Println(err)
	}
	td, err := ioutil.ReadFile(trieDataPath)
	if err != nil {
		fmt.Println(err)
	}
	tc, err := ioutil.ReadFile(trieNodeCountPath)
	if err != nil {
		fmt.Println(err)
	}
	rd, err := ioutil.ReadFile(rankDirectoryDataPath)
	if err != nil {
		fmt.Println(err)
	}
	po, err := ioutil.ReadFile(poJsonPath)
	if err != nil {
		fmt.Println(err)
	}
	d := JsData{
		BookIdAndInfosJson:    string(bj),
		SuccinctTrieData:      string(td),
		SuccinctTrieNodeCount: string(tc),
		RankDirectoryData:     string(rd),
		PoJson:                string(po),
	}
	f, err := os.Create(blobFilePath)
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()
	t := template.Must(template.ParseFiles(blobTemplatePath))
	err = t.Execute(f, d)
	if err != nil {
		fmt.Println(err)
	}
}
