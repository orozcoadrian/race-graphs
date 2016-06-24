from django.shortcuts import render

from hello.results_parser import ResultsParser
from .models import Greeting


# Create your views here.


def index(request):
    # return HttpResponse('Hello from Python!')
    # return render(request, 'index.html' )
    resultsParser = ResultsParser()
    return render(request, 'adrian0.html')
    # r = requests.get('http://httpbin.org/status/418')
    # print r.text
    # return HttpResponse('<pre>' + r.text + '</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

