from django.shortcuts import render


def index(request):
    return render(request, 'bid/bid_index.html', {})

