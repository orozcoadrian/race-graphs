from django.shortcuts import render
from django.http import HttpResponse
from hello.results_parser import ResultsParser
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
    return HttpResponse('Hello from Python!')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

