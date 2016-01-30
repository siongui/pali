package main

import "net/http"
import "github.com/siongui/pali/go/lib"

func main() {
	http.ListenAndServe(":8000", http.FileServer(http.Dir(lib.WebsiteDir)))
}
