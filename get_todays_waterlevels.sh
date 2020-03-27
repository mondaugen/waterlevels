curl 'https://www.waterlevels.gc.ca/eng/station?type=1&sid=15520&tz=EDT&pres=2' | \
python3 -c '
from waterlevel_parser import WaterParse
import sys
wp=WaterParse()
print(wp.feed(sys.stdin.read()))' | \
grep -E '^[0-9]{4}/[0-9]{2}/[0-9]{2}' | \
python3 update_wl_database.py
