.PHONY: clean
clean:
	rm -rf htmlcov
	rm -f .coverage
	rm -f coverage.xml
	rm -rf __pycache__
	rm -rf merge/__pycache__
	rm -rf .mypy_cache

.PHONY: set-hooks
set-hooks:
	@git config core.hooksPath .githooks

.PHONY: test
test:
	@python3 -m unittest tests/test*.py -v

.PHONY: type-check
type-check:
	# requires mypy module
	@mypy merge.py

.PHONY: coverage
coverage: test
	@coverage html
	@python3 -m http.server 8000 --directory htmlcov/