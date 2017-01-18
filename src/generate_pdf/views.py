from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# https://www.davidfischer.name/2015/08/generating-pdfs-with-and-without-python/
# http://ericsaupe.com/reportlab-and-django-part-1-the-set-up-and-a-basic-example/


from generate_pdf.pdf import MyPrint
from io import BytesIO


def print_users(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="My Users.pdf"'

    buffer = BytesIO()

    report = MyPrint(buffer, 'Letter')
    pdf = report.print_users()

    response.write(pdf)
    return response