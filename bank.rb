require 'coinbase/exchange'
require_relative 'utils'

class TransactionRequest
    def initialize( id, side, price )
        @id = id
        @side = side
        @price = price
    end
    attr_reader :id
    attr_reader :side
    attr_reader :price
end

class TransactionResponse
    def initialize( amt )
        @amt = amt
    end
    attr_reader :amt
end

class Accounts
    def initialize( env )
        @usd = 0.0
        @eth = 0.0
        @btc = 0.0
        @ltc = 0.0

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
                elsif account.currency == 'BTC'
                    @accounts[ 'LTC' ] = account
                    @ltc = account.available
                end
            end
        end
    end

    attr_reader :usd
    attr_reader :btc
    attr_reader :eth
    attr_reader :ltc
end

class Balance
    def initialize( allowance )
        @allowance = allowance
        @balance = 0.0
    end
    attr_reader :allowance
    attr_reader :balance
end

class Bank
    def initialize()
        @strats = Hash.new
        @accounts = Accounts.new( Env.new() )
    end
    
    def register_strategy( id )
        @strats[ id ] = Balance.new( @accounts.usd )
    end
    
    def request_action( tx_req )
        if tx_req.side == 'b'
            # val = ( @strats[ tx_req.id ].allowance - @strats[ tx_req.id ].balance ) / tx_req.price
            val = @strats[ tx_req.id ].allowance / tx_req.price
            ret = TransactionResponse.new( val )
        else
            val = @strats[ tx_req.id ].allowance / tx_req.price
            ret = TransactionResponse.new( val )
        end
    end
end

