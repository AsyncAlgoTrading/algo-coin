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
    def initialize( short_size, long_size )
        @short = Array.new
        @momentum_short  = Array.new
        @short_size = short_size
        @long = Array.new
        @momentum_long   = Array.new
        @long_size  = long_size
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
        return @long.length > @long_size
    end

    def golden()
        return @short.mean > @long.mean
    end

    def death()
        return @long.mean > @short.mean
    end 

end

# signals
signal1 = Signals.new(5, 15)
signal2 = Signals.new(5, 30)
signal3 = Signals.new(5, 50)
signal4 = Signals.new(5, 100)
signal5 = Signals.new(15, 30)
signal6 = Signals.new(15, 50)
signal7 = Signals.new(15, 100)
signal8 = Signals.new(15, 200)
signal9 = Signals.new(30, 50)
signal10 = Signals.new(30, 100)
signal11 = Signals.new(30, 200)
signal12 = Signals.new(30, 500)
signal13 = Signals.new(50, 100)
signal14 = Signals.new(50, 200)
signal15 = Signals.new(50, 500)
signal16 = Signals.new(100, 200)
signal17 = Signals.new(100, 500)
signal18 = Signals.new(100, 1000)
signal19 = Signals.new(200, 500)
signal20 = Signals.new(200, 1000)
signal21 = Signals.new(500, 1000)


golden1 = false
golden2 = false
death1 = false
death2 = false
buy1 = false
buy2 = false
sell1 = false
sell2 = false
first1 = true
first2 = true

intermediate_count = 0
buy_price1 = 0.0
buy_price2 = 0.0
profits1 = 0.0
profits2 = 0.0

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
  signal2.tick( resp.price )
  signal6.tick( resp.price )

  # buying/selling
  if signal2.ready()
    if signal2.golden()
        # buy or sell?
        if death1 and not first1
            # first golden cross after death cross
            buy1 = true
            sell1 = false
            buy_price1 = resp.price
        else
            buy1 = false
            sell1 = false
        end

        # period
        golden1 = true
        death1 = false

    elsif signal2.death() # death SELL
        if golden1 and not first1
            profits1 = profits1 + resp.price - buy_price1
            print "Transaction1: $ %.2f\n" % (resp.price - buy_price1)
            print "Profits1: $ %.2f\n" % profits1
            buy_price1 = 0.0
            buy1 = false
            sell1 = true
        elsif golden1
            # seen death cross
            first1 = false
        else
            buy1 = false
            sell1 = false
        end
        # period
        golden1 = false
        death1 = true
    else
        golden1 = false
        death1 = false
    end
  end

  # buying/selling
  if signal6.ready() == 50
    if signal6.golden() # golden BUY
        # buy or sell?
        if death2 and not first2
            buy2 = true
            sell2 = false
            buy_price2 = resp.price
        else
            buy2 = false
            sell2 = false
        end

        # period
        golden2 = true
        death2 = false

    elsif signal6.death()
        if golden2 and not first2
            profits2 = profits2 + resp.price - buy_price2
            print "Transaction2: $ %.2f\n" % (resp.price - buy_price2)
            print "Profits2: $ %.2f\n" % profits2
            buy_price2 = 0.0
            buy2 = false
            sell2 = true
        elsif golden2 
            first2 = false
        else
            buy2 = false
            sell2 = false
        end
        # period
        golden2 = false
        death2 = true
    else
        golden2 = false
        death2 = false
    end
  end
  # print Time.now.strftime("%H:%M:%S %Y-%m-%d\t") + "$ %.2f\t" % resp.price + "$ %.2f\t" % tick_5.mean + "$ %.2f\n" % tick_30.mean
end



# websocket stuff
EM.run do
  websocket.start!
  EM.add_periodic_timer(1) {
    websocket.ping do
      # p "Websocket is alive"
    end
  }
  EM.error_handler { |e|
    p "Websocket Error: #{e.message}"
  }
end
