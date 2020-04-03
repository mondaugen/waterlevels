import sys
import dbm
import plotly.graph_objects as go
import time
import numpy as np
import common

def db_to_fmttime_y(
db_path,
time_ival,
time_format='%Y %m %d %H:%M',
return_seconds=False):
    """
    looks up data indexed by time in epoch seconds from a database
    spaces the data equally by interpolating
    formats the x-axis using strftime
    returns array of formated times and y
    """

    times=[]
    levels=[]
    date_time=[]
    with dbm.open(db_path,'r') as db:
        numer_keys=[(float(k),k) for k in db.keys()]
        for nk,k in sorted(numer_keys,key=lambda t: t[0]):
            entries=[b.decode() for b in db[k].split(bytes(',',encoding='utf-8'))]
            nv=float(entries[-1])
            dt=' '.join(entries[:-1])
            times.append(nk)
            levels.append(nv)
            date_time.append(dt)

    # Because Plotly seems to assume dates are equally spaced, we linearly
    # interpolate the depths looked up at equally spaced times
    t=np.array(times)
    l=np.array(levels)
    t_=np.arange(t.min(),t.max()+time_ival,time_ival)
    l_=np.interp(t_, t, l)

    # now convert the equally spaced times to date formats
    dt_=[time.strftime(time_format,time.localtime(t__)) for t__ in t_]
    if return_seconds:
        return (dt_,l_,t_)
    return (dt_,l_)
