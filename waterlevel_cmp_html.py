# Compare waterlevels measured in difference places
import sys
import dbm
import plotly.graph_objects as go
import time
import numpy as np
import common
import plotwl

# default is 60 minutes between observations
TIME_IVAL=common.get_env.float('TIME_IVAL',default=3600)
# a string containing a %s where the station ID should be inserted
DB_PATH_FMT=common.get_env.str('DB_PATH_FMT',default='data/waterlevel_history_%s')
RENDER_HTML=common.get_env.int('RENDER_HTML',default=0)
# a string containing station IDs separated by commas
STATION_IDS=common.get_env.str('STATION_IDS',default='15520,15540')
# a string containing data labels, separated by commas
STATION_LABELS=common.get_env.str('STATION_LABELS',default='Jetee #1, rue Frontenac')
FIG_TITLE=common.get_env.str('FIG_TITLE',
default='St. Lawrence river water level measured at ' + STATION_LABELS)
# station ID pairs, separated by commas, that should be compared
# different pairs should be separated by ;
# the comparison is made by subtracting the corresponding heights from the
# second ID from those of the first ID.
STATION_DIFFS=common.get_env.str('STATION_DIFFS',
default='15540,15520;')

station_ids=STATION_IDS.split(',')
station_labels=STATION_LABELS.split(',')

# now convert the equally spaced times to date formats
data=[]
data_info=dict()
for sid,sla in zip(station_ids,station_labels):
    sla=sla.strip()
    db_path=DB_PATH_FMT % (sid,)
    dt_,l_,t_=plotwl.db_to_fmttime_y(db_path,TIME_IVAL,return_seconds=True)
    data.append(go.Line(x=dt_,y=l_,name=sla))
    data_info[sid]=dict(label=sla,
                        fmtt=dt_,
                        t=t_,
                        h=l_)
# now do comparisons
for pair in filter(len,STATION_DIFFS.split(';')):
    a,b=pair.split(',')
    # find common time range
    mint=max(np.min(data_info[a]['t']),np.min(data_info[b]['t']))
    maxt=min(np.max(data_info[a]['t']),np.max(data_info[b]['t']))
    # find indices where range starts and stops for each dataset
    si_a=np.where(data_info[a]['t']==mint)[0][0]
    si_b=np.where(data_info[b]['t']==mint)[0][0]
    ei_a=np.where(data_info[a]['t']==maxt)[0][0]
    ei_b=np.where(data_info[b]['t']==maxt)[0][0]
    dh=data_info[b]['h'][si_b:ei_b]-data_info[a]['h'][si_a:ei_a]
    data.append(go.Line(x=data_info[a]['fmtt'][si_a:ei_a],
                y=dh,
                name='(%s)-(%s)' % (data_info[b]['label'],data_info[a]['label'])))

fig = go.Figure(
    data=data
)

fig.update_layout(
    title=FIG_TITLE,
    xaxis=dict(title='Date'),
    yaxis=dict(title='Height (metres)')
)

if RENDER_HTML != 0:
    fig.write_html(sys.stdout,include_plotlyjs='cdn',post_script='PLOT_DIV="{plot_id}";')
else:
    fig.show()
