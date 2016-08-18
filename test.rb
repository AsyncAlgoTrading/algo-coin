require 'coinbase/exchange'
require 'eventmachine'
require 'ostruct'

# make it easy
class Array
    def sum
        inject(0.0) { |result, el| result + el }
    end

    def mean 
        sum / size
    end
end

class Env
    def initialize()
        # account data
        @api_key = ENV["COINBASE_API_KEY"]
        @api_secret = ENV["COINBASE_API_SECRET"]
        @api_pass = ENV["COINBASE_API_PASS"]
    end
    attr_reader :api_key
    attr_reader :api_secret
    attr_reader :api_pass
end

class Accounts
    def initialize( env )
        @usd = 0.0
        @eth = 0.0
        @btc = 0.0

        @accounts = Hash.new

        # for transactions
        @rest_api = Coinbase::Exchange::Client.new(env.api_key, env.api_secret, env.api_pass)
        @sandbox = Coinbase::Exchange::Client.new(env.api_key, env.api_secret, env.api_pass,
                                                                                          api_url: "https://api-public.sandbox.exchange.coinbase.com")
        @rest_api_async = Coinbase::Exchange::AsyncClient.new(env.api_key, env.api_secret, env.api_pass)

        @rest_api.accounts do |resp|
        resp.each do |account|
            # p "#{account.id}: %.2f #{account.currency} available for trading" % account.available
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
end


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

class Strategy
    def initialize( )
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
        
        @buy_state = Array.new # should be bought 
        @sell_state  = Array.new # should be sold
        @buy    = Array.new # bought/buy initiated
        @sell   = Array.new # sold/sell initiated

        for item in @all_signals
            @buy_state  << false
            @sell_state  << false
            @buy << false
            @sell << false
        end

        @buy_prices = Array.new
        @sell_prices = Array.new
        @profits = Array.new

        for item in @all_signals
            @buy_prices << 0.0
            @sell_prices << 0.0
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
                        @buy[i] = true
                        @sell[i] = false
                        @buy_prices[i] = price
                        # print "Buying strat %d at %.2f\n" % [i, resp.price]
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
                        print "Transaction%d: $ %.2f\n" % [i, val] 
                        print "Profits%d: $ %.2f\n" % [i, @profits[i]]
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


strat = Strategy.new()
accts = Accounts.new( Env.new() )

# new websocket
websocket = Coinbase::Exchange::Websocket.new(product_id: 'BTC-USD',
    keepalive: true)
#rest api

# logic
#execution
websocket.match do |resp|
    strat.tick( resp.price )
end # websocket.match

# new order received
websocket.received do |resp|
    # p resp
end

#order opened
websocket.open do |resp|
    if resp.remaining_size > 10
        print "[NEW] \t %s \t\t %3.3f \t@ %.2f\n" % [resp.side, resp.remaining_size, resp.price]
    else
        print "[NEW] \t %s \t\t %3.3f \t\t@ %.2f\n" % [resp.side, resp.remaining_size, resp.price]
    end
    # p resp
end

#order off the books
websocket.done do |resp|
    # p resp
    if resp.reason == 'filled'
        if resp.key?('remaining_size') 
            print "[FIL] \t %s \t\t %3.3f \t\t@ %.2f\n" % [resp.side, resp.remaining_size, resp.price]
        else
            print "[FIL] \t %s \t\t \t\t\n" % [resp.side]
        end
    elsif resp.reason == 'canceled'
        print "[CAN] \t %s \t\t \t\t@ %.2f\n" % [resp.side, resp.price]
    end
            
end

#order changed
websocket.change do |resp|
    print "[MOD] \t %s \t\t %3.3f \t\t@ %.2f\n" % [resp.side, resp.remaining_size, resp.price]
    # p resp
end

# #heartbeat
# websocket.heartbeat do |resp|
#     p resp
# end

#error
websocket.error do |resp|
    p resp
end


# websocket stuff
EM.run do
  websocket.start!
  EM.add_periodic_timer(1) {
    websocket.ping do
      # p "Websocket is alive"
  end
}
  # EM.error_handler { |e|
  #   p "Websocket Error: #{e.message}"
  # }
end
