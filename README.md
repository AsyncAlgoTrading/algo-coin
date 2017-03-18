#AlgoCoin
Algorithmic Trading Bitcoin. 

[![Version](https://img.shields.io/badge/version-0.0.13-lightgrey.svg)](https://img.shields.io/badge/version-0.0.13-lightgrey.svg)
[![Build Status](https://travis-ci.com/theocean154/algo-coin.svg?token=y6bAWygGk2pr7D7jBosB&branch=master)](https://travis-ci.com/theocean154/algo-coin)
[![Coverage](https://codecov.io/gh/theocean154/algo-coin/coverage.svg?branch=master&token=JGqz8ChQxd)](https://codecov.io/gh/theocean154/algo-coin)

##Overview 
Lightweight, extensible program for algorithmically trading cryptocurrencies across multiple exchanges. 

###System Architecture
AlgoCoin is an event based trading system written in python. It comes with support for live trading across (and between) multiple exchanges, fully integrated backtesting support, slippage and transaction cost modeling, and robust reporting and risk mitigation through manual and programatic algorithm controls.

###Algorithm
Like Zipline, the inspriation for this system, AlgoCoin exposes a single algorithm class which is utilized for both live trading and backtesting. The algorithm class is simple enough to write and test algorithms quickly, but extensible enough to allow for complex slippage and transaction cost modeling, as well as mid- and post- trade analysis.  

###Markets
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

####Market Data (Websocket)
[![GDAX](https://img.shields.io/badge/GDAX-OK-brightgreen.svg)](https://img.shields.io/badge/GDAX-OK-brightgreen.svg)
[![GEMINI](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)
[![ITBIT](https://img.shields.io/badge/ItBit-ERR-brightred.svg)](https://img.shields.io/badge/ItBit-ERR-brightred.svg)
[![KRAKEN](https://img.shields.io/badge/Kraken-ERR-brightred.svg)](https://img.shields.io/badge/Kraken-ERR-brightred.svg)
[![POLONIEX](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)

####Order Entry (REST)
[![GDAX](https://img.shields.io/badge/GDAX-OK-brightgreen.svg)](https://img.shields.io/badge/GDAX-OK-brightgreen.svg)
[![GEMINI](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)](https://img.shields.io/badge/Gemini-OK-brightgreen.svg)
[![ITBIT](https://img.shields.io/badge/ItBit-ERR-brightred.svg)](https://img.shields.io/badge/ItBit-ERR-brightred.svg)
[![KRAKEN](https://img.shields.io/badge/Kraken-ERR-brightred.svg)](https://img.shields.io/badge/Kraken-ERR-brightred.svg)
[![POLONIEX](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)](https://img.shields.io/badge/Poloniex-ERR-brightred.svg)
