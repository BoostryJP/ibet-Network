.PHONY: format isort black test

install:
	pip install -r tests/requirements.txt

format: isort black

isort:
	isort .

black:
	black .

test:
	pytest tests/ ${ARG}
