from urllib2 import urlopen

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