from urllib2 import HTTPError

from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
from hello.results_parser import ResultsParser
from homepage import get_years_from_homepage, get_html_for_year
from results_core import get_unique_cats, get_graphs_out_html
from .models import Greeting

# Create your views here.


def index(request):
    # return HttpResponse('Hello from Python!')
    # return render(request, 'index.html' )
    resultsParser = ResultsParser()
    resultsModel = resultsParser.parse('http://cfrsolo2.com/2016/04-17-16-brooksville_fin.htm')
    # return render(request, 'adrian0.html')
    # r = requests.get('http://httpbin.org/status/418')
    # print r.text
    # return HttpResponse('<pre>' + r.text + '</pre>')
    soup = BeautifulSoup()

    new_img_tag = soup.new_tag("img", style='position: absolute; top: 0; right: 0; border: 0;')
    new_a_tag = soup.new_tag("a", href='https://github.com/orozcoadrian/race-graphs')
    new_a_tag.append(new_img_tag)
    soup.append(new_a_tag)

    years = get_years_from_homepage()

    for year in years:
        new_a_tag = soup.new_tag("a", href=year)
        new_a_tag.string = year
        soup.append(new_a_tag)
        new_a_tag.append(soup.new_tag('br'))
    # self.wfile.write(soup.prettify())
    return HttpResponse(soup.prettify())


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def year(request, year):
    # return HttpResponse('handling year: '+str(year))
    # self.wfile.write(self.get_html_for_year(self.path[1:]))
    return HttpResponse('handling year: '+str(year)+'<br>'+get_html_for_year(year))

def path(request, path):
    # return HttpResponse('handling path: '+str(path))
    # self.wfile.write(self.get_html_for_year(self.path[1:]))
    # return HttpResponse('handling year: '+str(year)+'<br>'+get_html_for_year(year))
    resultsParser = ResultsParser()
    try:
        resultsModel = resultsParser.parse('http://cfrsolo2.com/' + path[4:])
        records = resultsModel.records

        cats = get_unique_cats(records)  # ['Novice', 'Street Modified', 'H Street']
        html_str = get_graphs_out_html(resultsModel)
        # print(cats)
        # bs = BeautifulSoup()

        # tag.append(new_string)
        # bs.append(NavigableString("handling request for: "+self.path))
        # bs.append(NavigableString("categories num: "+str(len(cats))))
        # bs.append(html_str)
        # self.wfile.write(html_str)
        return HttpResponse(html_str)
    except HTTPError, e:
        print(e.code)
        print(e.msg)
        # print(e.headers)
        # print(e.fp.read())
        # self.wfile.write('error: ' + str(e.code) + '; ' + e.msg)
        return HttpResponse('error: ' + str(e.code) + '; ' + e.msg)

