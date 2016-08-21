require 'coinbase/exchange'
require 'eventmachine'
require 'ostruct'
require_relative 'utils'
require_relative 'bank'
require_relative 'strategies'

accts = Bank.new()
strat = StrategyManager.new( accts )
VERBOSE = false

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
    if VERBOSE
    # p resp
    end
end

#order opened
websocket.open do |resp|
    if VERBOSE
    if resp.remaining_size > 10
        print "[NEW] \t %s \t\t %3.3f \t@ %.2f\n" % [resp.side, resp.remaining_size, resp.price]
    else
        print "[NEW] \t %s \t\t %3.3f \t\t@ %.2f\n" % [resp.side, resp.remaining_size, resp.price]
    end
    end
end

#order off the books
websocket.done do |resp|
    if VERBOSE
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
end

#order changed
websocket.change do |resp|
    if VERBOSE
        print "[MOD] \t %s \t\t %3.3f \t\t@ %.2f\n" % [resp.side, resp.remaining_size, resp.price]
    end
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
