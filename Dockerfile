FROM timkpaine/aat:latest

WORKDIR /usr/src/app
ADD . /usr/src/app

RUN python3.7 -m pip install -U codecov coverage pytest pytest-cov mock flake8 pylint
RUN python3.7 -m pip install -r requirements.txt

RUN DOCKER=true make test
RUN codecov --token 10cff21a-48fa-4326-9714-fd63aa7c785d
