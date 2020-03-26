curl 'http://www.isdm-gdsi.gc.ca/isdm-gdsi/twl-mne/inventory-inventaire/data-donnees-eng.asp?user=isdm-gdsi&region=LAU&tst=1&no=15520' \
-H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0' \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' \
-H 'Accept-Language: en-CA,en-US;q=0.7,en;q=0.3' --compressed \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Origin: http://www.isdm-gdsi.gc.ca' \
-H 'Connection: keep-alive' \
-H 'Referer: http://www.isdm-gdsi.gc.ca/isdm-gdsi/twl-mne/inventory-inventaire/interval-intervalle-eng.asp?user=isdm-gdsi&region=LAU&tst=1&no=15520' \
-H 'Upgrade-Insecure-Requests: 1' \
--data 'start_period=1960%2F01%2F01&end_period='"$(date +%Y%%2F%m%%2F%d)"'&resolution=d&time_zone=l&pcode=slev&datum=c'
# parse csv file address
# download it
# parse out the water levels
# this should only be run rarely, say once a day
# other requests will fill in the missing hours
