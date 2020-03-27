from waterlevel_parser import FindWaterCSV

fw=FindWaterCSV()

with open('/tmp/water.html','r') as f:
    fw.feed(f.read())
