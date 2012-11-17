# Documentation.  Automatic compilation of the README.rst file to aid editing

.README.html: README.rst
	rst2html.py $< > $@
	open $@; sleep 1; open $<

watch:
	while sleep 1; do make -q rst-html || make rst-html ; done

rst-html: .README.html

# Python Setup

# Updates the requirements to match the version on this machin
extended_requirements.txt: minimal_requirements.txt
	pip freeze -r $^ > $@

.PHONY: watch rst-html
