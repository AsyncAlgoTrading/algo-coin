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
