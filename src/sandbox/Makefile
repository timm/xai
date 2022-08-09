R=$(shell git rev-parse --show-toplevel)

~/tmp/%.html : %.lua
	@docco -l classic -o ~/tmp $<

../../docs/%.pdf : %.lua  ## make pdf
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

common:
	egrep '\<l\>.' rl.lua rlgo.lua \
	| sed 's/l\./LL/g' \
	| grep -o -E "(\w|')+" \
	| grep LL | sort | uniq -c | sort -n
