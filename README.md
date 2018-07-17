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

- GDAX (Coinbase Pro)
- Gemini 
- Binance
- Bitfinex
- ItBit
- Kraken
- Poloniex
- Bitstamp
- CEX
- HitBTC
- LakeBTC


#### Sandboxes
[![GEMINI](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)
[![GDAX](https://img.shields.io/badge/GDAX-ERR-brightreg.svg)](https://img.shields.io/badge/GDAX-ERR-brightred.svg)

#### Market Data (Websocket)
[![GDAX](https://img.shields.io/badge/GDAX-OK-brightgreen.svg)](https://img.shields.io/badge/GDAX-OK-brightgreen.svg)
[![GEMINI](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)
[![BINANCE](https://img.shields.io/badge/Binance-ERR-brightred.svg)](https://img.shields.io/badge/Binance-ERR-brightred.svg)
[![ITBIT](https://img.shields.io/badge/ItBit-ERR-brightred.svg)](https://img.shields.io/badge/ItBit-ERR-brightred.svg)
[![KRAKEN](https://img.shields.io/badge/Kraken-ERR-brightred.svg)](https://img.shields.io/badge/Kraken-ERR-brightred.svg)
[![POLONIEX](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)

#### Order Entry (REST)
[![GDAX](https://img.shields.io/badge/GDAX-ERR-brightred.svg)](https://img.shields.io/badge/GDAX-ERR-brightred.svg)
[![GEMINI](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)
[![BINANCE](https://img.shields.io/badge/Binance-ERR-brightred.svg)](https://img.shields.io/badge/Binance-ERR-brightred.svg)
[![ITBIT](https://img.shields.io/badge/ItBit-ERR-brightred.svg)](https://img.shields.io/badge/ItBit-ERR-brightred.svg)
[![KRAKEN](https://img.shields.io/badge/Kraken-ERR-brightred.svg)](https://img.shields.io/badge/Kraken-ERR-brightred.svg)
[![POLONIEX](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)

#### Markets Coverage
| Exchange | Pairs |
| -------- | :---: |
| Gemini   | BTC-USD, ZEC-USD, ZEC-BTC, ZEC-ETH, ETH-BTC, ETH-USD |
| GDAX     | BTC-USD, BTC-ETH, BTC-LTC, BTC-BCH, ETH-USD, LTC-USD, BCH-USD, ETH-BTC, LTC-BTC, BCH-BTC |

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

### Writing a trading strategy
Trading strategies implement the `TradingStrategy` abstract class in `algocoin.lib.strategy`. This has a number of required methods for handling messages:

- onBuy
- onSell
- onTrade 
- onChange
- onDone
- onError
- onOpen
- onReceived

There are also a variety of optional methods for more granular control over risk/execution/backtesting, such as `slippage`, `transactionCost`, `onHalt`, `onContinue`, etc. 

### Backtesting
An instance of `TradingStrategy` class is able to run live or against a set of historical trade/quote data. When instantiating a `TradingEngine` object with a `TradingEngineConfig` object, the `TradingEngineConfig` has a `type` which can be set to `live`, `sandbox`, or `backtest`. Some additional methods are then usable on the `TradingStrategy`, including the `onAnalyze` method which allows you to visualize algorithm performance.


#### Getting Data
Historical data is relatively sparse, but the provided `fetchdata.sh` script will help grab historical data from bitcoincharts.com.

### Sandboxes
Currently only the Gemini sandbox is supported, the other exchanges have discontinued theirs. To run in sandbox, set `TradingEngineConfig.type` to Sandbox.

### Live Trading
When you want to run live, set `TradingEngineConfig.type` to Live. You will want to become familiar with the risk and execution engines, as these control things like max drawdown, max risk accrual, execution eagerness, etc.

---

## Contributing

---
