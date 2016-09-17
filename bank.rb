require 'coinbase/exchange'
require_relative 'utils'
require_relative 'accounts'

# Request an action at a certain price
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

# Amount allowed
class TransactionResponse
    def initialize( amt )
        @amt = amt
    end
    attr_reader :amt
end

# Execute an action for a certain amount at a certain price
class Transaction
    def initialize( id, side, amt, price )
        @id = id
        @side = side 
        @amt = amt
        @price = price
    end
    attr_reader :id
    attr_reader :side
    attr_reader :amt
    attr_reader :price
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
            return TransactionResponse.new( val )
        else
            val = @strats[ tx_req.id ].allowance / tx_req.price
            return TransactionResponse.new( val )
        end
    end

    def register_action( tx )
        if tx.side == 'b'
            @strats[ tx.id ].allowance -= tx.amt*tx.price
            return TransactionResponse.new( @strats[ tx.id ].allowance )
        else
            @strats[ tx.id ].allowance += tx.amt*tx.price
            return TransactionResponse.new( @strats[ tx.id ].allowance )
        end
    end
end

