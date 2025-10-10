SHELL     := bash
MAKEFLAGS += --warn-undefined-variables
.SILENT:
.ONESHELL:

LOUD = \033[1;34m#
HIGH = \033[1;33m#
SOFT = \033[0m#

Top=$(shell git rev-parse --show-toplevel)
Tmp ?= $(HOME)/tmp 

help: ## show help.
	@gawk '\
		BEGIN {FS = ":.*?##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\ntargets:\n"}  \
    /^[a-z0-9A-Z_%\.\/-]+:.*?##/ {printf("  \033[36m%-10s\033[0m %s\n", $$1, $$2) | "sort" } \
	' $(MAKEFILE_LIST)

pull: ## update from main
	git pull

push: ## commit to main
	echo -en "$(LOUD)Why this push? $(SOFT)" 
	read x ; git commit -am "$$x" ;  git push
	git status

sh: $(Top)/etc/hi.txt $(Top)/etc/bash.rc ## run custom shell
	clear; tput setaf 3; cat $(Top)/etc/hi.txt; tput sgr0
	$(Top)/etc/bash.rc


docs/index.html : docs/xai.html
	cp $^ $@

docs/%.html : %.md
	pandoc -s  $^ --toc  -o $@
	open $@


