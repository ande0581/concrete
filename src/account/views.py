from django.contrib.auth import login, logout, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserLoginForm

User = get_user_model()


def login_view(request, *args, **kwargs):
    next_url = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username_ = form.cleaned_data.get('username')
        user_obj = User.objects.get(username__iexact=username_)
        login(request, user_obj)
        if next_url:
            return redirect(next_url)
        return HttpResponseRedirect(reverse('overview_app:overview_list'))
    return render(request, 'account/account_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


