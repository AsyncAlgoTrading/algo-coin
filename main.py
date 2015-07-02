import sys

if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print('usage: python3 main.py <config-file> \
            <ex-keys-file> <wallet-keys-file>\n')
        sys.exit(1)

    config_file = sys.argv[1]
    ex_keys_file = sys.argv[2]
    wlt_keys_file = sys.argv[3]

    try:
        from algo_coin.algo_coin_backend import *
        from algo_coin.algo_coin_frontend import *
        from algo_coin.algo_coin_strategy import *
        from algo_coin.log import *
    except Exception:
        print("Import Error.")
        sys.exit(1)

    try:
        log = Log()
    except Exception:
        print("Error creating logfile.")
        sys.exit(1)

    acb = AlgoCoinBackend(log)
    acf = AlgoCoinFrontend(log)
    strat = AlgoCoinStrategy(log)

    # try:
    #     acb.setup(config_file, ex_keys_file, wlt_keys_file)
    # except Exception:
    #     print("Could not setup backend.")
    #     sys.exit(1)

    acb.setup(config_file, ex_keys_file, wlt_keys_file)
