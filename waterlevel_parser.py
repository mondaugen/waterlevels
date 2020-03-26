from html.parser import HTMLParser
class WaterParse(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.relaying=False
        self.depth=0
    def handle_starttag(self,tag,attrs):
        if self.depth == 0:
            for k,v in attrs:
                if (k == 'class'):
                    self.relaying=(v == 'stationTextData')
        if self.relaying:
            self.depth += 1
    def handle_endtag(self,tag):
        if self.relaying:
            self.depth -= 1
        if self.depth == 0:
            self.relaying = False
    def handle_data(self,data):
        if self.relaying:
            print(data.strip())

wp=WaterParse()

with open('/tmp/hmm','r') as f:
    wp.feed(f.read())

    
