from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
from hello.results_parser import ResultsParser
from homepage import get_years_from_homepage, get_html_for_year
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
    return HttpResponse('handling year: '+get_html_for_year(year))

