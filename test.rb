require 'coinbase/exchange'
require 'eventmachine'
require 'ostruct'

# signals
tick_5 = Array.new
tick_30 = Array.new
tick_200 = Array.new
tick_1000 = Array.new
moving_up = false
moving_down = false
golden = false
death = false
buy = false
sell = false
first = true


intermediate_count = 0
buy_price = 0.0
profits = 0.0

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
  tick_30 << resp.price
  tick_200 << resp.price
  tick_1000 << resp.price
  
  # manage ticks
  if tick_5.length > 5
    tick_5.shift
  end
  
  if tick_5.length > 5
    tick_5.shift
  end
  
  if tick_30.length > 30
    tick_30.shift
  end
  
  if tick_200.length > 200
    tick_200.shift
  end
  
  if tick_1000.length > 1000
    tick_1000.shift
  end

  # buying/selling
  if tick_5.length == 5 and tick_30.length == 30
    if tick_5.mean > tick_30.mean
        # buy or sell?
        if death and not first
            print "GOLDEN: "
            buy = true
            sell = false
        elsif death
            first = false
        else
            buy = false
            sell = false
        end

        # period
        golden = true
        death = false
    elsif tick_30.mean > tick_5.mean
        # buy or sell?
        if golden and not first
            print "DEATH: "
            buy = false
            sell = true
        elsif death
            first = false
        else
            buy = false
            sell = false
        end

        # period
        golden = false
        death = true
    else
        golden = false
        death = false
    end

  end
  print Time.now.strftime("%H:%M:%S %Y-%m-%d\t") + "$ %.2f\t" % resp.price + "$ %.2f\t" % tick_5.mean + "$ %.2f\n" % tick_30.mean
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
