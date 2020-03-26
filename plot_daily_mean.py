import plotly.graph_objects as go

dates=[]
levels=[]

with open('15520-01-JAN-1960_slev.csv','r') as f:
    for line in f.readlines():
        line=line.strip()
        if (len(line)>0) and line[0] != '#':
            fields=line.split(',')
            if len(fields) >= 2:
               dates.append(fields[0])
               levels.append(fields[1])
            else:
                print("bad line: %s" % (line,))

fig = go.Figure(
    data=[go.Line(x=dates,y=levels)]
)
#fig.show(renderer='iframe')
