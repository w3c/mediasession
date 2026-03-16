LOCAL_BIKESHED := $(shell command -v bikeshed 2> /dev/null)

index.html: index.bs
	./format.py $<
ifndef LOCAL_BIKESHED
	curl https://www.w3.org/publications/spec-generator/ -F type=bikeshed-spec -F file=@$< > $@
else
	bikeshed spec
endif
