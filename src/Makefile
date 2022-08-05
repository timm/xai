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

../docs/%.html: %.lua  README.md ## make html
	gawk -f $R/etc/lua2doc.awk $< > tmp.lua
	echo "docco: $< -> $@"
	docco -l classic  tmp.lua > /dev/null
	gawk 'sub(/>tmp.lua</,">$(basename $<)<") 1 ' $R/docs/tmp.html > $@
	cp $R/etc/docco.css docs/docco.css

../docs/%.md : %.lua  README.md
	echo $< 2>&1
	gawk -f 2md.awk $< > /tmp/page 2> /tmp/toc
	gawk 'sub(/TABLE.OF.CONTENTS/,"",$$0) {system("cat /tmp/toc")} 1' /tmp/page > $@


../docs/%.pdf : %.lua  ## make pdf
	@mkdir -p docs
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
