SHELL := /bin/bash

help: ## show help.
	@gawk -f sh/makehelp.awk $(MAKEFILE_LIST)

ok: ~/gits/moot ## set up baseline
	chmod +x *.py

push: ## save to cloud
	@read -p "Reason? " msg; git commit -am "$$msg"; git push; git status

ghReset:
	git remote set-url origin https://timmenzies@github.com/timmenzies/xai.git

~/gits/moot:  ## get the data
	mkdir -p ~/gits
	git clone http://tiny.cc/moot $@
