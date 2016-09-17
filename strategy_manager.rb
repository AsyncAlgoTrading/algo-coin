require_relative 'utils'
require_relative 'bank'
require_relative 'strategies'

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
        @all_signals << CrossesStrat.new(100, 500, false)             #18
        @all_signals << CrossesStrat.new(100, 1000, false)            #19
        @all_signals << CrossesStrat.new(200, 500, false)             #20
        @all_signals << CrossesStrat.new(200, 1000, false)            #21
        @all_signals << CrossesStrat.new(500, 1000, false)            #22
        
        @all_signals.each_with_index do |item, i|
            @bank.register_strategy( i )
        end

        @profits = Array.new

        for item in @all_signals
            @profits << 0.0
        end
    end

    def tick( price )

        for item in @all_signals
            actions = Array.new
            item.tick( price )
            actions << item.action( price )
        end

        # buy when sell state transitions to buy state 
        # sell when buy state transitions to sell state
        actions.each_with_index do |item, i|
            if item == 'b'
                amt = @bank.request_action( TransactionRequest.new( i, 'b', price ) ).amt
                if amt > 0.0
                    @all_signals[i].bought( price )
                    print "Buying %.2f @ %.2f\n" % [ amt, price ]
                    @bank.register_action( Transaction.new( i, amt, price ) )
                end
            elsif item == 's'
                @all_signals[i].sold( price )
                @profits[i] = @profits[i] + price - @all_signals[i].buy_price
                val = price - @all_signals[i].buy_price
                print "Transaction%d: $ %.2f\n" % [i, val] 
                print "Profits%d: $ %.2f\n" % [i, @profits[i]]
            elsif item == 'n'
            end
        end
    end
    #     # buy when sell state transitions to buy state 
    #     # sell when buy state transitions to sell state
    #     @all_signals.each_with_index do |item, i|
    #         if item.ready()
    #             if item.buy() #  BUY
    #                 if @sell_state[i] # sell -> buy ?
    #                     amt = @bank.request_action( TransactionRequest.new( i, 'b', price ) ).amt
    #                     if amt > 0.0
    #                         @buy[i] = true
    #                         @sell[i] = false
    #                         @buy_prices[i] = price
    #                         @buy_qtys[i]    = price
    #                         print "Buying %.2f @ %.2f\n" % [ amt, price ]

    #                         @bank.register_action( Transaction.new( i, amt, price ) )
    #                     # print "Buying strat %d at %.2f\n" % [i, resp.price]
    #                     end
    #                 else
    #                     @buy[i] = false
    #                     @sell[i] = false
    #                 end

    #                 # period
    #                 @buy_state[i] = true
    #                 @sell_state[i] = false

    #             elsif item.sell() # SELL
    #                 if @buy_state[i] and @buy_prices[i] > 0.0
    #                     @profits[i] = @profits[i] + price - @buy_prices[i]
    #                     val = price - @buy_prices[i]
    #                     print "Transaction%d: $ %.2f\n" % [i, val] 
    #                     print "Profits%d: $ %.2f\n" % [i, @profits[i]]
    #                     @buy_prices[i] = 0.0
    #                     @buy[i] = false
    #                     @sell[i] = true
    #                 else
    #                     @buy[i] = false
    #                     @sell[i] = false
    #                 end

    #                 # period
    #                 @buy_state[i] = false
    #                 @sell_state[i] = true

    #             else # do nothing
    #                 @buy_state[i] = false
    #                 @sell_state[i] = false
    #             end
    #         end 
    #     end
    # end
end
