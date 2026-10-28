PYTHON ?= python3

.PHONY: help test lint sync install check

help:            ## Show this help
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-8s %s\n", $$1, $$2}'

test:            ## Run offline tests
	$(PYTHON) -m unittest discover tests -v

lint:            ## Style check (needs: pip install ruff)
	ruff check .

sync:            ## Copy shared/india_data.py into every skill
	$(PYTHON) scripts/sync_shared.py

install:         ## Install skills into ~/.claude/skills
	./install.sh

check: sync lint test  ## Everything CI runs
