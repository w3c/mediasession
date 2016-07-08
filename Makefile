index.html: index.bs
	./format.py $<
	curl https://api.csswg.org/bikeshed/ -F file=@$< > $@
