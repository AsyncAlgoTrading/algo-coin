require_relative 'strategies'

f = File.new( 'config.cfg' )
f.each_line do |l|
  row = l.strip.split(', ')
  clazz = Object.const_get( row[ 1 ].strip )
  clazz.new( *row[ 2..-1 ] )
end
