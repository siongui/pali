package main

import "github.com/siongui/gopherjs-i18n/tool"

func main() {
	po2json.PO2JSON(poDomain, localeDir, poJsonPath)
}
