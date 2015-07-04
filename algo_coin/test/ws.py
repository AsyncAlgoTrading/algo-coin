
# import websocket
# import _thread
# import time


# websocket_feed_url = "wss://ws-feed.exchange.coinbase.com"


# def on_message(ws, message):
#     print(message)


# def on_error(ws, error):
#     print("error")


# def on_close(ws):
#     print("closed")


# def on_open(ws):
#     def run(*args):
#         time.sleep(1)
#         ws.send("GET /accounts")
#         time.sleep(1)
#         ws.close()
#         print("terminating thread")
#     _thread.start_new_thread(run, ())

# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp(websocket_feed_url,
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close)

#     ws.on_open = on_open
#     ws.run_forever()

# from cbe import *

# c = CoinbaseExchange()
# print(c.getProducts())

from websocket import create_connection

import json

ws = create_connection('wss://ws-feed.exchange.coinbase.com')
sub = json.dumps({"type": "subscribe", "product_id": "BTC-USD"})
ws.send(sub)
seq = -1

while True:
    result = json.loads(ws.recv())
    if seq < 0:
        seq = result['sequence']
    elif seq == (result['sequence'] - 1):
        seq += 1
    else:
        print("Sequence error")
        seq = -1

    # print(result)
    # print(result['sequence'])

ws.close()
