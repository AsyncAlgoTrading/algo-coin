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


if __name__ == "__main__":
    import algo_coin.algo_coin as ac
    ac.main()
