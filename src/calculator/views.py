from django.shortcuts import render


def index(request):
    return render(request, 'calculator/calculator_index.html', {})

