.PHONY: format isort black test

install:
	cd tests && poetry install --no-root --sync

format: isort black

isort:
	isort .

black:
	black .

test:
	cd tests && poetry run pytest -vv . ${ARG}
