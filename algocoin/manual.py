from .lib.enums import Side, CurrencyType, OrderType, OrderSubType
from .lib.structs import TradeRequest
from .lib.logging import LOG as log


def manual(exchange):
    log.info('')
    log.critical('Entering manual mode')
    print(commands())
    while True:
        try:
            c = input('')
            x = c.split(' ')
            if x[0] == 'stats':
                print('Stats:')
                print(exchange._last)
                print('')
            elif x[0] == 'b':
                print('Buy')
                try:
                    d = parse_buy(x, exchange._type)
                    exchange.buy(d)
                except IndexError:
                    print('Usage: b <volume> <price>'
                          " <l,m : limit or market order>"
                          " <p,f,a : post only,"
                          " fill or kill, or all or nothing>")
                    continue
            elif x[0] == 's':
                print('Sell')
                try:
                    d = parse_sell(x, exchange._type)
                    exchange.sell(d)
                except IndexError:
                    print('Usage: s <volume> <price>'
                          " <l,m : limit or market order>"
                          " <p,f,a : post only,"
                          " fill or kill, or all or nothing>")
                    continue
            elif x[0] == 'q':
                return 0
            elif x[0] == 'c':
                return 1
            elif x[0] == 'h':
                return 2
        except:
            print("")
            print("Invalid command")
            print("")
            continue


def parse_buy(x, typ):
    vol = x[1]
    price = x[2]
    extra = x[3]
    extra2 = x[4] if len(x) == 5 else None

    ret = TradeRequest(side=Side.BUY,
                       volume=float(vol),
                       price=float(price),
                       exchange=typ,
                       currency=CurrencyType.BTC,
                       order_type=symbol_to_order_type(extra),
                       order_sub_type=symbol_to_order_sub_type(extra2))

    return ret


def parse_sell(x, typ):
    vol = x[1]
    price = x[2]
    extra = x[3]
    extra2 = x[4] if len(x) == 5 else None

    ret = TradeRequest(side=Side.SELL,
                       volume=float(vol),
                       price=float(price),
                       exchange=typ,
                       currency=CurrencyType.BTC,
                       order_type=symbol_to_order_type(extra),
                       order_sub_type=symbol_to_order_sub_type(extra2))
    return ret


def symbol_to_order_type(s):
    if s == 'l':
        return OrderType.LIMIT
    elif s == 'm':
        return OrderType.MARKET
    raise Exception('Order Type not recognized %s' % s)


def symbol_to_order_sub_type(s):
    if s == 'p':
        return OrderSubType.POST_ONLY
    elif s == 'f':
        return OrderSubType.FILL_OR_KILL
    elif s == 'a':
        return OrderSubType.ALL_OR_NOTHING
    else:
        return OrderSubType.NONE


def commands():
    print("")
    print("")
    print("")
    print("    Stats: stats")
    print("        Print current trade price, bid/ask, etc")
    print("")
    print("    Buy: b <volume> <price>"
          "<l,m : limit or market order>"
          "<p,f,a : post only,"
          "fill or kill, or all or nothing>")
    print("        Manually buy BTC")
    print("")
    print("    Sell: s <volume> <price>"
          "<l,m : limit or market order>"
          "<p,f,a : post only,"
          "fill or kill, or all or nothing>")
    print("        Manually sell BTC")
    print("")
    print("    Quit: q")
    print("        Quit the application")
    print("")
    print("    Continue: c")
    print("        Continue automated trading")
    print("")
    print("    Halt: h")
    print("        Halt automated trading")
    print("")


def Manual(pipe, exchange):
    while True:
        try:
            if pipe.recv():
                pipe.send(manual(exchange))
        except:
            continue
