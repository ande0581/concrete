from pdf.pdf_template import generate_pdf
from bid.models import Bid


def create_pdf(request, **kwargs):

    obj = Bid.objects.get(pk=kwargs['bid_id'])

    # TODO file naming convention
    filename = 'magic.pdf'

    response = generate_pdf(filename=filename, obj=obj)
    return response
