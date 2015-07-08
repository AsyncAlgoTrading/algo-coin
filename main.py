import sys
from multiprocessing import Process


def deploy_db():
    DB = db.Dashboard(Log())
    DB.run()


def deploy_ce():
    CE = ce.ConnectivityEngine(Log())


def deploy_rr():
    RR = rr.ReceiverRouter(Log())


def deploy_se():
    SE = se.SendEngine(Log())


def deploy_ob():
    OB = ob.OrderBook(Log())


def deploy_bk():
    BK = bk.Bank(Log())


if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print('usage: python3 main.py <config-file> \
            <ex-keys-file> <wallet-keys-file>\n')
        sys.exit(1)

    # config files
    # specify which exchanges we are trading on
    # and where we the wallets are when moving
    # funds across exchanges
    config_file = sys.argv[1]

    # api keys
    # this is where the exchange api keys are
    ex_keys_file = sys.argv[2]

    # this is where the wallet api keys are
    wlt_keys_file = sys.argv[3]

    # make sure paths are all good by trying to import
    try:
        from algo_coin.dashboard import dashboard as db
        from algo_coin.connectivity import connectivity_engine as ce
        from algo_coin.recrouter import recrouter as rr
        from algo_coin.sendeng import sendengine as se
        from algo_coin.orderbook import orderbook as ob
        from algo_coin.wallet import bank as bk
        from algo_coin.util.log import *

    except Exception:
        print("Import Error.")
        sys.exit(1)

    # initialize and connect different processes TODO
    # 1. startup dashboard
    # 2. startup connectivity engine
    # 3. startup receiver router
    # 4. startup send engine
    # 5. build order book
    # 6. startup bank
    # 7. startup strategy manager
    p_db = Process(target=deploy_db)
    p_db.start()

    p_ce = Process(target=deploy_ce)
    p_rr = Process(target=deploy_ce)
    p_se = Process(target=deploy_ce)
    p_ob = Process(target=deploy_ce)
    p_bk = Process(target=deploy_ce)

    #TODO wait around and ping subprocesses for life.

    running = True
    triggered = None

    while(running):
        if not (p_db.is_alive()):
            running = False
            triggered = p_db

    #TODO Cleanup
    p_db.terminate()
    p_ce.terminate()
    p_rr.terminate()
    p_se.terminate()
    p_ob.terminate()
    p_bk.terminate()






    #connect to wallets and exchanges. this is the most important step
