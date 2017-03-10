import json
import time
import requests
try:
    #python3 compatibility
    import urllib.parse as urlparse
except ImportError:
    import urllib as urlparse
import base64
import hashlib
import hmac


#location of the api (change to https://beta-api.itbit.com/v1 for beta endpoint)
api_address = 'https://api.itbit.com/v1'

class MessageSigner(object):

    def make_message(self, verb, url, body, nonce, timestamp):
        # There should be no spaces after separators
        return json.dumps([verb, url, body, str(nonce), str(timestamp)], separators=(',', ':'))

    def sign_message(self, secret, verb, url, body, nonce, timestamp):
        message = self.make_message(verb, url, body, nonce, timestamp)
        sha256_hash = hashlib.sha256()
        nonced_message = str(nonce) + message
        sha256_hash.update(nonced_message.encode('utf8'))
        hash_digest = sha256_hash.digest()
        hmac_digest = hmac.new(secret, url.encode('utf8') + hash_digest, hashlib.sha512).digest()
        return base64.b64encode(hmac_digest)


class itBitApiConnection(object):

    #clientKey, secret, and userId are provided by itBit and are specific to your user account
    def __init__(self, clientKey, secret, userId):
        self.clientKey = clientKey
        self.secret = secret.encode('utf-8')
        self.userId = userId
        self.nonce = 0

    #returns ticker information for a specific ticker symbol
    def get_ticker(self, tickerSymbol):
        path = "/markets/%s/ticker" % (tickerSymbol)
        response = self.make_request("GET", path, {})
        return response

    #returns order book information for a specific ticker symbol
    def get_order_book(self, tickerSymbol):
        path = "/markets/%s/order_book" % (tickerSymbol)
        response = self.make_request("GET", path, {})
        return response

    #returns a list of all wallets for the userid provided
    def get_all_wallets(self, filters={}):
        filters['userId'] = self.userId
        queryString = self._generate_query_string(filters)
        path = "/wallets%s" % (queryString)
        response = self.make_request("GET", path, {})
        return response

    #creates a new wallet
    def create_wallet(self, walletName):
        path = "/wallets"
        response = self.make_request("POST", path, {'userId': self.userId, 'name': walletName})
        return response

    #returns a specific wallet by wallet id
    def get_wallet(self, walletId):
        path = "/wallets/%s" % (walletId)
        response = self.make_request("GET", path, {})
        return response

    #returns the balance of a specific currency within a wallet
    def get_wallet_balance(self, walletId, currency):
        path = "/wallets/%s/balances/%s" % (walletId, currency)
        response = self.make_request("GET", path, {})
        return response

    #returns a list of trades for a specific wallet
    #  results are paginated and limited to a maximum of 50 per request
    def get_wallet_trades(self, walletId, filters={}):
        queryString = self._generate_query_string(filters)
        path = "/wallets/%s/trades%s" % (walletId, queryString)
        response = self.make_request("GET", path, {})
        return response

    #returns a list of funding history for a wallet
    #  response will be paginated and limited to 50 items per response
    def get_funding_history(self, walletId, filters={}):
        queryString = self._generate_query_string(filters)
        path = "/wallets/%s/funding_history%s" % (walletId, queryString)
        response = self.make_request("GET", path, {})
        return response

    #returns a list of orders for a wallet
    #  response will be paginated and limited to 50 items per response
    #  orders can be filtered by status (ex: open, filled, etc)
    def get_wallet_orders(self, walletId, filters={}):
        queryString = self._generate_query_string(filters)
        path = "/wallets/%s/orders%s" % (walletId, queryString)
        response = self.make_request("GET", path, {})
        return response

    #creates a new limit order
    def create_order(self, walletId, side, currency, amount, price, instrument):
        path = "/wallets/%s/orders/" % (walletId)
        response = self.make_request("POST", path, {'type': 'limit', 'currency': currency, 'side': side, 'amount': amount, 'price': price, 'instrument': instrument})
        return response

    #creates a new limit order with a specific display amount (iceberg order)
    def create_order_with_display(self, walletId, side, currency, amount, price, display ,instrument):
        path = "/wallets/%s/orders/" % (walletId)
        response = self.make_request("POST", path, {'type': 'limit', 'currency': currency, 'side': side, 'amount': amount, 'price': price, 'display': display, 'instrument': instrument})
        return response 

    #returns a specific order by order id
    def get_order(self, walletId, orderId):
        path = "/wallets/%s/orders/%s" % (walletId, orderId)
        response = self.make_request("GET", path, {})
        return response

    #cancels an order by order id
    def cancel_order(self, walletId, orderId):
        path = "/wallets/%s/orders/%s" % (walletId, orderId)
        response = self.make_request("DELETE", path, {})
        return response

    #requests a withdrawal to a bitcoin address
    def cryptocurrency_withdrawal_request(self, walletId, currency, amount, address):
        path = "/wallets/%s/cryptocurrency_withdrawals" % (walletId)
        response = self.make_request("POST", path, {'currency': currency, 'amount': amount, 'address': address})
        return response

    #returns a new bitcoin address for deposits to a wallet
    def cryptocurrency_deposit_request(self, walletId, currency):
        path = "/wallets/%s/cryptocurrency_deposits" % (walletId)
        response = self.make_request("POST", path, {'currency': currency})
        return response

    #transfers funds of a single currency between two wallets
    def create_wallet_transfer(self, sourceWalletId, destinationWalletId, amount, currencyCode):
        path = "/wallet_transfers"
        response = self.make_request("POST", path, {'sourceWalletId': sourceWalletId, 'destinationWalletId': destinationWalletId, 'amount': amount, 'currencyCode': currencyCode})
        return response

    def make_request(self, verb, url, body_dict):
        url = api_address + url
        nonce = self._get_next_nonce()
        timestamp = self._get_timestamp()

        if verb in ("PUT", "POST"):
            json_body = json.dumps(body_dict)
        else:
            json_body = ""

        signer = MessageSigner()
        signature = signer.sign_message(self.secret, verb, url, json_body, nonce, timestamp)

        auth_headers = {
            'Authorization': self.clientKey + ':' + signature.decode('utf8'),
            'X-Auth-Timestamp': timestamp,
            'X-Auth-Nonce': nonce,
            'Content-Type': 'application/json'
        }

        return requests.request(verb, url, data=json_body, headers=auth_headers)

    #increases nonce so each request will have a unique nonce
    def _get_next_nonce(self):
        self.nonce += 1
        return self.nonce

    #timestamp must be unix time in milliseconds
    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _generate_query_string(self, filters):
        if filters:
            return '?' + urlparse.urlencode(filters)
        else:
            return ''
