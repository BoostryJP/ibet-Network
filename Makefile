.PHONY: install update format isort black test

install:
	cd tests && poetry install --no-root --sync

update:
	cd tests && poetry update

format: isort black

isort:
	isort .

black:
	black .

test:
	cd tests && poetry run pytest -vv . ${ARG}
