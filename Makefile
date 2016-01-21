# Simple makefile with common rules.

makefiles_dir = .makefiles
include $(makefiles_dir)/rst2html.mk

PYTHON=/data/apps/anaconda/bin/python
HG=`which hg`

help:
	@echo 'Commonly used make targets:'
	@echo '  test - run all tests in the automatic test suite'
	@echo '  test-all - also run blacklisted tests'

test:
	cd tests && $(PYTHON) run-tests.py -f --blacklist=BLACKLIST --with-hg=$(HG) $(TESTFLAGS)

test-all:
	cd tests && $(PYTHON) run-tests.py --with-hg=$(HG) $(TESTFLAGS)

.PHONY: help test test-all
