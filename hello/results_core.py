# from __future__ import print_function
import cgi
import os
import re
from collections import OrderedDict
from urllib2 import urlopen

import time



def html_escape(text):
    # http://stackoverflow.com/questions/2077283/escape-special-html-characters-in-python
    """Produce entities within text."""
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }

    return "".join(html_escape_table.get(c, c) for c in text)

def adrian_html_escape(text):
    # http://stackoverflow.com/questions/2004168/escape-quotes-in-javascript
    html_escape_table = {
        # "&": "&amp;",
        # '"': "&quot;",
        "'": "\x27",
        # ">": "&gt;",
        # "<": "&lt;",
    }
    for c in text:
        print(c)
        if c in html_escape_table:
            print('found')

    return "".join(html_escape_table.get(c, c) for c in text)

def adrian_html_escape2(text):
    # http://stackoverflow.com/questions/2004168/escape-quotes-in-javascript
    html_escape_table = {
        # "&": "&amp;",
        # '"': "&quot;",
        "'": "_",
        # ">": "&gt;",
        # "<": "&lt;",
    }

    return "".join(html_escape_table.get(c, c) for c in text)

import sys
from bs4 import BeautifulSoup
import tabulate


def get_unique_cats(records):
    ret = []
    a_set = set()
    for r in records:
        if r['category'].name not in a_set:
            ret.append(r['category'])
        a_set.add(r['category'].name)
    return ret


def do_graphs_output(resultsModel, out_dir):
    map_file = out_dir + '/' + 'graphs.htm'
    page_html_str = get_graphs_out_html(resultsModel)

    if len(resultsModel.records) > 0:
        with open(map_file, 'wb') as handle:
            handle.write(page_html_str)


def get_graphs_out_html(resultsModel):
    records = resultsModel.records
    if len(records) == 0:
        return 'error 2. no supported records found'
    else:
        cats = get_unique_cats(records)  # ['Novice', 'Street Modified', 'H Street']
        # print(cats)
        # charts_num = len(cats) + 1

        charts_num = 0
        all_tables_str = ''
        func_name, table_str = get_table_str(records, "0", "all categories")
        func_names=[]
        if func_name and table_str:
            func_names.append(func_name)
        all_tables_str += table_str
        for i, cat in enumerate(cats):
            func_name,a_table_str = get_table_str2(cat, records, str(i + 1))
            if a_table_str:
                all_tables_str += a_table_str
                charts_num +=1
                func_names.append(func_name)

        draw_funcs_str = '\n'.join([str(x) + ';' for x in func_names])
        html1 = '''
                        <html>
              <head>
                <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
                <script type="text/javascript">
            google.charts.load("current", {
              packages: ["corechart"]
            });
            google.charts.setOnLoadCallback(drawCharts);

        function drawCharts() {
        ''' + draw_funcs_str + '''

        }
        '''


        # chart_divs_str='\n'.join(['drawChart'+str(x)+'();' for x in range(4) ])
        chart_divs_str = '\n'.join(['<div id="chart_div' + str(x) + '" style=""></div>' for x in range(charts_num)])
        html2b = '''

            </script>
          </head>
          <body>
            <a href="''' + resultsModel.url + '''" target="_blank">''' + resultsModel.results_title + '''</a><br>
            ''' + chart_divs_str + '''
          </body>
        </html>

        '''
        page_html_str = html1 + all_tables_str + html2b
        return page_html_str


def get_table_str2(cat, records, id):
    return get_table_str([x for x in records if cat.name == x['category'].name], id, cat.code + " - '" + cat.name + "'",
                         True)


def get_table_str(records_1, id, title, show_place_and_trophy=False):
    if len(records_1)==0:
        return None, 'error 1. no records found'
    else:
        func_name = 'drawChart' + id + '()'
        html1b = '''
        function '''+func_name+''' {
          var data = new google.visualization.DataTable();
            '''
        chart_data_str = ''
        rows_num = 0
        for r in records_1:
            for run in r['runs']:
                if run.is_valid_for_chart():
                    rows_num = max(rows_num, int(run.id))
        # rows_num+=1
        chart_data_str += "data.addRows(" + str(rows_num) + ");\n"
        chart_data_str += "data.addColumn('string', 'run');\n"

        for r in records_1:
            legend_str = ''
            if show_place_and_trophy:
                legend_str += r['place2']
                legend_str += ' '
            escaped_name = adrian_html_escape2(r['name'])
            # print('escaped_name: '+escaped_name)
            legend_str += escaped_name
            if show_place_and_trophy:
                legend_str += (' (T)' if r['trophy'] else '')
            chart_data_str += "data.addColumn('number', '" + legend_str + "');\n"
        # for i, r in enumerate(records_1):
        #     chart_data_str += "data.setValue(" + str(i) + ", 0, " + str(i + 1) + "); // " + r['name'] + "\n"
        for i in range(rows_num):
            chart_data_str += "data.setValue(" + str(i) + ", 0, '" + str(i + 1) + "'); \n"
        run_unique_ids = set()
        for i, r in enumerate(records_1):
            for run in r['runs']:
                if run.is_valid_for_chart():
                    run_unique_ids.add(int(run.id))
                    chart_data_str += "data.setValue(" + str(int(run.id) - 1) + ", " + str(i + 1) + ", " + str(
                        run.time) + "); // " + r[
                                          'name'] + " run: " + str(run.id) + "\n"
        max_value_str = ''
        if len(run_unique_ids) > 0:
            max_value_str = str(list(run_unique_ids)[-1])
        html2 = '''
        var options = {
            //legend: 'none',
            hAxis: {
                minValue: 1, maxValue: ''' + max_value_str + '''
                ,title: 'run'
                //,format: 'none'
                },
            //vAxis: { maxValue: 100 },
            vAxis: { title: 'time(sec)' },
            //colors: ['#795548'],
            pointSize: 10,
            pointShape: 'square',
            interpolateNulls: true
            ,height: 900
            ,explorer: {
                    axis: 'vertical',
                    keepInBounds: true
                }
            ,title:   "''' + title + '''"
          };

          var chart = new google.visualization.LineChart(document.getElementById('chart_div''' + id + ''''));
          chart.draw(data, options);
        }
    '''
        if not max_value_str:
            return None, None
        return func_name, html1b + chart_data_str + html2


