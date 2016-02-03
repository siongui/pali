# cannot use relative path in GOROOT, otherwise 6g not found. For example,
#   export GOROOT=../go  (=> 6g not found)
# it is also not allowed to use relative path in GOPATH
export GOROOT=$(realpath ../../go)
export GOPATH=$(realpath .)
export PATH := $(GOROOT)/bin:$(GOPATH)/bin:$(PATH)

SCSSDIR=theme/styling
WEBSITE_DIR=website
WEBSITE_JSON_DIR=$(WEBSITE_DIR)/json
PRODUCTION_DIR=src/github.com/siongui/pali-dictionary


devserver: js
	go run server.go

production:
	rm -rf $(PRODUCTION_DIR)
	git clone https://github.com/siongui/pali-dictionary.git $(PRODUCTION_DIR)
	mkdir $(PRODUCTION_DIR)/output
	cp theme/index.html $(PRODUCTION_DIR)/output
	gopherjs build gopherjs/*.go -m -o $(PRODUCTION_DIR)/output/pali.js
	python -mscss < $(SCSSDIR)/style.scss -I $(SCSSDIR) -o $(PRODUCTION_DIR)/output/style.css
	@# Google Search: makefile change directory
	@# http://stackoverflow.com/questions/1789594/how-to-write-cd-command-in-makefile
	cd $(PRODUCTION_DIR); ghp-import output; git push origin gh-pages

js:
	gopherjs build gopherjs/*.go -o $(WEBSITE_DIR)/pali.js

scss:
	python -mscss < $(SCSSDIR)/style.scss -I $(SCSSDIR) -o $(WEBSITE_DIR)/style.css

html:
	cp theme/index.html $(WEBSITE_DIR)

blobgo:
	@go run setup/setuppath.go setup/createblob.go

succinct_trie:
	@go run setup/setuppath.go setup/buildSuccinctTrie.go

parsewords: dir
	@go run setup/setuppath.go setup/setuplib.go setup/parsewords.go

parsebooks: dir
	@go run setup/setuppath.go setup/setuplib.go setup/parsebooks.go

dir:
	@[ -d $(WEBSITE_JSON_DIR) ] || mkdir -p $(WEBSITE_JSON_DIR)

fmt:
	@go fmt setup/*.go
	@go fmt lib/*.go
	@go fmt gopherjs/*.go
	@go fmt server.go

clone:
	@git clone https://github.com/siongui/data.git

install: lib_pali lib_opencc lib_pyScss lib_succinct_trie
	go get -u github.com/gopherjs/gopherjs
	go get -u github.com/chai2010/gettext-go/gettext
	@#-go get -u honnef.co/go/js/dom
	@#-go get -u honnef.co/go/js/xhr

lib_pali:
	rm -rf src/github.com/siongui/pali/
	go get -u github.com/siongui/pali/go/lib

lib_opencc:
	sudo apt-get install opencc libopencc-dev
	go get -u github.com/siongui/go-opencc

lib_pyScss:
	sudo apt-get install python-pip
	sudo pip install pyScss

lib_go_libsass:
	go get -u github.com/wellington/go-libsass

lib_succinct_trie:
	go get -u github.com/siongui/go-succinct-data-structure-trie

test_lib_pali:
	rm -rf src/github.com/siongui/pali/go/lib/
	cp -r lib/ src/github.com/siongui/pali/go/
	go get github.com/siongui/pali/go/lib

clean:
	rm -rf bin pkg src data website
