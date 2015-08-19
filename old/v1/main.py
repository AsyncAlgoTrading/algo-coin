import sys
import time
# from multiprocessing import Process
from algo_coin.connectivity.connectivity_engine import ConnectivityEngine


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

    config_file = sys.argv[1]
    ex_keys_file = sys.argv[2]
    wlt_keys_file = sys.argv[3]

    # make sure paths are all good by trying to import
    from algo_coin.util.log import *
    from algo_coin.util.processes import *

    thread_pool = []
    processes = []

    p_ce = ConnectivityEngine(Log())
    p_ce.setup(config_file, ex_keys_file, wlt_keys_file)
    p_ce.run()


    for process in processes:
        print(process)
        process.start()
        thread_pool.append(process)

    time.sleep(2)

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
