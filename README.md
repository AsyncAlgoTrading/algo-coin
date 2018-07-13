# AlgoCoin
Algorithmic Trading Bitcoin. 

# WARNING: Code refactoring still in progress

[![Build Status](https://travis-ci.org/timkpaine/algo-coin.svg?branch=master)](https://travis-ci.org/timkpaine/algo-coin)
[![Coverage](https://codecov.io/gh/timkpaine/algo-coin/coverage.svg?branch=master&token=JGqz8ChQxd)](https://codecov.io/gh/timkpaine/algo-coin)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/algo-coin/Lobby)
[![Waffle.io](https://badge.waffle.io/timkpaine/algo-coin.png?label=ready&title=Ready)](https://waffle.io/timkpaine/algo-coin?utm_source=badge)
[![BCH compliance](https://bettercodehub.com/edge/badge/timkpaine/algo-coin?branch=master)](https://bettercodehub.com/)
[![Beerpay](https://beerpay.io/timkpaine/algo-coin/badge.svg?style=flat)](https://beerpay.io/timkpaine/algo-coin)
[![License](https://img.shields.io/github/license/timkpaine/algo-coin.svg)](https://pypi.python.org/pypi/algocoin)
[![PyPI](https://img.shields.io/pypi/v/algocoin.svg)](https://pypi.python.org/pypi/algocoin)
[![Docs](https://img.shields.io/readthedocs/algo-coin.svg)](http://algo-coin.readthedocs.io/en/latest/)
[![Site](https://img.shields.io/badge/Site--grey.svg?colorB=FFFFFF)](http://paine.nyc/algo-coin)

## Overview 
Lightweight, extensible program for algorithmically trading cryptocurrencies across multiple exchanges. 

### System Architecture
AlgoCoin is an event based trading system written in python. It comes with support for live trading across (and between) multiple exchanges, fully integrated backtesting support, slippage and transaction cost modeling, and robust reporting and risk mitigation through manual and programatic algorithm controls.

### Algorithm
Like Zipline, the inspriation for this system, AlgoCoin exposes a single algorithm class which is utilized for both live trading and backtesting. The algorithm class is simple enough to write and test algorithms quickly, but extensible enough to allow for complex slippage and transaction cost modeling, as well as mid- and post- trade analysis.  

### Markets
Eventual coverage:

- Bitstamp
- Bitfinex
- CEX
- GDAX 
- Gemini 
- HitBTC
- ItBit
- Kraken
- LakeBTC
- Poloniex

#### Market Data (Websocket)
[![GDAX](https://img.shields.io/badge/GDAX-ERR-brightred.svg)](https://img.shields.io/badge/GDAX-ERR-brightred.svg)
[![GEMINI](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)
[![ITBIT](https://img.shields.io/badge/ItBit-ERR-brightred.svg)](https://img.shields.io/badge/ItBit-ERR-brightred.svg)
[![KRAKEN](https://img.shields.io/badge/Kraken-ERR-brightred.svg)](https://img.shields.io/badge/Kraken-ERR-brightred.svg)
[![POLONIEX](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)

#### Order Entry (REST)
[![GDAX](https://img.shields.io/badge/GDAX-ERR-brightred.svg)](https://img.shields.io/badge/GDAX-ERR-brightred.svg)
[![GEMINI](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)
[![ITBIT](https://img.shields.io/badge/ItBit-ERR-brightred.svg)](https://img.shields.io/badge/ItBit-ERR-brightred.svg)
[![KRAKEN](https://img.shields.io/badge/Kraken-ERR-brightred.svg)](https://img.shields.io/badge/Kraken-ERR-brightred.svg)
[![POLONIEX](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)

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

### API Keys
You should creat API keys for exchanges you wish to trade on. For this example, we will assume a GDAX sandbox account with trading enabled. I usually put my keys in a set of shell scripts that are gitignored, so I don't post anything by accident. My scripts look something like:

```bash
export GEMINI_API_KEY=...
export GEMINI_API_SECRET=...
export GEMINI_API_PASS=...
```

Prior to running, I then source the keys I need. 

Let's make sure everything worked out by running a sample strategy on the GDAX sandbox exchange:

```bash
python3 -m algocoin --sandbox
```

### Writing an algorithm

### Backtesting

#### Getting Data

### Sandboxes

### Live Trading

---

## Contributing

---
