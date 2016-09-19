require 'coinbase/exchange'
require_relative 'utils'

class Accounts
    def initialize( env )
        @usd = 0.0
        @eth = 0.0
        @btc = 0.0

        @accounts = Hash.new

        # for transactions
        @rest_api = Coinbase::Exchange::Client.new(env.api_key, env.api_secret, env.api_pass)
        @sandbox = Coinbase::Exchange::Client.new(env.api_key, env.api_secret, env.api_pass, api_url: "https://api-public.sandbox.exchange.coinbase.com")
        @rest_api_async = Coinbase::Exchange::AsyncClient.new(env.api_key, env.api_secret, env.api_pass)

        @rest_api.accounts do |resp|
            resp.each do |account|
                p "#{account.id}: %.2f #{account.currency} available for trading" % account.available
                if account.currency == 'USD'
                    @accounts[ 'USD' ] = account
                    @usd = account.available
                elsif account.currency == 'ETH'
                    @accounts[ 'ETH' ] = account
                    @eth = account.available
                elsif account.currency == 'BTC'
                    @accounts[ 'BTC' ] = account
                    @btc = account.available
                end
            end
        end
    end

    attr_reader :usd
    attr_reader :btc
end

