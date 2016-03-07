export GOROOT=$(realpath ../go)
export GOPATH=$(realpath .)
export PATH := $(GOROOT)/bin:$(GOPATH)/bin:$(PATH)

DATA_REPO_DIR=$(CURDIR)/data
COMMON_DIR=$(CURDIR)/common
LOCALE_DIR=$(COMMON_DIR)/locale
DICTIONARY_DIR=$(CURDIR)/dictionary
TIPITAKA_DIR=$(CURDIR)/tipitaka

parsetpk:
	@echo "\033[92mParsing Tipitaka data ...\033[0m"
	@python $(TIPITAKA_DIR)/setup/init1getTocs.py
	@python $(TIPITAKA_DIR)/setup/init2tocsToJson.py
	@python $(TIPITAKA_DIR)/setup/init3addSubpathInJson.py

dicdevserver:
	cd $(DICTIONARY_DIR); python devNotGaeRun.py

mindiccss:
	@echo "\033[92m(Dictionary) TODO: minify css ...\033[0m"
	@cp $(DICTIONARY_DIR)/app/css/app.css $(DICTIONARY_DIR)/app/css/app.min.css

mindicjs:
	@echo "\033[92m(Dictionary) Concatenate and compress js ...\033[0m"
	@go fmt $(DICTIONARY_DIR)/minjs.go
	@go run $(DICTIONARY_DIR)/minjs.go

setup: install cptpkcss symlinks pot initenuspo lib_opencc twpo2cn po2mo ngjs parsedics prefix_words_html succinct_trie ngdatajs

ngdatajs:
	@echo "\033[92mCreating ng js module for books info and succinct trie data...\033[0m"
	@python $(DICTIONARY_DIR)/setup/init4jsonToJS.py

succinct_trie:
	@echo "\033[92mCreating succinct trie json ...\033[0m"
	@cp $(DATA_REPO_DIR)/src/succinct_trie.json $(DICTIONARY_DIR)/pylib/json/

prefix_words_html:
	@echo "\033[92mCreating prefix-words HTML ...\033[0m"
	@python $(DICTIONARY_DIR)/setup/init3prefixWordsHtml.py

parsedics:
	@echo "\033[92mParse Dictionary Books Information ...\033[0m"
	@python $(DICTIONARY_DIR)/setup/init1parseBooks.py
	@echo "\033[92mParse Dictionary Words ...\033[0m"
	@python $(DICTIONARY_DIR)/setup/init2parseWords.py

ngjs:
	@echo "\033[92mCreating client-side i18n js ...\033[0m"
	@python setup/i18nUtils.py js

po2mo:
	@echo "\033[92mmsgfmt PO to MO ...\033[0m"
	@msgfmt $(LOCALE_DIR)/zh_TW/LC_MESSAGES/messages.po -o $(LOCALE_DIR)/zh_TW/LC_MESSAGES/messages.mo
	@msgfmt $(LOCALE_DIR)/zh_CN/LC_MESSAGES/messages.po -o $(LOCALE_DIR)/zh_CN/LC_MESSAGES/messages.mo
	@msgfmt $(LOCALE_DIR)/vi_VN/LC_MESSAGES/messages.po -o $(LOCALE_DIR)/vi_VN/LC_MESSAGES/messages.mo
	@msgfmt $(LOCALE_DIR)/fr_FR/LC_MESSAGES/messages.po -o $(LOCALE_DIR)/fr_FR/LC_MESSAGES/messages.mo
	@msgfmt $(LOCALE_DIR)/en_US/LC_MESSAGES/messages.po -o $(LOCALE_DIR)/en_US/LC_MESSAGES/messages.mo

twpo2cn:
	@echo "\033[92mCreating zh_CN PO from zh_TW PO ...\033[0m"
	@cd go; go run setup/setuppath.go setup/twpo2cn.go

initenuspo:
	msginit --no-wrap --no-translator --input=$(LOCALE_DIR)/messages.pot --locale=en_US -o $(LOCALE_DIR)/en_US/LC_MESSAGES/messages.po

