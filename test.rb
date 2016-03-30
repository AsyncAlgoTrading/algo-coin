require 'coinbase/exchange'
require 'eventmachine'
require 'ostruct'

# signals
tick_5 = Array.new
tick_15 = Array.new
tick_30 = Array.new
tick_50 = Array.new
tick_100 = Array.new
tick_200 = Array.new
tick_500 = Array.new
tick_1000 = Array.new

momentum_5 = Array.new
momentum_15 = Array.new
momentum_30 = Array.new
momentum_50 = Array.new
momentum_100 = Array.new
momentum_200 = Array.new
momentum_500 = Array.new
momentum_1000 = Array.new

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

# make it easy
class Array
  def sum
    inject(0.0) { |result, el| result + el }
  end

  def mean 
    sum / size
  end
end

# logic
websocket.match do |resp|
  tick_5 << resp.price
  tick_15 << resp.price
  tick_30 << resp.price
  tick_50 << resp.price
  tick_100 << resp.price
  tick_200 << resp.price
  tick_500 << resp.price
  tick_1000 << resp.price
  
  # manage ticks
  if tick_5.length > 5
    tick_5.shift
    momentum_5 << tick_5.mean
    momentum_5.shift
  end

  if tick_15.length > 15
    tick_15.shift
    momentum_15 << tick_15.mean
    momentum_15.shift
  end

  if tick_30.length > 30
    tick_30.shift
    momentum_30 << tick_30.mean
    momentum_30.shift
  end

  if tick_50.length > 50
    tick_50.shift
    momentum_50 << tick_50.mean
    momentum_50.shift
  end

  if tick_100.length > 100
    tick_100.shift
    momentum_100 << tick_100.mean
    momentum_100.shift
  end

  if tick_200.length > 200
    tick_200.shift
    momentum_200 << tick_200.mean
    momentum_200.shift
  end
  
  if tick_500.length > 500
    tick_500.shift
    momentum_500 << tick_500.mean
    momentum_500.shift
  end

  if tick_1000.length > 1000
    tick_1000.shift
    momentum_1000 << tick_1000.mean
    momentum_1000.shift
  end

  # buying/selling
  if tick_30.length == 30
    if tick_5.mean > tick_30.mean
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
    elsif tick_30.mean > tick_5.mean
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
  if tick_50.length == 50
    if tick_15.mean > tick_50.mean
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
    elsif tick_50.mean > tick_15.mean
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
