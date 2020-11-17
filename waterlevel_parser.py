from html.parser import HTMLParser
import re

# match the paragraph containing the link
link_p_matcher=re.compile("^Data file has been created, click on the file name to download\.")
class WaterParse(HTMLParser):
    """ Parse waterlevels from a site displaying them in list format """
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

class FindWaterCSV(WaterParse):
    """
    Find the URL to a CSV file containing the waterlevels so the CSV can be
    downloaded.
    """
    def handle_starttag(self,tag,attrs):
        if self.relaying and (tag == 'a'):
            for k,v in attrs:
                if k == 'href':
                    print(v)
                    self.relaying = False
    def handle_data(self,data):
        data=data.strip()
        if link_p_matcher.match(data):
            self.relaying=True
        
                
