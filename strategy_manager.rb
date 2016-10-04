require_relative 'utils'
require_relative 'bank'
require_relative 'strategies'

class StrategyManager
    def initialize( bank )
        @bank = bank

        @all_signals = Array.new

        f = File.new( 'config.cfg' )
        f.each_line do |l|
            row = l.strip.split( ', ' )
            clazz = Object.const_get( row[ 1 ].strip )
            p "Registering Strategy %s" % l.strip
            @all_signals <<  clazz.new( *row[ 2..-1 ] )
        end
        
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
