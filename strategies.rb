require_relative 'utils'
require_relative 'bank'

class CrossesStrat
    def initialize( short_size, long_size, rev )
        @short = Array.new
        @momentum_short  = Array.new
        @short_size = short_size
        
        @long = Array.new
        @momentum_long   = Array.new
        @long_size  = long_size
        
        @rev = rev

        @sell_state = false
        @buy_state = false
        @sell_price = 0.0
        @buy_price = 0.0

        @profit = 0.0
    end
    attr_reader :sell_price
    attr_reader :buy_price


    def tick( value )
        @short << value
        @long  << value
        @momentum_short << @short.mean
        @momentum_long  << @long.mean

        if @short.length > @short_size
            @short.shift
            @momentum_short.shift
        end

        if @long.length > @long_size
            @long.shift
            @momentum_long.shift
        end

    end

    def ready
        return @long.length >= @long_size
    end

    def buy
        if @rev
            return @long.mean > @short.mean
        end
        
        return @short.mean > @long.mean
    end

    def sell
        if @rev
            return @short.mean > @long.mean
        end

        return @long.mean > @short.mean
    end 

    def action
        if ready
            if buy #  BUY
                @buy_state = true
                if @sell_state # sell -> buy ?
                    @sell_state = false
                    return 'b'
                else
                    @sell_state = false
                    return 'n'
                end

            elsif sell # SELL
                @sell_state = true
                if @buy_state and @buy_price > 0.0
                    @buy_state = false
                    return 's'
                else
                    @buy_state = false
                    return 'n'
                end

            else # do nothing
                @buy_state = false
                @sell_state = false
            end # if buy/elsif sell
        else
            return 'n'
        end # ready

    end   

    def bought( px )
        @buy_price = px
    end 

    def sold( px )
        @sell_price = px
    end
end