pot:
	@echo "\033[92mCreating PO template ...\033[0m"
	@xgettext --no-wrap --from-code=UTF-8 --keyword=_ --output=$(LOCALE_DIR)/messages.pot \
	`find $(DICTIONARY_DIR)/app -name *.html` \
	`find $(DICTIONARY_DIR)/pylib/partials -name *.html` \
	`find $(TIPITAKA_DIR)/app -name *.html` \
	`find $(TIPITAKA_DIR)/pylib/partials -name *.html`

cptpkcss:
	@echo "\033[92mCopying tipitaka css ...\033[0m"
	@cp $(DATA_REPO_DIR)/tipitaka/romn/cscd/tipitaka-latn.css $(TIPITAKA_DIR)/app/css/

symlinks:
	@echo "\033[92mCreating symbolic links ...\033[0m"
	@[ -L $(TIPITAKA_DIR)/common ] || (cd $(TIPITAKA_DIR); ln -s $(COMMON_DIR) common)
	@[ -L $(TIPITAKA_DIR)/pylib/translation ] || (cd $(TIPITAKA_DIR)/pylib; ln -s $(DATA_REPO_DIR)/tipitaka/translation/ translation)
	@[ -L $(TIPITAKA_DIR)/pylib/romn ] || (cd $(TIPITAKA_DIR)/pylib; ln -s $(DATA_REPO_DIR)/tipitaka/romn/ romn)
	@[ -L $(DICTIONARY_DIR)/common ] || (cd $(DICTIONARY_DIR); ln -s $(COMMON_DIR) common)
	@[ -L $(COMMON_DIR)/pylib/jianfan ] || (cd $(COMMON_DIR)/pylib; ln -s $(DATA_REPO_DIR)/pylib/jianfan/ jianfan)

install:
	@echo "\033[92mInstalling git via apt-get ...\033[0m"
	@sudo apt-get install git
	@# gettext installed on Ubuntu 15.10 by default
	@#apt-cache policy gettext
	@echo "\033[92mInstalling Python webpy via apt-get ...\033[0m"
	@sudo apt-get install python-webpy
	@echo "\033[92mInstalling Python jinja2 via apt-get ...\033[0m"
	@sudo apt-get install python-jinja2
	@echo "\033[92mInstalling Python lxml via apt-get ...\033[0m"
	@#sudo apt-get install python-lxml

ubuntu_upgrade:
	@echo "\033[92mUpgrading Ubuntu Linux ...\033[0m"
	sudo apt-get update
	sudo apt-get upgrade

lib_opencc:
	@echo "\033[92mInstalling OpenCC and its Go binding ...\033[0m"
	sudo apt-get install opencc libopencc-dev
	go get -u github.com/siongui/go-opencc

clone:
	@echo "\033[92mClone Pāli data Repo ...\033[0m"
	@git clone https://github.com/siongui/data.git $(DATA_REPO_DIR)

clean:
	-rm $(TIPITAKA_DIR)/app/css/tipitaka-latn.css
	-rm $(DICTIONARY_DIR)/common
	-rm $(TIPITAKA_DIR)/common
	-rm $(TIPITAKA_DIR)/pylib/romn
	-rm $(TIPITAKA_DIR)/pylib/translation
	-rm $(COMMON_DIR)/pylib/jianfan
	-rm $(LOCALE_DIR)/messages.pot
	-rm $(LOCALE_DIR)/en_US/LC_MESSAGES/messages.po
	rm -rf $(LOCALE_DIR)/zh_CN/
	-rm `find $(LOCALE_DIR) -name *.mo`
	-rm common/app/scripts/services/data/i18nStrings.js
	rm -rf $(DICTIONARY_DIR)/pylib/json/
	rm -rf $(DICTIONARY_DIR)/pylib/paliwords/
	rm -rf $(DICTIONARY_DIR)/pylib/prefixWordsHtml/
	-rm common/app/scripts/services/data/dicBooks.js
	-rm common/app/scripts/services/data/succinctTrie.js
	-rm $(DICTIONARY_DIR)/app/all_compiled.js
	-rm $(DICTIONARY_DIR)/app/css/app.min.css
	rm -rf $(TIPITAKA_DIR)/build/
	rm -rf $(TIPITAKA_DIR)/pylib/json/
	rm -rf $(TIPITAKA_DIR)/app/scripts/services/data/
