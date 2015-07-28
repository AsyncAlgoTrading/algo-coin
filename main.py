import sys
import time
from multiprocessing import Process, Pool


if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print('usage: python3 main.py <config-file> \
            <ex-keys-file> <wallet-keys-file>\n')
        sys.exit(1)

    config_file = sys.argv[1]
    ex_keys_file = sys.argv[2]

    from algo_coin.util.log import *
    from algo_coin.connectivity.connection_manager import ConnectionManager
    from algo_coin.connectivity.connectivity_engine import ConnectivityEngine
    from algo_coin.recrouter.recrouter import ReceiverRouter

    processes = []
    conn_manager = ConnectionManager(config_file, ex_keys_file)
    conn_engine = ConnectivityEngine(conn_manager)
    # conn_engine.init_processes()
    # conn_engine.run_processes()
    # recrouter = ReceiverRouter(conn_engine)
    # time.sleep(15)
    # print("will it restart??")
    # if not conn_engine.monitor_processes():
    #     print("Connection down")
    #     conn_engine.restart_down()
    # time.sleep(10)
    # conn_engine.terminate()

    recrouter = ReceiverRouter(conn_engine)
    recrouter.run()
