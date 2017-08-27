import sys
import requests
import warnings


class Price:
	def __init__(self):
		self.__coinlisturl = 'https://www.cryptocompare.com/api/data/coinlist/'
		self.__priceurl = 'https://min-api.cryptocompare.com/data/price?'
		self.__pricemultiurl = 'https://min-api.cryptocompare.com/data/pricemulti?'
		self.__pricemultifullurl = 'https://min-api.cryptocompare.com/data/pricemultifull?'
		self.__generateavgurl = 'https://min-api.cryptocompare.com/data/generateAvg?'
		self.__dayavgurl = 'https://min-api.cryptocompare.com/data/dayAvg?'
		self.__historicalurl = 'https://min-api.cryptocompare.com/data/pricehistorical?'
		self.__coinsnapshoturl = 'https://www.cryptocompare.com/api/data/coinsnapshot/?'
		self.__coinsnapshotfull = 'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?'

	def coinList(self):
		return self.__get_url(self.__coinlisturl)

	def price(self, from_curr, to_curr, e=None, extraParams=None, sign=False, tryConversion=True):
		return self.__get_price(self.__priceurl, from_curr, to_curr, e, extraParams, sign, tryConversion)

	def priceMulti(self, from_curr, to_curr, e=None, extraParams=None, sign=False, tryConversion=True):
		return self.__get_price(self.__pricemultiurl, from_curr, to_curr, e, extraParams, sign, tryConversion)

	def priceMultiFull(self, from_curr, to_curr, e=None, extraParams=None, sign=False, tryConversion=True):
		return self.__get_price(self.__pricemultifullurl, from_curr, to_curr, e, extraParams, sign, tryConversion)

	def priceHistorical(self, from_curr, to_curr, markets, ts=None, e=None, extraParams=None,
						sign=False, tryConversion=True):
		return self.__get_price(self.__historicalurl, from_curr, to_curr, markets, e, extraParams, sign, tryConversion)

	def generateAvg(self, from_curr, to_curr, markets, extraParams=None, sign=False, tryConversion=True):
		return self.__get_avg(self.__generateavgurl, from_curr, to_curr, markets, extraParams, sign, tryConversion)

	def dayAvg(self, from_curr, to_curr, e=None, extraParams=None, sign=False, tryConversion=True,
			   avgType=None, UTCHourDiff=0, toTs=None):
		return self.__get_avg(self.__dayavgurl, from_curr, to_curr, e, extraParams, sign,
							tryConversion, avgType, UTCHourDiff, toTs)

	def coinSnapshot(self, from_curr, to_curr):
		return self.__get_url(self.__coinsnapshoturl + 'fsym=' + from_curr.upper() + '&tsym=' + to_curr.upper())

	def coinSnapshotFullById(self, coin_id):
		return self.__get_url(self.__coinsnapshotfull + 'id=' + str(coin_id))

	def __get_price(self, baseurl, from_curr, to_curr, e=None, extraParams=None, sign=False,
				  tryConversion=True, markets=None, ts=None):
		args = list()
		if isinstance(from_curr, str):
			args.append('fsym=' + from_curr.upper())
		elif isinstance(from_curr, list):
			args.append('fsyms=' + ','.join(from_curr).upper())
		if isinstance(to_curr, list):
			args.append('tsyms=' + ','.join(to_curr).upper())
		elif isinstance(to_curr, str):
			args.append('tsyms=' + to_curr.upper())
		if isinstance(markets, str):
			args.append('markets=' + markets)
		elif isinstance(markets, list):
			args.append('markets=' + ','.join(markets))
		if e:
			args.append('e=' + e)
		if extraParams:
			args.append('extraParams=' + extraParams)
		if sign:
			args.append('sign=true')
		if ts:
			args.append('ts=' + str(ts))
		if not tryConversion:
			args.append('tryConversion=false')
		if len(args) >= 2:
			return self.__get_url(baseurl + '&'.join(args))
		else:
			raise ValueError('Must have both fsym and tsym arguments.')

	def __get_avg(self, baseurl, from_curr, to_curr, markets=None, e=None, extraParams=None,
				sign=False, tryConversion=True, avgType=None, UTCHourDiff=0, toTs=None):
		args = list()
		if isinstance(from_curr, str):
			args.append('fsym=' + from_curr.upper())
		if isinstance(to_curr, str):
			args.append('tsym=' + to_curr.upper())
		if isinstance(markets, str):
			args.append('markets=' + markets)
		elif isinstance(markets, list):
			args.append('markets=' + ','.join(markets))
		if e:
			args.append('e=' + e)
		if extraParams:
			args.append('extraParams=' + extraParams)
		if sign:
			args.append('sign=true')
		if avgType:
			args.append('avgType=' + avgType)
		if UTCHourDiff:
			args.append('UTCHourDiff=' + str(UTCHourDiff))
		if toTs:
			args.append('toTs=' + toTs)
		if not tryConversion:
			args.append('tryConversion=false')
		if len(args) >= 2:
			return self.__get_url(baseurl + '&'.join(args))
		else:
			raise ValueError('Must have both fsym and tsym arguments.')

	def __get_url(self, url):
		raw_data = requests.get(url)
		raw_data.encoding = 'utf-8'
		if raw_data.status_code != 200:
			raw_data.raise_for_status()
			return False
		try:
			if isinstance(raw_data.text, unicode):
				warnings.warn('Object returned is of type unicode. Cannot parse to str in Python 2.')
		except NameError:
			pass
		return raw_data.json()