class Category(object):
    def __init__(self):
        self.raw_str = None
        self.code = None
        self.name = None

    @classmethod
    def from_raw_str(cls, raw_str):
        ret = Category()
        ret.raw_str = raw_str
        m = re.search("(?P<code>.+) - '(?P<name>.+)'.*", ret.raw_str)
        if m:
            ret.code = m.group('code')
            ret.name = m.group('name')
        return ret

    def __repr__(self):
        return 'Category{' \
               + 'raw_str="' + self.raw_str + '"' \
               + ', ' + 'code="' + str(self.code) + '"' \
               + ', ' + 'name="' + str(self.name) + '"' \
               + '}'


class Run(object):
    def __init__(self):
        self.raw_str = None
        self.id = None
        self.dnf = None
        self.time = None
        self.penalty_seconds = 0

    @classmethod
    def from_raw_str(cls, id, raw_str):
        ret = Run()
        ret.id = id
        ret.raw_str = raw_str
        ret.dnf = '+dnf' in ret.raw_str
        if not ret.dnf and '999.999' not in ret.raw_str and 'off' not in ret.raw_str:
            # ret.time = ret.raw_str.replace('+dnf', '')
            m = re.search("(?P<time>\d+\.\d+)(\+(?P<penalty>\d+))?", ret.raw_str)
            if m:
                ret.time = float(m.group('time'))
                if m.group('penalty'):
                    ret.penalty_seconds = int(m.group('penalty'))
        return ret

    def __repr__(self):
        return 'Run{' \
               + 'raw_str="' + self.raw_str + '"' \
               + ', ' + 'id="' + str(self.id) + '"' \
               + ', ' + 'dnf=' + str(self.dnf) \
               + ', ' + 'time="' + str(self.time) + '"' \
               + '}'

    def is_valid_for_chart(self):
        return self.time





class ResultsParser(object):
    def __init__(self):
        pass

    def parse(self, url):
        # page = '05-07-16-daytona_fin.htm'
        # page = '05-22-16-brooksville_fin.htm'
        # url = 'http://cfrsolo2.com/2016/04-17-16-brooksville_fin.htm'

        print('ResultsParser.parse('+url+')')

        # page = url[url.rfind('/') + 1:]
        # html = urlopen(url).read()
        # filename = page  # '05-07-16-daytona_fin.htm'
        # with open(filename, 'w') as f:
        #     f.write(html)

        # lines = None
        # with open('05-07-16-daytona_fin.htm') as f:
        #      lines = f.readlines()
        # for i,line in enumerate(lines):
        #     print(str(i)+' '+line)

        # soup = BeautifulSoup(open(filename))
        soup = BeautifulSoup(urlopen(url).read())

        # results_table = soup.find('table', {'border': '1'})
        records = []
        row_headers = []
        fixed_headers = ['place', 'unknown', 'number', 'name', 'car', 'color', 'run1', 'run2', 'run3', 'run4', 'run5',
                         'run6',
                         'total', 'diff']
        trs = soup.find_all('table')[1].find_all('tr')
        # print('len(trs): ' + str(len(trs)))
        for tr in trs:
            # print(tr)
            ths = tr.find_all('th')
            if (len(ths) > 0):
                # print('h ', end="")
                row_headers = [str(th.text).strip() for th in ths]
                # print('h ' + ', '.join(row_headers))
                # for th in ths:
                #     print(str(th.string), end=", ")
                # print('')
            # print(' len(row_headers): '+str(len(row_headers)))
            tds = tr.find_all('td')
            # print(' len(tds): ' + str(len(tds)))
            record = {}
            if (len(tds) > 0):
                row_datas = [str(td.string).strip() for td in tds]
                # print('  len(row_datas): ' + str(len(row_datas)))
                if len(row_datas) == 10 or len(
                        row_datas) == 13 or len(
                        row_datas) == 14:  # need a better way to uniquely identify the records table
                    record = OrderedDict(zip(fixed_headers, row_datas))
                    # print(zipped_d)
                    # print('d ' + ', '.join(row_datas))
                    if record['name'] == 'None':
                        continue
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




class ResultsModel(object):
    def __init__(self, records, results_title, url):
        self.records = records
        self.results_title = results_title
        self.url = url

def main():
    resultsParser = ResultsParser()

    # resultsModel = resultsParser.parse('http://cfrsolo2.com/2016/04-17-16-brooksville_fin.htm')
    # resultsModel = resultsParser.parse('http://cfrsolo2.com/2016/04-02-16-occc_fin.htm')
    resultsModel = resultsParser.parse('http://cfrsolo2.com/2016/04-03-16-occc_fin.htm')

    # print(tabulate.tabulate(display_rows, headers='firstrow', tablefmt="fancy_grid"))

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    parent_out_dir = 'outputs'
    out_dir = parent_out_dir + '/' + timestamp
    # if args.out_tag:
    #     out_dir+='_'+args.out_tag
    os.makedirs(out_dir)
    do_graphs_output(resultsModel, out_dir)

if __name__ == '__main__':
    sys.exit(main())

