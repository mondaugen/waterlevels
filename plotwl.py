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
return_seconds=False,
t_min=None,
t_max=None):
    """
    looks up data indexed by time in epoch seconds from a database
    spaces the data equally by interpolating
    formats the x-axis using strftime
    if t_min or t_max are specified, these are used to limit the bounds on the
    output times. They are specified in the same format as time_format.
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
    if t_min is None:
        t_min = t.min()
    else:
        t_min = time.mktime(time.strptime(t_min,time_format))
    if t_max is None:
        t_max = t.max()
    else:
        t_max = time.mktime(time.strptime(t_max,time_format))
    t_=np.arange(t_min,t_max+time_ival,time_ival)
    l_=np.interp(t_, t, l)

    # now convert the equally spaced times to date formats
    dt_=[time.strftime(time_format,time.localtime(t__)) for t__ in t_]
    if return_seconds:
        return (dt_,l_,t_)
    return (dt_,l_)
