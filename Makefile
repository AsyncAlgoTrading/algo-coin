CONFIG=./config/sandbox_gemini.cfg
EXCHANGE=gemini
CURRENCY=USD


runconfig:  ## Clean and make target, run target
	python3 -m algocoin --config=$(CONFIG)

run:  clean ## Clean and make target, run target
	python3 -m algocoin --live --verbose=$(VERBOSE) --exchange=$(EXCHANGE)

sandbox:  ## Clean and make target, run target
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


tests: ## Clean and Make unit tests
	python3 -m nose -v algocoin/tests --with-coverage --cover-erase --cover-package=`find algocoin -name "*.py" | sed "s=\./==g" | sed "s=/=.=g" | sed "s/.py//g" | tr '\n' ',' | rev | cut -c2- | rev`

test: ## run the tests for travis CI
	@ python3 -m nose -v algocoin/tests --with-coverage --cover-erase --cover-package=`find algocoin -name "*.py" | sed "s=\./==g" | sed "s=/=.=g" | sed "s/.py//g" | tr '\n' ',' | rev | cut -c2- | rev`

test_verbose: ## run the tests with full output
	python3 -m nose -vv -s algocoin/tests --with-coverage --cover-erase --cover-package=`find algocoin -name "*.py" | sed "s=\./==g" | sed "s=/=.=g" | sed "s/.py//g" | tr '\n' ',' | rev | cut -c2- | rev`

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

install: ## install the package
	python3 setup.py install

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean run runconfig sandbox backtest backtest_config test tests test_verbose help install docs data
