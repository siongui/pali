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
LOCALE_DIR=../common/locale


devserver: html js scss
	@# http://stackoverflow.com/a/5947779
	@echo "\033[92mDevelopment Server Running ...\033[0m"
	@go run server.go

production:
	@echo "\033[92mClone Remote Repo ...\033[0m"
	rm -rf $(PRODUCTION_DIR)
	git clone https://github.com/siongui/pali-dictionary.git $(PRODUCTION_DIR)
	@echo "\033[92mGenerating HTML ...\033[0m"
	mkdir $(PRODUCTION_DIR)/output
	go run setup/setuppath.go setup/html.go > $(PRODUCTION_DIR)/output/index.html
	@echo "\033[92mGenerating JavaScript ...\033[0m"
	gopherjs build gopherjs/*.go -m -o $(PRODUCTION_DIR)/output/pali.js
	@echo "\033[92mGenerating CSS ...\033[0m"
	@# TODO: use github.com/wellington/go-libsass
	python -mscss < $(SCSSDIR)/style.scss -I $(SCSSDIR) -o $(PRODUCTION_DIR)/output/style.css
	@echo "\033[92mPush to Remote Repo ...\033[0m"
	@# Google Search: makefile change directory
	@# http://stackoverflow.com/questions/1789594/how-to-write-cd-command-in-makefile
	cd $(PRODUCTION_DIR); ghp-import output; git push origin gh-pages

js:
	@echo "\033[92mGenerating JavaScript ...\033[0m"
	@gopherjs build gopherjs/*.go -o $(WEBSITE_DIR)/pali.js

scss:
	@echo "\033[92mGenerating CSS ...\033[0m"
	@go run setup/setuppath.go setup/scss.go
	@#python -mscss < $(SCSSDIR)/style.scss -I $(SCSSDIR) -o $(WEBSITE_DIR)/style.css

html:
	@echo "\033[92mGenerating HTML ...\033[0m"
	@# Google Search: shell stdout to file
	@go run setup/setuppath.go setup/html.go > $(WEBSITE_DIR)/index.html

blobgo:
	@echo "\033[92mGenerating blob data to be used in client-side/browser ...\033[0m"
	@go run setup/setuppath.go setup/createblob.go

succinct_trie:
	@echo "\033[92mBuilding Succinct Trie ...\033[0m"
	@go run setup/setuppath.go setup/buildSuccinctTrie.go

po2json:
	@echo "\033[92mConverting PO files to JSON (to be used in client-side/browser) ...\033[0m"
	@go run setup/setuppath.go setup/po2json.go

twpo2cn:
	@echo "\033[92mCreating zh_CN PO from zh_TW PO ...\033[0m"
	@go run setup/setuppath.go setup/twpo2cn.go

parsewords: dir
	@echo "\033[92mParse Dictionary Words ...\033[0m"
	@go run setup/setuppath.go setup/setuplib.go setup/parsewords.go

parsebooks: dir
	@echo "\033[92mParse Dictionary Books Information ...\033[0m"
	@go run setup/setuppath.go setup/setuplib.go setup/parsebooks.go

dir:
	@echo "\033[92mCreate website directory if not exists ...\033[0m"
	@[ -d $(WEBSITE_JSON_DIR) ] || mkdir -p $(WEBSITE_JSON_DIR)

fmt:
	@echo "\033[92mGo fmt source code...\033[0m"
	@go fmt setup/*.go
	@go fmt lib/*.go
	@go fmt gopherjs/*.go
	@go fmt server.go

clone:
	@echo "\033[92mClone Pāli data Repo ...\033[0m"
	@git clone https://github.com/siongui/data.git

install: lib_pali lib_opencc lib_go_libsass lib_succinct_trie lib_ime_pali lib_gopherjs_i18n lib_gettext_go lib_gopherjs

lib_gopherjs:
	@echo "\033[92mInstalling GopherJS ...\033[0m"
	go get -u github.com/gopherjs/gopherjs
	@#-go get -u honnef.co/go/js/dom
	@#-go get -u honnef.co/go/js/xhr

lib_pali:
	@echo "\033[92mInstalling common lib used in this project ...\033[0m"
	rm -rf src/github.com/siongui/pali/
	go get -u github.com/siongui/pali/go/lib

lib_opencc:
	@echo "\033[92mInstalling OpenCC and its Go binding ...\033[0m"
	sudo apt-get install opencc libopencc-dev
	go get -u github.com/siongui/go-opencc

lib_pyScss: lib_normalize_css
	@echo "\033[92mInstalling pyScss ...\033[0m"
	sudo apt-get install python-pip
	sudo pip install pyScss

lib_go_libsass: lib_normalize_css
	@echo "\033[92mInstalling libsass and its Go binding ...\033[0m"
	go get -u github.com/wellington/go-libsass

lib_normalize_css:
	@echo "\033[92mInstalling Normalize.css ...\033[0m"
	@[ -e $(SCSSDIR)/_normalize302.scss ] || wget -O $(SCSSDIR)/_normalize302.scss http://necolas.github.com/normalize.css/3.0.2/normalize.css

lib_succinct_trie:
	@echo "\033[92mInstalling Go Succinct Trie library ...\033[0m"
	go get -u github.com/siongui/go-succinct-data-structure-trie

lib_ime_pali:
	@echo "\033[92mInstalling Online Go Pāli IME ...\033[0m"
	go get -u github.com/siongui/go-online-input-method-pali

lib_gopherjs_i18n:
	@echo "\033[92mInstalling GopherJS gettext library (online/client-side)...\033[0m"
	go get -u github.com/siongui/gopherjs-i18n

lib_gettext_go:
	@echo "\033[92mInstalling Go gettext library (offline/server-side) ...\033[0m"
	go get -u github.com/chai2010/gettext-go/gettext

po2mo:
	@echo "\033[92mmsgfmt PO to MO ...\033[0m"
	msgfmt $(LOCALE_DIR)/zh_TW/LC_MESSAGES/messages.po -o $(LOCALE_DIR)/zh_TW/LC_MESSAGES/messages.mo
	msgfmt $(LOCALE_DIR)/vi_VN/LC_MESSAGES/messages.po -o $(LOCALE_DIR)/vi_VN/LC_MESSAGES/messages.mo
	msgfmt $(LOCALE_DIR)/fr_FR/LC_MESSAGES/messages.po -o $(LOCALE_DIR)/fr_FR/LC_MESSAGES/messages.mo

test_lib_pali:
	rm -rf src/github.com/siongui/pali/go/lib/
	cp -r lib/ src/github.com/siongui/pali/go/
	go get github.com/siongui/pali/go/lib

clean:
	@echo "\033[92mClean Repo ...\033[0m"
	@#rm -rf bin pkg src data website
	rm -rf bin pkg src website
