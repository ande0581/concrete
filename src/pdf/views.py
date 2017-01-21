from pdf.pdf_template import generate_pdf


def create_pdf(request, **kwargs):

    filename = 'magic.pdf'
    response = generate_pdf(filename)
    return response
