APP = allocator
UV = uv run
PYTHON = python

.PHONY: run test lint format type clean

run:
	@$(UV) $(PYTHON) -m $(APP).main

lint:
	$(UV) ruff check src

format:
	$(UV) ruff format src

test:
	$(UV) pytest

type:
	$(UV) mypy src

clean:
	rm -rf __pycache__ .ruff_cache .mypy_cache .pytest_cache
