import sys
import time
from multiprocessing import Process


def deploy_db():
    DB = db.Dashboard(Log())
    DB.run()


def deploy_ce(config_file, ex_keys_file, wlt_keys_file):
    CE = ce.ConnectivityEngine(Log())
    CE.setup(config_file, ex_keys_file, wlt_keys_file)


def deploy_rr():
    RR = rr.ReceiverRouter(Log())


def deploy_se():
    SE = se.SendEngine(Log())


def deploy_ob():
    OB = ob.OrderBook(Log())


def deploy_bk():
    BK = bk.Bank(Log())


def cleanup(thread_pool):
    print("\nTaking all threads down now...")
    for thread in thread_pool:
        if thread.is_alive():
            thread.terminate()
        thread.join()


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
        print()
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
    thread_pool = []

    try:
        p_db_args = ()
        p_db = Process(target=deploy_db, args=p_db_args,
                       name="Thread-Dashboard")
        p_db.start()
        thread_pool.append(p_db)

    except Exception:
        print("Error deploying Dashboard, terminating all processes")
        cleanup(thread_pool)
        sys.exit(1)

    try:
        p_ce_args = (config_file, ex_keys_file, wlt_keys_file)
        p_ce = Process(target=deploy_ce, args=p_ce_args,
                       name="Thread-ConnectivityEngine")
        p_ce.start()
        thread_pool.append(p_ce)

    except Exception:
        print("Error deploying ConnectivityEngine, terminating all processes")
        cleanup(thread_pool)
        sys.exit(1)

    try:
        p_rr_args = ()
        p_rr = Process(target=deploy_rr, args=p_rr_args,
                       name="Thread-ReceiverRouter")
        p_rr.start()
        thread_pool.append(p_rr)

    except Exception:
        print("Error deploying ReceiverRouter, terminating all processes")
        cleanup(thread_pool)
        sys.exit(1)

    try:
        p_se_args = ()
        p_se = Process(target=deploy_se, args=p_se_args,
                       name="Thread-SendEngine")
        p_se.start()
        thread_pool.append(p_se)

    except Exception:
        print("Error deploying Send Engine, terminating all processes")
        sys.exit(1)

    try:
        p_ob_args = ()
        p_ob = Process(target=deploy_ob, args=p_ob_args,
                       name="Thread-Orderbook")
        p_ob.start()
        thread_pool.append(p_ob)

    except Exception:
        print("Error deploying OrderBook, terminating all processes")
        cleanup(thread_pool)
        sys.exit(1)

    try:
        p_bk_args = ()
        p_bk = Process(target=deploy_bk, args=p_bk_args,
                       name="Thread-Bank")
        p_bk.start()
        thread_pool.append(p_bk)

    except Exception:
        print("Error deploying Bank, terminating all processes")
        cleanup(thread_pool)
        sys.exit(1)

    for thread in thread_pool:
        if not thread.is_alive():
            print(thread.name + " is down")
            cleanup(thread_pool)
            sys.exit(1)
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            cleanup(thread_pool)
            sys.exit(1)
