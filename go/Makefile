# cannot use relative path in GOROOT, otherwise 6g not found. For example,
#   export GOROOT=../go  (=> 6g not found)
# it is also not allowed to use relative path in GOPATH
export GOROOT=$(realpath ../../go)
export GOPATH=$(realpath .)
export PATH := $(GOROOT)/bin:$(GOPATH)/bin:$(PATH)

setUp:
	@go run setup/parsebooks.go

fmt:
	@go fmt setup/parsebooks.go

clone:
	@git clone https://github.com/siongui/data.git

install:
	-go get -u github.com/gopherjs/gopherjs
	-go get -u honnef.co/go/js/dom
	-go get -u honnef.co/go/js/xhr
