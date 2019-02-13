CONFIG=./config/sandbox_gemini.cfg
EXCHANGE=gemini
CURRENCY=USD


runconfig: buildinplace ## Clean and make target, run target
	python3 -m algocoin --config=$(CONFIG)

run:  clean buildinplace  ## Clean and make target, run target
	python3 -m algocoin --live --verbose=$(VERBOSE) --exchange=$(EXCHANGE)

sandbox: buildinplace  ## Clean and make target, run target
	python3 -m algocoin --sandbox --verbose=$(VERBOSE) -exchange=$(EXCHANGE)

data:  ## Fetch data for EXCHANGE
	. scripts/fetchdata.sh $(EXCHANGE) $(CURRENCY)

fetch_data: ## Fetch data for EXCHANGE
	. scripts/fetchdata.sh $(EXCHANGE) $(CURRENCY)

backtest_config: ## Clean and make target, run backtest
	python3 -m algocoin --config=./config/backtest_gemini.cfg

backtest: ## Clean and make target, run backtest
	python3 -m algocoin --backtest --verbose=$(VERBOSE) --exchange=$(EXCHANGE)

backtest_inline:  ## Clean and make target, run backtest, plot in terminal
	bash -c "export MPLBACKEND=\"module://itermplot\";	export ITERMPLOT=\"rv\"; python3 -m algocoin backtest $(VERBOSE) $(EXCHANGE)"

boost:  ## Install boost python dependencies on os x with homebrew
	brew install boost boost-python3
	sudo ln -s /usr/local/lib/libboost_python37.dylib /usr/local/lib/libboost_python.dylib

buildext: ## build the package extensions
	python3 setup.py build_ext

buildinplace: ## build the package extensions
	python3 setup.py build
	python3 setup.py build_ext
	cp -r build/`ls build | grep lib`/algocoin .

build: ## build the package
	python3 setup.py build

install: ## install the package
	python3 setup.py install

dist:  ## dist to pypi
	python3 setup.py sdist upload -r pypi

js:  ## build the js
	npm install
	npm run build

tests: ## Clean and Make unit tests
	python3 -m pytest ./build/`ls ./build | grep lib`/algocoin/tests --cov=algocoin

test: clean build lint ## run the tests for travis CI
	@ python3 -m pytest ./build/`ls ./build | grep lib`/algocoin/tests --cov=algocoin

test_verbose: ## run the tests with full output
	@ python3 -m nose2 -vv ./build/`ls ./build | grep lib`/algocoin/tests --with-coverage --coverage=algocoin

lint: ## run linter
	pylint algocoin || echo
	flake8 algocoin 

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
