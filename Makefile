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
	@python3 -m pytest -v

.PHONY: type-check
type-check:
	# requires mypy module
	@mypy merge/merge.py

.PHONY: cov
cov:
	@coverage run -m unittest tests/test*.py

.PHONY: cov-xml
cov-xml: cov
	@coverage xml merge/merge.py

.PHONY: cov-report
cov-report: cov
	@coverage html
	@python3 -m http.server 8000 --directory htmlcov/
