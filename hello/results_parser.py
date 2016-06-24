from urllib2 import urlopen

class ResultsParser(object):
    def __init__(self):
        pass

    def parse(self, url):
        # page = '05-07-16-daytona_fin.htm'
        # page = '05-22-16-brooksville_fin.htm'
        # url = 'http://cfrsolo2.com/2016/04-17-16-brooksville_fin.htm'
        page = url[url.rfind('/') + 1:]
        html = urlopen(url).read()
        filename = page  # '05-07-16-daytona_fin.htm'
        # with open(filename, 'w') as f:
        #     f.write(html)

        # lines = None
        # with open('05-07-16-daytona_fin.htm') as f:
        #      lines = f.readlines()
        # for i,line in enumerate(lines):
        #     print(str(i)+' '+line)

        # soup = BeautifulSoup(open(filename))