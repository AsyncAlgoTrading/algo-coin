import sys
import time
# from multiprocessing import Process, Pool


if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print('usage: python3 main.py <config-file> \
            <ex-keys-file> <wallet-keys-file>\n')
        sys.exit(1)

    config_file = sys.argv[1]
    ex_keys_file = sys.argv[2]

    from algo_coin.util.log import *
    from algo_coin.connectivity.connections import Connections
    from algo_coin.connectivity.connectivity_engine import ConnectivityEngine
    from algo_coin.connectivity.connection_monitor import ConnectionMonitor
    from algo_coin.recrouter.recrouter import ReceiverRouter

    processes = []
    conn_manager = Connections(config_file, ex_keys_file, Log())
    conn_engine = ConnectivityEngine(conn_manager, Log())
    conn_monitor = ConnectionMonitor(conn_engine, Log())
    recrouter = ReceiverRouter(conn_engine.queues, Log())

    try:
        #start recrouter
        recrouter.run()

        #start exchange processes
        conn_monitor.start_exchange_processes()

        #start connectivity monitor
        conn_monitor.run()
    except KeyboardInterrupt:
        print("Terminating all processes")
        recrouter.terminate()
        conn_monitor.terminate()
