package main

/* currently not used */

import (
	"bufio"
	"flag"
	"fmt"
	"github.com/siongui/go-opencc"
	"os"
	"path/filepath"
	"strings"
)

var cs2t *opencc.Converter

func File2lines(filePath string) []string {
	f, err := os.Open(filePath)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	var lines []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		panic(err)
	}

	return lines
}

func tw2cn(twPOPath, cnPOPath string) {
	os.MkdirAll(filepath.Dir(cnPOPath), 0755)
	fo, err := os.Create(cnPOPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		panic(err)
	}
	defer fo.Close()

	for _, line := range File2lines(twPOPath) {
		if strings.HasPrefix(line, "msgstr") {
			fo.Write([]byte(ct2s.Convert(line)))
		} else {
			if strings.Contains(line, "zh_TW") {
				fo.Write([]byte(strings.Replace(line, "zh_TW", "zh_CN", 1)))
			} else {
				fo.Write([]byte(line))
			}
		}
		fo.Write([]byte("\n"))
	}
}

func main() {
	twPOPath := flag.String("tw", "locale/zh_TW/LC_MESSAGES/messages.po", "Path of zh_TW PO file")
	cnPOPath := flag.String("cn", "locale/zh_CN/LC_MESSAGES/messages.po", "Path of zh_CN PO file")
	openccConf := flag.String("confopencc", "zhs2zht.ini", "OpenCC Configuration")
	flag.Parse()

	cs2t = opencc.NewConverter(*openccConf)
	defer cs2t.Close()

	tw2cn(*twPOPath, *cnPOPath)
}
