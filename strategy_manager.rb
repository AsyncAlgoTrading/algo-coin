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
        # @all_signals << CrossesStrat.new(200, 500, false)             #20
        # @all_signals << CrossesStrat.new(200, 1000, false)            #21
        # @all_signals << CrossesStrat.new(500, 1000, false)            #22
        
        @all_signals.each_with_index do |item, i|
            @bank.register_strategy( i )
        end
        @profits = Array.new

        for item in @all_signals
            @profits << 0.0
        end
    end

    def tick( price )

        actions = Array.new
        for item in @all_signals
            item.tick( price )
            actions << item.action()
        end

        # buy when sell state transitions to buy state 
        # sell when buy state transitions to sell state
        actions.each_with_index do |item, i|
            if item == 'b'
                amt = @bank.request_action( TransactionRequest.new( i, 'b', price ) ).amt
                if amt > 0.0000
                    @all_signals[i].bought( price )
                    @bank.register_action( Transaction.new( i, 'b', amt, price ) )
                    print "%d Buying %.2f @ %.2f\n" % [ i, amt, price ]
                end

            elsif item == 's'
                amt = @bank.request_action( TransactionRequest.new( i, 'b', price ) ).amt
                if amt > 0.0
                    @all_signals[i].sold( price )
                    @bank.register_action( Transaction.new( i, 's', amt, price ) )
                    
                    @profits[i] = @profits[i] + price - @all_signals[i].buy_price
                    val = price - @all_signals[i].buy_price
                    print "%d Transaction: $ %.2f\n" % [i, val] 
                    print "%d Profits: $ %.2f\n" % [i, @profits[i]]
                end

            elsif item == 'n'
                # p 'n'
            end
        end
    end
end
