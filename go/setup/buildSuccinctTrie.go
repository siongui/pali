package main

import "github.com/siongui/go-succinct-data-structure-trie"
import "path/filepath"
import "os"
import "io/ioutil"
import "strconv"

func main() {
	// set alphabet of words
	bits.SetAllowedCharacters("abcdeghijklmnoprstuvyāīūṁṃŋṇṅñṭḍḷ…'’° -")
	// encode: build succinct trie
	te := bits.Trie{}
	te.Init()

	i := 0
	// walk all word json files
	filepath.Walk("website/json", func(path string, info os.FileInfo, err error) error {
		if !info.IsDir() {
			word := info.Name()[:len(info.Name())-5]
			print(i)
			print(" ")
			println(word)
			// encode: insert words
			te.Insert(word)
			i++
		}
		return nil
	})
	// encode: trie encoding
	teData := te.Encode()
	//println(teData)
	ioutil.WriteFile("website/strie.txt", []byte(teData), 0644)
	println(te.GetNodeCount())
	ioutil.WriteFile("website/strie_node_count.txt", []byte(strconv.Itoa(int(te.GetNodeCount()))), 0644)
	// encode: build cache for quick lookup
	rd := bits.CreateRankDirectory(teData, te.GetNodeCount()*2+1, bits.L1, bits.L2)
	//println(rd.GetData())
	ioutil.WriteFile("website/rd.txt", []byte(rd.GetData()), 0644)
}
