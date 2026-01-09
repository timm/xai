SHELL := /bin/bash
GIT_ROOT := $(shell git rev-parse --show-toplevel 2>/dev/null)

help: ## show help.
	@gawk -f $(GIT_ROOT)/sh/makehelp.awk $(MAKEFILE_LIST)

ok: ~/gits/moot ## set up baseline
	chmod +x *.py

push: ## save to cloud
	@read -p "Reason? " msg; git commit -am "$$msg"; git push; git status

clean: ## remove pycadhe
	rm -rf __pycache__

ghReset:
	git remote set-url origin https://timmenzies@github.com/timmenzies/xai.git

#------------------------
# xai speicif stuff

tree: ok
	./xai.py --tree ~/gits/moot/optimize/misc/auto93.csv

xais: ok
	./xai.py --xais ~/gits/moot/optimize/misc/auto93.csv

~/gits/moot:  ## get the data
	mkdir -p ~/gits
	git clone http://tiny.cc/moot $@

#--------------------------
MY=@bash sh/ell

.PHONY: sh
.IGNORE: sh
sh: ## demo of my shell
	@-bash --init-file $(GIT_ROOT)/sh/ell -i

mytree: ## demo of my tree
	$(MY) tree

ls: ## demo of my ls
	$(MY) ls

tmux: ## demo of my tmux
	$(MY) tmux

grep: ## demo of my grep
	$(MY) grep es Makefile

col: ## demo of my col
	printf "name,age,city\nalice,30,raleigh\nbob,25,boston\ncarol,40,denver\n" \
		| bash $(GIT_ROOT)/sh/ell col



