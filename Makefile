.PHONY: help install install-tools install-tests update format format-check isort black test typecheck

UV = env -u VIRTUAL_ENV UV_MALWARE_CHECK=1 uv

help:
	@echo "Available targets:"
	@echo "  help           Show this help message"
	@echo "  install        Install root and tests dependencies"
	@echo "  install-tools  Install root project dependencies"
	@echo "  install-tests  Install tests project dependencies"
	@echo "  update         Update root and tests dependencies"
	@echo "  format         Format code with isort and black"
	@echo "  format-check   Check formatting with isort and black"
	@echo "  isort          Run isort"
	@echo "  black          Run black"
	@echo "  typecheck      Run pyright"
	@echo "  test           Run tests (use ARG=... for extra pytest args)"

install:
	$(MAKE) install-tools
	$(MAKE) install-tests

install-tools:
	$(UV) sync --all-groups

install-tests:
	$(UV) --directory tests sync --all-groups

update:
	$(UV) lock --upgrade
	$(UV) --directory tests lock --upgrade

format: isort black

format-check:
	$(UV) run isort --check-only --diff .
	$(UV) run black --check .

isort:
	$(UV) run isort .

black:
	$(UV) run black .

typecheck:
	$(UV) run pyright

test:
	$(UV) --directory tests run pytest -vv . ${ARG}
