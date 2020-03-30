# csv pairs received on stdin
# if only 2 fields, first assumed date and second height in metres
# if 3 fields, first assumed date, second time of day and third height in metres
# all other numbers of fields rejected (not put into database)
# NOTE: this works for fields separated by , or ;
import sys
import dbm
import time
import string
import common

DB_PATH=common.get_env.str('DB_PATH',default='data/waterlevel_history')

with dbm.open(DB_PATH,'c') as db:
    for line in sys.stdin:
        line=line.strip(string.whitespace+',;').translate({ord(';'):ord(',')})
        fields=line.split(',')
        if len(fields) == 2:
            # if no hour of day, set hour to 12:00 PM
            hour_of_day="12:00 PM"
            height=fields[1]
        elif len(fields) == 3:
            hour_of_day=fields[1]
            height=fields[2]
        else:
            continue # bad number of fields
        secs=time.mktime(
            time.strptime(
                fields[0]+' '+hour_of_day,"%Y/%m/%d %I:%M %p"))
        value=','.join([fields[0],hour_of_day,height])
        db[str(secs)]=value

            
