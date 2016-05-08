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

class Signals
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

    def golden()
        if @rev
            return @long.mean > @short.mean
        end
        
        return @short.mean > @long.mean
    end

    def death()
        if @rev
            return @short.mean > @long.mean
        end

        return @long.mean > @short.mean
    end 

end

# signals
all_signals = Array.new
all_signals << Signals.new(1, 5, true)                         #1
all_signals << Signals.new(5, 15, true)                      #2
all_signals << Signals.new(5, 30, true)                      #3
all_signals << Signals.new(5, 50, true)                      #4
all_signals << Signals.new(5, 100, true)                    #5
all_signals << Signals.new(15, 30, true)                    #6
all_signals << Signals.new(15, 50, true)                    #7
all_signals << Signals.new(15, 100, true)                  #8  
all_signals << Signals.new(15, 200, true)                  #9
all_signals << Signals.new(30, 50, true)                    #10
all_signals << Signals.new(30, 100, true)                  #11
all_signals << Signals.new(30, 200, true)                  #12
all_signals << Signals.new(30, 500, true)                  #13
all_signals << Signals.new(50, 100, true)                  #14
all_signals << Signals.new(50, 200, true)                  #15
all_signals << Signals.new(50, 500, true)                  #16
all_signals << Signals.new(100, 200, true)                #17
all_signals << Signals.new(100, 500, false)              #18
all_signals << Signals.new(100, 1000, false)            #19
all_signals << Signals.new(200, 500, false)              #20
all_signals << Signals.new(200, 1000, false)            #21
all_signals << Signals.new(500, 1000, false)            #22

goldens = Array.new
deaths = Array.new
buys = Array.new
sells = Array.new

for item in all_signals
    goldens << false
    deaths << false
    buys << false
    sells << false
end

buy_prices = Array.new
sell_prices = Array.new
profits = Array.new
for item in all_signals
    buy_prices << 0.0
    sell_prices << 0.0
    profits << 0.0
end

# new websocket
websocket = Coinbase::Exchange::Websocket.new(product_id: 'BTC-USD',
                                              keepalive: true)
# account data
api_key = ENV["COINBASE_API_KEY"]
api_secret = ENV["COINBASE_API_SECRET"]
api_pass = ENV["COINBASE_API_PASS"]

accounts = Array.new

# for transactions
rest_api = Coinbase::Exchange::Client.new(api_key, api_secret, api_pass)
sandbox = Coinbase::Exchange::Client.new(api_key, api_secret, api_pass,
                                          api_url: "https://api-public.sandbox.exchange.coinbase.com")

rest_api.accounts do |resp|
  resp.each do |account|
    p "#{account.id}: %.2f #{account.currency} available for trading" % account.available
    accounts << account
  end
end

# logic
websocket.match do |resp|
  for item in all_signals
    item.tick( resp.price )
    # print "current price : %.2f\n" % resp.price
  end

  all_signals.each_with_index do |item, i|
    if item.ready()
        if item.golden() # golden BUY
            if deaths[i]
                buys[i] = true
                sells[i] = false
                buy_prices[i] = resp.price
                # print "Buying strat %d at %.2f\n" % [i, resp.price]
            else
                buys[i] = false
                sells[i] = false
            end

            # period
            goldens[i] = true
            deaths[i] = false

        elsif item.death() # death SELL
            if goldens[i] and buy_prices[i] > 0.0
                profits[i] = profits[i] + resp.price - buy_prices[i]
                val = resp.price - buy_prices[i]
                print "Transaction%d: $ %.2f\n" % [i, val] 
                print "Profits%d: $ %.2f\n" % [i, profits[i]]
                buy_prices[i] = 0.0
                buys[i] = false
                sells[i] = true
            else
                buys[i] = false
                sells[i] = false
            end

            # period
            goldens[i] = false
            deaths[i] = true

        else # do nothing
            goldens[i] = false
            deaths[i] = false
        end

      end # item.golden()
    end # item.ready()
end # websocket.match


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
