require 'coinbase/exchange'
require_relative 'utils'
require_relative 'accounts'
require_relative 'transaction'

class Balance
    def initialize( allowance )
        @allowance = allowance
        @balance = 0.0
    end
    attr_reader :allowance
    attr_writer :allowance
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
            return TransactionResponse.new( val )
        else
            val = @strats[ tx_req.id ].allowance / tx_req.price
            return TransactionResponse.new( val )
        end
    end

    def register_action( tx )
        if tx.side == 'b'
            @strats[ tx.id ].allowance -= tx.amt * tx.price
            return TransactionResponse.new( @strats[ tx.id ].allowance )
        else
            @strats[ tx.id ].allowance += tx.amt * tx.price
            return TransactionResponse.new( @strats[ tx.id ].allowance )
        end
    end
end

