
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
