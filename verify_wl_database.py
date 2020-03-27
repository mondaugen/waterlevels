import dbm
with dbm.open('data/waterlevel_history','r') as db:
    for k in db.keys():
        print(k,db[k])
