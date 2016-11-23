run: clean  ## clean and make target, run target
	python3 main.py live

sandbox: clean  ## clean and make target, run target
	python3 main.py sandbox

backtest: clean  ## clean and make target, run target
	python3 main.py backtest

tests: clean ## Clean and Make unit tests
	python3 -m nose -v tests --with-coverage --cover-erase --cover-package=`ls ./*.py ./exchanges/*.py | sed "s=\./==g" | sed "s=/=.=g" | sed "s/.py//g" | tr '\n' ',' | rev | cut -c2- | rev`

test: ## run the tests for travis CI
	@ python3 -m nose -v tests --with-coverage --cover-erase --cover-package=`ls ./*.py ./exchanges/*.py | sed "s=\./==g" | sed "s=/=.=g" | sed "s/.py//g" | tr '\n' ',' | rev | cut -c2- | rev`
 

test_verbose: ## run the tests with full output
	python3 -m nose -vv -s tests --with-coverage --cover-erase --cover-package=`ls ./*.py ./exchanges/*.py | sed "s=\./==g" | sed "s=/=.=g" | sed "s/.py//g" | tr '\n' ',' | rev | cut -c2- | rev`
 

clean: ## clean the repository
	rm -rf *.pyc __pycache__ tests/__pycache__ tests/*.pyc exchanges/*.pyc exchange/__pycache__ .coverage cover htmlcov

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean run wave test tests target
