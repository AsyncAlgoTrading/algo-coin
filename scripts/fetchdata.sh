#!/bin/bash
BASE_URL="http://api.bitcoincharts.com/v1/csv/"

function help_and_quit {
    echo "usage: fetchdata -e <bitfinex/bitstamp/coinbase/itbit/kraken/hitbtc/lake> -c <USD>"
    exit
}

EXCHANGE="coinbase"
CURRENCY="USD"

# while [[ $# -gt 1 ]]
# do
# key="$1"
# case $key in
#     -e|--exchange)
#     EXCHANGE="$2"
#     case $EXCHANGE in
#         bitfinex)
#         ;;
#         bitstamp)
#         ;;
#         coinbase)
#         ;;
#         itbit)
#         ;;
#         kraken)
#         ;;
#         hitbtc)
#         ;;
#         lake)
#         ;;
#         *)
#         help_and_quit # unknown option
#         ;;
#     esac
#     shift # past argument
#     ;;
#     -c|--currency)
#     CURRENCY="$2"
#     shift # past argument
#     ;;
#     *)
#     help_and_quit # unknown option
#     ;;
# esac
# shift
# done

while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    bitfinex)
    EXCHANGE="$1"
    shift # past argument
    ;;
    bitstamp)
    EXCHANGE="$1"
    shift # past argument
    ;;
    coinbase)
    EXCHANGE="$1"
    shift # past argument
    ;;
    itbit)
    EXCHANGE="$1"
    shift # past argument
    ;;
    kraken)
    EXCHANGE="$1"
    shift # past argument
    ;;
    hitbtc)
    EXCHANGE="$1"
    shift # past argument
    ;;
    lake)
    EXCHANGE="$1"
    shift # past argument
    ;;
    USD)
    CURRENCY="$1"
    shift # past argument
    ;;
    *)
    help_and_quit # unknown option
    ;;
esac
shift
done


BASE="wget -cN " 
DESTINATION="data/exchange/" 
FILE=$EXCHANGE$CURRENCY
COMMAND="$BASE$BASE_URL$FILE".csv.gz""

# get file
echo $COMMAND
$COMMAND

# make directory
mkdir -p $DESTINATION

# move to location
mv $FILE".csv.gz" $DESTINATION

# extract
gunzip $DESTINATION$FILE".csv.gz"
