export GOROOT=$(realpath ../go)
export GOPATH=$(realpath .)
export PATH := $(GOROOT)/bin:$(GOPATH)/bin:$(PATH)

symlinks:
	@echo "\033[92mCreating symbolic links ...\033[0m"
	[ -L tipitaka/common ] || (cd tipitaka; ln -s ../common/ common)
	[ -L tipitaka/pylib/translation ] || (ln -s ../../data/tipitaka/translation/ translation)
	[ -L tipitaka/pylib/romn ] || (ln -s ../../data/tipitaka/romn/ romn)
	[ -L dictionary/common ] || (cd dictionary; ln -s ../common/ common)

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
	@git clone https://github.com/siongui/data.git
