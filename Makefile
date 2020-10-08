init:
	pipenv

test:
	python -m unittest discover -s tests

.PHONY: init test