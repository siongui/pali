export GOROOT=$(realpath ../go)
export GOPATH=$(realpath .)
export PATH := $(GOROOT)/bin:$(GOPATH)/bin:$(PATH)

DATA_REPO_DIR=$(CURDIR)/data
COMMON_DIR=$(CURDIR)/common
LOCALE_DIR=$(COMMON_DIR)/locale
DICTIONARY_DIR=$(CURDIR)/dictionary
TIPITAKA_DIR=$(CURDIR)/tipitaka

pot:
	@echo "\033[92mCreating PO template ...\033[0m"
	@xgettext --no-wrap --from-code=UTF-8 --keyword=_ --output=$(LOCALE_DIR)/messages.pot \
	`find $(DICTIONARY_DIR)/app -name *.html` \
	`find $(DICTIONARY_DIR)/pylib/partials -name *.html` \
	`find $(TIPITAKA_DIR)/app -name *.html` \
	`find $(TIPITAKA_DIR)/pylib/partials -name *.html`

setup: cptpkcss symlinks

cptpkcss:
	@echo "\033[92mCopying tipitaka css ...\033[0m"
	@cp $(DATA_REPO_DIR)/tipitaka/romn/cscd/tipitaka-latn.css $(TIPITAKA_DIR)/app/css/

symlinks:
	@echo "\033[92mCreating symbolic links ...\033[0m"
	@[ -L $(TIPITAKA_DIR)/common ] || (cd $(TIPITAKA_DIR); ln -s $(COMMON_DIR) common)
	@[ -L $(TIPITAKA_DIR)/pylib/translation ] || (cd $(TIPITAKA_DIR)/pylib; ln -s $(DATA_REPO_DIR)/tipitaka/translation/ translation)
	@[ -L $(TIPITAKA_DIR)/pylib/romn ] || (cd $(TIPITAKA_DIR)/pylib; ln -s $(DATA_REPO_DIR)/tipitaka/romn/ romn)
	@[ -L $(DICTIONARY_DIR)/common ] || (cd $(DICTIONARY_DIR); ln -s $(COMMON_DIR) common)

install:
	@echo "\033[92mInstalling git via apt-get ...\033[0m"
	@#sudo apt-get install git
	@# gettext installed on Ubuntu 15.10 by default
	@#apt-cache policy gettext
	@echo "\033[92mInstalling Python webpy via apt-get ...\033[0m"
	@#sudo apt-get install python-webpy
	@echo "\033[92mInstalling Python jinja2 via apt-get ...\033[0m"
	@#sudo apt-get install python-jinja2
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
