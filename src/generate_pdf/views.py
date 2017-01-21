from generate_pdf.pdf import generate_commercial_invoice


def create_pdf(request):

    filename = 'magic.pdf'

    response = generate_commercial_invoice(filename)

    return response
