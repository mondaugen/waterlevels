# Get the html that plots the waterlevel history
import sys
import dbm
import plotly.graph_objects as go
import time
import numpy as np
import common
import plotwl

# default is 60 minutes between observations
TIME_IVAL=common.get_env.float('TIME_IVAL',default=3600)
DB_PATH=common.get_env.str('DB_PATH',default='data/waterlevel_history')
RENDER_HTML=common.get_env.int('RENDER_HTML',default=0)
FIG_TITLE=common.get_env.str('FIG_TITLE',
default='St. Lawrence river water level measured at Jetee #1')

# now convert the equally spaced times to date formats
dt_,l_=plotwl.db_to_fmttime_y(DB_PATH,TIME_IVAL)

fig = go.Figure(
    data=[go.Line(x=dt_,y=l_)]
)

fig.update_layout(
    title=FIG_TITLE,
    xaxis=dict(title='Date'),
    yaxis=dict(title='Height (metres)')
)

if RENDER_HTML != 0:
    fig.write_html(sys.stdout)
else:
    fig.show()
