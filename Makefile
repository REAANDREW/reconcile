
.PHONY: install
install:
	pip install --user -e .

.PHONY: format
format:
	find . -name '*.py'|grep -v migrations|xargs autoflake --in-place --remove-all-unused-imports --remove-unused-variables
	autopep8 --in-place --aggressive --aggressive **/*.py

.PHONY: test
test:
	nosetests --all-modules --traverse-namespace --with-coverage --cover-min-percentage=95 --cover-package=reconcile --cover-inclusive --cover-html

.PHONY: lint
lint:
	pylint --rcfile pylint.rc --disable=missing-docstring --msg-template='{msg_id}:{path}:{symbol}:{line:3d},{column}: {obj}: {msg}' **/*.py

.PHONY: build
build: install test lint test

.PHONY: run
run: build
	FLASK_APP=reconcile FLASK_DEBUG=true flask run

