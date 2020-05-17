.PHONY: clean
clean:
	rm -rf htmlcov
	rm -f .coverage
	rm -f coverage.xml
	rm -rf __pycache__
	rm -rf .mypy_cache

.PHONY: test
test:
	@python3 -m unittest -v

.PHONY: type-check
type-check:
	# requires mypy module
	@mypy merge.py

.PHONY: coverage
coverage:
	@coverage run -m unittest test_merge.py
	@coverage html
	@python3 -m http.server 8000 --directory htmlcov/

.PHONY: codecov
codecov: clean
	@coverage run test_merge.py
	@bash <(curl -s https://codecov.io/bash) -t 65bd25f1-60c7-415b-b825-1356e9f012d6