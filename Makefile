.PHONY: help install install-tools install-tests update format isort black test

POETRY = env -u VIRTUAL_ENV poetry

help:
	@echo "Available targets:"
	@echo "  help           Show this help message"
	@echo "  install        Install root and tests dependencies"
	@echo "  install-tools  Install root project dependencies"
	@echo "  install-tests  Install tests project dependencies"
	@echo "  update         Update root and tests dependencies"
	@echo "  format         Run isort and black"
	@echo "  isort          Run isort"
	@echo "  black          Run black"
	@echo "  test           Run tests (use ARG=... for extra pytest args)"

install:
	$(MAKE) install-tools
	$(MAKE) install-tests

install-tools:
	$(POETRY) sync --with dev --no-root

install-tests:
	$(POETRY) -C tests sync --with dev --no-root

update:
	$(POETRY) update
	$(POETRY) -C tests update

format: isort black

isort:
	$(POETRY) run isort .

black:
	$(POETRY) run black .

test:
	$(POETRY) -C tests run pytest -vv . ${ARG}
