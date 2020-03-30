# Get the html that plots the waterlevel history
import sys
import dbm
import plotly.graph_objects as go
import time

times=[]
levels=[]
date_time=[]
with dbm.open('data/waterlevel_history','r') as db:
    numer_keys=[(float(k),k) for k in db.keys()]
    for nk,k in sorted(numer_keys,key=lambda t: t[0]):
        entries=[b.decode() for b in db[k].split(bytes(',',encoding='utf-8'))]
        nv=float(entries[-1])
        dt=' '.join(entries[:-1])
        times.append(time.strftime('%Y %m %d %H:%M',time.localtime(nk)))
        levels.append(nv)
        date_time.append(dt)

fig = go.Figure(
    data=[go.Line(x=times,y=levels)]
)

#fig.update_layout(
#    xaxis=dict(
#        #tickmode='array',
#        #tickvals=times[::len(times)//10],
#        #ticktext=date_time[::len(times)//10],
#        tickformat='%x'
#    )
#)

#fig.write_html(sys.stdout)
fig.show()
