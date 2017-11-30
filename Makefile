# Simple makefile with common rules.

makefiles_dir = .makefiles
include $(makefiles_dir)/rst2html.mk

# This gets the version of python that mercurial uses
PYTHON="$$(shebang=$$(head -n1 $$(type -p hg));echo $${shebang:2})"
HG=`which hg`
MMF_SETUP=$(shell pwd)/mmf_setup

nbinit.py: make_nbinit.py mmf_setup/_data/nbthemes/mmf.*
	python make_nbinit.py

help:
	@echo 'Commonly used make targets:'
	@echo '  test - run all tests in the automatic test suite'

test:
	cd tests && MMF_SETUP=$(MMF_SETUP) $(PYTHON) run-tests.py --with-hg=$(HG) $(TESTFLAGS)

.PHONY: help test test-all
