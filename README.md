# AlgoCoin
AlgoCoin is a python library for writing trading algorithms. It is designed using a combination of asyncio and callbacks to make writing cross-asset, cross-currency, and cross exchange algorithms for backtesting and live trading as simple as possible. 

# WARNING: Code refactoring still in progress

[![Build Status](https://travis-ci.org/timkpaine/algo-coin.svg?branch=master)](https://travis-ci.org/timkpaine/algo-coin)
[![Coverage](https://codecov.io/gh/timkpaine/algo-coin/coverage.svg?branch=master&token=JGqz8ChQxd)](https://codecov.io/gh/timkpaine/algo-coin)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/algo-coin/Lobby)
[![BCH compliance](https://bettercodehub.com/edge/badge/timkpaine/algo-coin?branch=master)](https://bettercodehub.com/)
[![License](https://img.shields.io/github/license/timkpaine/algo-coin.svg)](https://pypi.python.org/pypi/algocoin)
[![PyPI](https://img.shields.io/pypi/v/algocoin.svg)](https://pypi.python.org/pypi/algocoin)
[![Docs](https://img.shields.io/readthedocs/algo-coin.svg)](http://algo-coin.readthedocs.io/en/latest/)

## Overview 
Lightweight, extensible program for algorithmically trading cryptocurrencies and derivatives across multiple exchanges. 

### System Architecture
AlgoCoin is an event based trading system written in python. It is built on [aat](https://github.com/timkpaine/aat).

### Markets
AlgoCoin will support all exchanges and currencies covered by [ccxt](https://github.com/ccxt/ccxt)

---

## Getting Started
### Installation
Install the library from pip:

```python
pip install algocoin
```

Install the library from source:

```python
python setup.py install
```

## Documentation
Refer to the documentation for [aat](https://github.com/timkpaine/aat).

## Screenshots
### Backtest
[![](docs/img/bt.png)]()

### UI
#### Accounts overview
[![](docs/img/ui1.png)]()

#### Instrument registry
[![](docs/img/ui2.png)]()

#### Live trades
[![](docs/img/ui3.png)]()

#### Last price per asset/exchange
[![](docs/img/ui4.png)]()

#### Strategy trade requests/trade results
[![](docs/img/ui5.png)]()