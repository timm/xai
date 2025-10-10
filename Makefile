docs/index.html : docs/xai.html
	cp $^ $@

docs/%.html : %.md
	pandoc -s $^ -o $@
	open $@

push:
	git commit -am push; git push; git status
