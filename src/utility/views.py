from django.http import HttpResponse


# Create your views here.
def email_website_folder(request):
    return HttpResponse('this is the email site to admin view')