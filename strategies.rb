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
    end

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

    def ready()
        return @long.length >= @long_size
    end

    def buy()
        if @rev
            return @long.mean > @short.mean
        end
        
        return @short.mean > @long.mean
    end

    def sell()
        if @rev
            return @short.mean > @long.mean
        end

        return @long.mean > @short.mean
    end 
end

class StrategyManager
    def initialize( bank )
        @bank = bank

        # signals
        @all_signals = Array.new
        @all_signals << CrossesStrat.new(1, 5, true)                  #1
        @all_signals << CrossesStrat.new(5, 15, true)                 #2
        @all_signals << CrossesStrat.new(5, 30, true)                 #3
        @all_signals << CrossesStrat.new(5, 50, true)                 #4
        @all_signals << CrossesStrat.new(5, 100, true)                #5
        @all_signals << CrossesStrat.new(15, 30, true)                #6
        @all_signals << CrossesStrat.new(15, 50, true)                #7
        @all_signals << CrossesStrat.new(15, 100, true)               #8  
        @all_signals << CrossesStrat.new(15, 200, true)               #9
        @all_signals << CrossesStrat.new(30, 50, true)                #10
        @all_signals << CrossesStrat.new(30, 100, true)               #11
        @all_signals << CrossesStrat.new(30, 200, true)               #12
        @all_signals << CrossesStrat.new(30, 500, true)               #13
        @all_signals << CrossesStrat.new(50, 100, true)               #14
        @all_signals << CrossesStrat.new(50, 200, true)               #15
        @all_signals << CrossesStrat.new(50, 500, true)               #16
        @all_signals << CrossesStrat.new(100, 200, true)              #17
        @all_signals << CrossesStrat.new(100, 500, true)             #18
        @all_signals << CrossesStrat.new(100, 1000, true)            #19
        @all_signals << CrossesStrat.new(200, 500, true)             #20
        @all_signals << CrossesStrat.new(200, 1000, true)            #21
        @all_signals << CrossesStrat.new(500, 1000, true)            #22
        
        @buy_state = Array.new # should be bought 
        @sell_state  = Array.new # should be sold
        @buy    = Array.new # bought/buy initiated
        @sell   = Array.new # sold/sell initiated

        @all_signals.each_with_index do |item, i|
            @bank.register_strategy( i )
        end

        for item in @all_signals
            @buy_state  << false
            @sell_state  << false
            @buy << false
            @sell << false
        end

        @buy_prices = Array.new
        @buy_qtys = Array.new
        @sell_prices = Array.new
        @sell_qtys = Array.new
        @profits = Array.new

        for item in @all_signals
            @buy_prices << 0.0
            @buy_qtys << 0.0
            @sell_prices << 0.0
            @sell_qtys << 0.0
            @profits << 0.0
        end
    end

    def tick( price )

        for item in @all_signals
            item.tick( price )
            # print "current price : %.2f\n" % resp.price
        end

        # buy when sell state transitions to buy state 
        # sell when buy state transitions to sell state
        @all_signals.each_with_index do |item, i|
            if item.ready()
                if item.buy() #  BUY
                    if @sell_state[i] # sell -> buy ?
                        amt = @bank.request_action( TransactionRequest.new( i, 'b', price ) ).amt
                        if amt > 0.0
                            @buy[i] = true
                            @sell[i] = false
                            @buy_prices[i] = price
                            @buy_qtys[i]    = price
                            # print "Buying %.2f @ %.2f\n" % [ amt, price ]
                        end
                    else
                        @buy[i] = false
                        @sell[i] = false
                    end

                    # period
                    @buy_state[i] = true
                    @sell_state[i] = false

                elsif item.sell() # SELL
                    if @buy_state[i] and @buy_prices[i] > 0.0
                        @profits[i] = @profits[i] + price - @buy_prices[i]
                        val = price - @buy_prices[i]
                        # print "Transaction%d: $ %.2f\n" % [i, val] 
                        @profits.each_with_index do |pft, i|
                            print "%d: $ %.2f\t" % [i, pft]
                        end
                        print "\n"
                        @buy_prices[i] = 0.0
                        @buy[i] = false
                        @sell[i] = true
                    else
                        @buy[i] = false
                        @sell[i] = false
                    end

                    # period
                    @buy_state[i] = false
                    @sell_state[i] = true

                else # do nothing
                    @buy_state[i] = false
                    @sell_state[i] = false
                end
            end 
        end
    end
end
