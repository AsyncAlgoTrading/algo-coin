require 'coinbase/exchange'
require_relative 'utils'

class Execution
    def initialize(  )
        @total = 0.0
    end
    attr_reader :total
end
