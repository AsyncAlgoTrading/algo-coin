run: clean  ## clean and make target, run target
	python3 -m algocoin live

sandbox: clean  ## clean and make target, run target
	python3 -m algocoin sandbox

backtest: clean  ## clean and make target, run target
	python3 -m algocoin backtest

tests: clean ## Clean and Make unit tests
	python3 -m nose -v algocoin/tests --with-coverage --cover-erase --cover-package=`ls ./algocoin/*.py ./algocoin/lib/exchanges/*.py ./algocoin/lib/*.py | sed "s=\./==g" | sed "s=/=.=g" | sed "s/.py//g" | tr '\n' ',' | rev | cut -c2- | rev`

test: ## run the tests for travis CI
	@ python3 -m nose -v algocoin/tests --with-coverage --cover-erase --cover-package=`ls ./algocoin/*.py ./algocoin/lib/exchanges/*.py ./algocoin/lib/*.py | sed "s=\./==g" | sed "s=/=.=g" | sed "s/.py//g" | tr '\n' ',' | rev | cut -c2- | rev`
 

test_verbose: ## run the tests with full output
	python3 -m nose -vv -s algocoin/tests --with-coverage --cover-erase --cover-package=`ls ./algocoin/*.py ./algocoin/lib/exchanges/*.py ./algocoin/lib/*.py | sed "s=\./==g" | sed "s=/=.=g" | sed "s/.py//g" | tr '\n' ',' | rev | cut -c2- | rev`
 

clean: ## clean the repository
	rm -rf *.pyc __pycache__ algocoin/__pycache__ algocoin/*.pyc algocoin/lib/__pycache__ algocoin/lib/*.pyc algocoin/tests/__pycache__ algocoin/tests/*.pyc algocoin/lib/exchanges/*.pyc algocoin/lib/exchanges/__pycache__ .coverage cover htmlcov

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean run sandbox backtest test tests test_verbose help
