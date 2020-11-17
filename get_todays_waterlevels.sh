# remember to update database path to the correct ID, too
[ -z $STATION_ID ] && STATION_ID=15520
export PYTHONPATH="$(dirname $0):$PYTHONPATH"

curl_init_req () {
    curl "https://www.waterlevels.gc.ca/eng/station?type=1&sid=${STATION_ID}&tz=EDT&pres=2" 
}

parse_waterlevels () {
    curl_init_req | \
    python3 -c '
from waterlevel_parser import WaterParse
import sys
wp=WaterParse()
print(wp.feed(sys.stdin.read()))'
}

_main () {
    parse_waterlevels | \
    grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}' | \
    DATE_SEP="-" python3 "$(dirname $0)/update_wl_database.py"
}

if [[ "$1" == curl_init_req ]]; then
    curl_init_req
elif [[ "$1" == parse_waterlevels ]]; then
    parse_waterlevels
else
    _main
fi
