init:
	pipenv

test:
	green -vvv

coverage:
	green -r

run:
	python ./src/semblance/semblance.py

.PHONY: init run test coverage
