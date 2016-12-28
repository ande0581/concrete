from django.shortcuts import render


def index(request):
    return render(request, 'bid/index.html', {})

