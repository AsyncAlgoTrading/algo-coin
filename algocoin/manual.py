import sys
import select
import queue
from .lib.enums import Side, CurrencyType, OrderType, OrderSubType
from .lib.structs import TradeRequest
from .lib.logging import MANUAL as log


def manual(exchange, inqueue, outqueue):
    log.info('')
    log.critical('Entering manual mode')
    print(commands())
    while True:
        try:

            i, o, e = select.select([sys.stdin], [], [], 1)

            if (i):

                c = sys.stdin.readline().strip()
                x = c.split(' ')

                if x[0] == 'stats':
                    log.critical('stats: %s', exchange._last)
                elif x[0] == 'b':
                    try:
                        d = parse_buy(x, exchange._type)
                        outqueue.put(('b', d))
                        log.critical('manual buy!')
                        # exchange.buy(d)
                    except IndexError:
                        log.critical("Usage: b <volume> <price>"
                                     " <l,m : limit or market order>"
                                     " <p,f,a : post only,"
                                     " fill or kill, or all or nothing>")
                        continue
                elif x[0] == 's':
                    try:
                        d = parse_sell(x, exchange._type)
                        outqueue.put(('s', d))
                        log.critical('manual sell!')
                        # exchange.sell(d)
                    except IndexError:
                        log.critical("Usage: s <volume> <price>"
                                     " <l,m : limit or market order>"
                                     " <p,f,a : post only,"
                                     " fill or kill, or all or nothing>")
                        continue
                elif x[0] == 'q':
                    outqueue.put(('q'))
                elif x[0] == 'c':
                    outqueue.put(('c'))
                elif x[0] == 'h':
                    outqueue.put(('h'))
                elif x[0] == 'r':
                    outqueue.put(('r'))
            else:
                try:
                    x = inqueue.get(block=False)
                    if x:
                        log.critical('manual thread exiting')
                        return 0
                except queue.Empty:
                    continue
        except KeyboardInterrupt:
            outqueue.put(('q'))
        except:
            log.critical("Invalid command")
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
    return '''
    Stats: stats
        Print current trade price, bid/ask, etc

    Buy: b <volume> <price> <l,m : limit or market order> <p,f,a : post only, fill or kill, or all or nothing>
        Manually buy BTC

    Sell: s <volume> <price>  <l,m : limit or market order> <p,f,a : post only, fill or kill, or all or nothing>
        Manually sell BTC

    Quit: q
        Quit the application

    Continue: c
        Continue automated trading

    Halt: h
        Halt automated trading

    Return: r
        Exit manual mode
    '''
