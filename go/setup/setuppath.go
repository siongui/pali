package main

// input
const localeDir = "../common/locale"
const poDomain = "messages"

// template of website
const htmlTemplateDir = "theme/template"

//const tipitakaURL = "https://epalitipitaka.appspot.com/"
const tipitakaURL = "http://tipitaka.sutta.org/"

// output
const WebsiteDir = "website"
const trieDataPath = WebsiteDir + "/strie.txt"
const trieNodeCountPath = WebsiteDir + "/strie_node_count.txt"
const rankDirectoryDataPath = WebsiteDir + "/rd.txt"
const blobTemplatePath = "setup/blob.tpl"
const blobFilePath = "gopherjs/blob.go"
const indexHtmlPath = WebsiteDir + "/index.html"
const poJsonPath = WebsiteDir + "/po.json"