class History:
	def __init__(self):
		self.__histominuteurl = 'https://min-api.cryptocompare.com/data/histominute?'
		self.__histohoururl = 'https://min-api.cryptocompare.com/data/histohour?'
		self.__histodayurl = 'https://min-api.cryptocompare.com/data/histoday?'

	def histoMinute(self, from_curr, to_curr, e=None, extraParams=None,
					sign=False, tryConversion=True, aggregate=None, limit=None, toTs=None):
		return self.__get_price(self.__histominuteurl, from_curr, to_curr, e, extraParams, sign,
								tryConversion, aggregate, limit, toTs)

	def histoHour(self, from_curr, to_curr, e=None, extraParams=None,
				  sign=False, tryConversion=True, aggregate=None, limit=None, toTs=None):
		return self.__get_price(self.__histohoururl, from_curr, to_curr, e, extraParams, sign,
								tryConversion, aggregate, limit, toTs)

	def histoDay(self, from_curr, to_curr, e=None, extraParams=None, sign=False,
				 tryConversion=True, aggregate=None, limit=None, toTs=None, allData=False):
		return self.__get_price(self.__histodayurl, from_curr, to_curr, e, extraParams, sign,
								tryConversion, aggregate, limit, toTs, allData)

	def __get_price(self, baseurl, from_curr, to_curr, e=None, extraParams=None, sign=False,
					tryConversion=True, aggregate=None, limit=None, toTs=None, allData=False):
		args = list()
		if isinstance(from_curr, str):
			args.append('fsym=' + from_curr.upper())
		if isinstance(to_curr, str):
			args.append('tsym=' + to_curr.upper())
		if e:
			args.append('e=' + e)
		if extraParams:
			args.append('extraParams=' + extraParams)
		if sign:
			args.append('sign=true')
		if aggregate:
			args.append('aggregate=' + str(aggregate))
		if limit:
			args.append('limit=' + str(limit))
		if toTs:
			args.append('toTs=' + str(toTs))
		if allData:
			args.append('allData=true')
		if not tryConversion:
			args.append('tryConversion=false')
		if len(args) >= 2:
			return self.__get_url(baseurl + '&'.join(args))
		else:
			raise ValueError('Must have both fsym and tsym arguments.')

	def __get_url(self, url):
		raw_data = requests.get(url)
		raw_data.encoding = 'utf-8'
		if raw_data.status_code != 200:
			raw_data.raise_for_status()
			return False
		try:
			if isinstance(raw_data.text, unicode):
				warnings.warn('Object returned is of type unicode. Cannot parse to str in Python 2.')
		except NameError:
			pass
		return raw_data.json()
