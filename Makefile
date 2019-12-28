CONFIG=./config/simulation_gemini.cfg
EXCHANGE=gemini
CURRENCY=USD


runconfig: build ## Clean and make target, run target
	python3 -m algocoin --config=$(CONFIG)

run:  clean build  ## Clean and make target, run target
	python3 -m algocoin --live --verbose=$(VERBOSE) --exchange=$(EXCHANGE)

build: ## build the package
	python3 setup.py build

install: ## install the package
	python3 setup.py install

dist: js  ## dist to pypi
	rm -rf dist build
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	twine check dist/* && twine upload dist/*

js:  ## build the js
	yarn
	yarn build

fixtures:  ## make db fixtures
	python3 -m aat.persistence sqlite:///aat.db

tests: ## Clean and Make unit tests
	python3 -m pytest -v ./algocoin/tests --cov=algocoin
	yarn test

lint: ## run linter
	python3 -m flake8 algocoin 
	yarn lint

fix:  ## run autopep8/tslint fix
	python3 -m autopep8 --in-place -r -a -a algocoin/
	yarn fix

annotate: ## MyPy type annotation check
	mypy -s algocoin 

annotate_l: ## MyPy type annotation check - count only
	mypy -s algocoin | wc -l 

docs:  ## Build the sphinx docs
	make -C docs html

clean: ## clean the repository
	find . -name "__pycache__" | xargs rm -rf
	find . -name "*.pyc" | xargs rm -rf
	rm -rf .coverage cover htmlcov logs build dist *.egg-info
	find . -name "*.so"  | xargs rm -rf
	make -C ./docs clean

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean run runconfig sandbox backtest backtest_config test tests test_verbose help install docs data dist js build buildext boost
