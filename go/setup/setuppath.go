package main

// input
const BookCsvPath = "data/dictionary/dict-books.csv"
const WordsCSV1Path = "data/dictionary/dict_words_1.csv"
const WordsCSV2Path = "data/dictionary/dict_words_2.csv"

// template of website
const themeDir = "theme/template"
const indexTpl = themeDir + "/index.html"
const navbarTpl = themeDir + "/includes/navbar.html"
const imeTpl = themeDir + "/includes/ime.html"

// output
const WebsiteDir = "website"
const wordsJsonDir = WebsiteDir + "/json"
const BookJsonPath = WebsiteDir + "/bookIdAndInfos.json"
const trieDataPath = WebsiteDir + "/strie.txt"
const trieNodeCountPath = WebsiteDir + "/strie_node_count.txt"
const rankDirectoryDataPath = WebsiteDir + "/rd.txt"
const blobTemplatePath = "setup/blob.tpl"
const blobFilePath = "gopherjs/blob.go"
const indexHtmlPath = WebsiteDir + "/index.html"
