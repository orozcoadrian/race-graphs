from urllib2 import urlopen

import requests
from bs4 import BeautifulSoup



def get_years_from_homepage():
    url = 'http://cfrsolo2.com/'
    # r = requests.get('http://cfrsolo2.com/2016/index.php')
    html = urlopen(url).read()
    # filename = page  # '05-07-16-daytona_fin.htm'
    # with open(filename, 'w') as f:
    #     f.write(html)
    # lines = None
    # with open('05-07-16-daytona_fin.htm') as f:
    #      lines = f.readlines()
    # for i,line in enumerate(lines):
    #     print(str(i)+' '+line)
    soup = BeautifulSoup(html)
    # print(soup.prettify())
    the_lis_parent = soup.select('li#n-shows')
    the_lis_parent = soup.find(id='n-shows')
    the_lis = the_lis_parent.find_all('li')
    # print(str(len(the_lis)))
    # print(the_lis)
    years = []
    for a_li in the_lis:
        # print('-> ' + a_li.a.text)
        years.append(a_li.a.text)
    return years


def get_html_for_year(self, year):
    r = requests.get('http://cfrsolo2.com/' + year + '/index.php')
    soup = BeautifulSoup(
        r.text)  # self.wfile.write(r.content.replace('<th width="200">Raw</th>', '<th width="200">Raw</th><th width="200">viz</th>'))
    first_table = soup.find_all('table')[0]
    my = first_table.find_all('tr')[1].find_all('th')[4]
    new_tag = soup.new_tag("th", width="200")
    new_tag.string = "viz"
    # my.append(new_tag)
    for my_i in soup.find_all('iframe'):
        # print('found an iframe')
        my_i.extract()
    for i, my_i2 in enumerate(first_table.find_all('script')):
        # print('found a script')
        # print(my_i2)
        my_i2.clear()
        my_i2['src'] = 'cleared'
        # if i == 0:
        #     my_i2.extract()
        #     break
        # print(my)
    # first_table.find('script').extract()
    # print(first_table)
    trs = first_table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds) > 3:
            the_raw = tds[1]
            # print(the_raw)
            # print(the_raw)
            if the_raw and the_raw.a:
                new_a_tag = soup.new_tag("a", href=year + '/' + the_raw.a['href'])
                print(new_a_tag)

                new_a_tag.string = "viz"
                # new_a_tag.encode_contents(formatter='html')
                # the_raw.append(new_td_tag)
                new_td_tag = soup.new_tag("td", align="center")
                # new_td_tag.string = "hi"
                the_raw.append(NavigableString("["))
                the_raw.append(new_a_tag)
                the_raw.append(NavigableString("]"))
                # print(the_raw)
                # new_a_tag.wrap(new_a_tag)
        for td in tds:
            # print(td)
            if td.a:
                print('before: ' + td.a['href'])
                td.a['href'] = 'http://cfrsolo2.com/' + year + '/' + td.a['href']
                print('after: ' + td.a['href'])
    return first_table.encode('utf-8')