# from coinbase.client import Client

# f = open(".keys","r")
# api_key = f.readline().split("=")[1].rstrip('\n')
# api_secret  = f.readline().split("=")[1].rstrip('\n')
# api_key2 = f.readline().split("=")[1].rstrip('\n')
# api_secret2  = f.readline().split("=")[1].rstrip('\n')
# f.close()


# client = Client(api_key, api_secret)
# #client2 = Client(api_key2, api_secret2)

# accounts = client.get_accounts()
# print(accounts)

import sys

if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print('usage: python3 main.py <config-file> \
            <ex-keys-file> <wallet-keys-file>\n')
        sys.exit(1)

    config_file = sys.argv[1]
    ex_keys_file = sys.argv[2]
    wlt_keys_file = sys.argv[3]

    from algo_coin.algo_coin import *
    ac = AlgoCoin()
    ac.main(config_file, ex_keys_file, wlt_keys_file)
