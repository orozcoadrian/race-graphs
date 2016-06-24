from collections import OrderedDict
from urllib2 import urlopen

from bs4 import BeautifulSoup

from hello.categories import Category
from hello.results import Run, ResultsModel


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

        soup = BeautifulSoup(html)

        records = []
        row_headers = []
        fixed_headers = ['place', 'unknown', 'number', 'name', 'car', 'color', 'run1', 'run2', 'run3', 'run4', 'run5',
                         'run6',
                         'total', 'diff']
        for tr in soup.find_all('table')[1].find_all('tr'):
            # print(tr)
            ths = tr.find_all('th')
            if (len(ths) > 0):
                # print('h ', end="")
                row_headers = [str(th.text).strip() for th in ths]
                print('h ' + ', '.join(row_headers))
                # for th in ths:
                #     print(str(th.string), end=", ")
                # print('')
            tds = tr.find_all('td')
            record = {}
            if (len(tds) > 0):
                row_datas = [str(td.string).strip() for td in tds]
                if len(row_datas) == 13 or len(
                        row_datas) == 14:  # need a better way to uniquely identify the records table
                    record = OrderedDict(zip(fixed_headers, row_datas))
                    # print(zipped_d)
                    # print('d ' + ', '.join(row_datas))
                    record['place2'] = record['place'].replace('T', '')
                    record['trophy'] = 'T' in record['place']
                    record['category'] = Category.from_raw_str(row_headers[0])
                    runs = []
                    for i in range(1, 6):
                        if 'run' + str(i) in record and 'None' not in record['run' + str(i)]:
                            runs.append(Run.from_raw_str(str(i), record['run' + str(i)]))
                    record['runs'] = runs
                    # print(record)
                    records.append(record)

        results_title = soup.find_all('table')[0].find_all('th')[2].string
        return ResultsModel(records, results_title, url)