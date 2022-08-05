MAKEFLAGS += --silent
SHELL:= /bin/bash#
R=$(shell git rev-parse --show-toplevel)

WEB=$(HOME)/gits/baittery/baittery.github.io

help : Makefile
	echo ""; printf "usage: make [OPTIONS]\n\n"
	@gawk 'BEGIN {FS="[ \t]*:.*##[ \t]*"}  \
	  NF==2 { printf \
           "  \033[36m%-25s\033[0m %s\n","make " $$1,$$2}'  $< \
	| grep -v awk

loc:
	gawk '!/^(--|[ \t]*$$)/{n++} END {print n" lines"}' *.lua

ready:  ##  commit to main
	git add *;git commit -am save;git push;git status

LUAS = $(wildcard [a-z]*.lua)

htmls:  $(subst .lua,.html,../docs/$(subst lua ,html ../docs/,$(LUAS))) ## make all htmls
	cp -r docs/* $(WEB)/
	(cd $(WEB); git  add *; git commit -am save; git push)

../docs/%.html: %.lua  ## make html
	gawk -f $R/etc/lua2doc.awk $< > tmp.lua
	echo "docco: $< -> $@"
	docco -l classic -o $R/docs tmp.lua > /dev/null
	gawk 'sub(/>tmp.lua</,">$(basename $<)<") 1 ' $R/docs/tmp.html > $@
	cp $R/etc/docco.css $R/docs/docco.css

../docs/%.pdf : %.lua  ## make pdf
	@mkdir -p $R/docs
	@echo "pdf-ing $@ ... "
	@a2ps -Bjr             \
		-q                    \
		-L 125                 \
		--line-numbers=1        \
		--highlight-level=normal \
		--borders=no              \
		--pro=color                \
		--columns 3                 \
		--right-footer=""            \
		--left-footer=""              \
		--pretty-print=$R/etc/lua.ssh  \
		--footer="page %p."             \
		-M letter                        \
		-o $@.ps $<
	@ps2pdf $@.ps $@; rm $@.ps; git add $@
