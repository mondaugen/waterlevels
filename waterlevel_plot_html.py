# Get the html that plots the waterlevel history
import sys
import dbm
import plotly.graph_objects as go
import time
import numpy as np
import common

# default is 60 minutes between observations
TIME_IVAL=common.get_env.float('TIME_IVAL',default=3600)
DB_PATH=common.get_env.str('DB_PATH',default='data/waterlevel_history')
RENDER_HTML=common.get_env.int('RENDER_HTML',default=0)

times=[]
levels=[]
date_time=[]
with dbm.open(DB_PATH,'r') as db:
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
t_=np.arange(t.min(),t.max()+TIME_IVAL,TIME_IVAL)
l_=np.interp(t_, t, l)

# now convert the equally spaced times to date formats
dt_=[time.strftime('%Y %m %d %H:%M',time.localtime(t__)) for t__ in t_]

fig = go.Figure(
    data=[go.Line(x=dt_,y=l_)]
)

fig.update_layout(
    title='St. Lawrence water level measured at Jetee #1',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Height (metres)')
)

if RENDER_HTML != 0:
    fig.write_html(sys.stdout)
else:
    fig.show()
