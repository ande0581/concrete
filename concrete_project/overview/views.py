from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context_dict = {'boldmessage': 'Crunch, creamy, cookie, candy, cupcake'}
    return render(request, 'overview/index.html', context=context_dict)

