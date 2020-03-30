# this is used to fill in the past waterlevels
# these are updated a week or so after the waterlevels are recorded so there is
# a gap in time between the water levels you can get today (at 15 minute
# intervals) and all the water levels recorded in the past (resolution is daily
# mean)
# we would run this script everyday, so the data base would slowly get filled
# and fill in the gap (after an initial running we would change start period to
# a more recent date)
#
# parse csv file address
# download it
# parse out the water levels
# add to database
# this should only be run rarely, say once a day
# other requests will fill in the missing hours
export PYTHONPATH="$(dirname $0):$PYTHONPATH"
csv_addr="$(curl 'http://www.isdm-gdsi.gc.ca/isdm-gdsi/twl-mne/inventory-inventaire/data-donnees-eng.asp?user=isdm-gdsi&region=LAU&tst=1&no=15520' \
-H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0' \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' \
-H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' --compressed \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Origin: http://www.isdm-gdsi.gc.ca' \
-H 'Connection: keep-alive' \
-H 'Referer: http://www.isdm-gdsi.gc.ca/isdm-gdsi/twl-mne/inventory-inventaire/interval-intervalle-eng.asp?user=isdm-gdsi&region=LAU&tst=1&no=15520' \
-H 'Upgrade-Insecure-Requests: 1' \
--data 'start_period=2000%2F01%2F01&end_period='$(date +%Y%%2F%m%%2F%d)'&resolution=d&time_zone=l&pcode=slev&datum=c' | \
python3 -c '
from waterlevel_parser import FindWaterCSV
import sys
fw=FindWaterCSV()
fw.feed(sys.stdin.read())')"

full_csv_addr="http://www.isdm-gdsi.gc.ca/isdm-gdsi/twl-mne/inventory-inventaire/$csv_addr"
echo "Downloading $full_csv_addr"

# get csv and keep only lines beginning with dates
curl "$full_csv_addr" | grep -E '^[0-9]{4}/[0-9]{2}/[0-9]{2}' | \
python3 "$(dirname $0)/update_wl_database.py"
