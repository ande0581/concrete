import datetime
from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.six import BytesIO
import os
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import cm
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import KeepTogether
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

from bid_item.models import BidItem
from pdf.models import PDFImage


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(115 * mm, 25 * mm + (0.2 * inch),
                             "Page {} of {}".format(self._pageNumber, page_count))


def generate_pdf(request, obj, bid_item_dict, invoice, save_to_disk=False):
    buff = BytesIO()

    # The page width totals 18.6cm
    doc = SimpleDocTemplate(buff, rightMargin=2 * cm, leftMargin=2 * cm,
                            topMargin=1.5 * cm, bottomMargin=3.75 * cm)

    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = Paragraph('Thank You For Your Business', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()

    story = []

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Data', alignment=TA_LEFT, fontSize=8, leading=7))
    styles.add(ParagraphStyle(name='Line_Data_Small', alignment=TA_LEFT, fontSize=7, leading=8))
    styles.add(ParagraphStyle(name='Line_Data_Medium', alignment=TA_LEFT, fontSize=10, leading=8))
    styles.add(ParagraphStyle(name='Line_Data_Large', alignment=TA_LEFT, fontSize=12, leading=12))
    styles.add(ParagraphStyle(name='Line_Data_Large_Right', alignment=TA_RIGHT, fontSize=12, leading=12))
    styles.add(ParagraphStyle(name='Invoice_Date', alignment=TA_LEFT, fontSize=12, leading=12))
    styles.add(ParagraphStyle(name='Line_Data_Largest', fontName='Times-BoldItalic', alignment=TA_CENTER, fontSize=22, leading=15))
    styles.add(ParagraphStyle(name='Line_Label', fontSize=10, leading=12, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Label_Center', fontSize=7, alignment=TA_CENTER))

    # Add Company Address, Logo and Invoice Info
    company_paragraph = """
        179 Marvy ST<br />
        Lino Lakes, MN 55014<br />
        (612) 508-2484 <br />
        concrete@madsenconcrete.com <br />
        MN License: BC690748
        """

    logo = os.path.join(settings.STATIC_ROOT, 'img/logo.jpg')
    denominator = 5
    image = Image(logo, width=800 / denominator, height=269 / denominator)

    if invoice:
        proposal_invoice_paragraph = """
            Date: {}<br />
            Invoice #: {:04d} <br />
        """.format(datetime.date.today(), obj.id)
    else:
        proposal_invoice_paragraph = """
            Submitted By: <br />
            Tom Madsen <br />
            Date: {}<br />
            Proposal #: {:04d} <br />
        """.format(datetime.date.today(), obj.id)

    data1 = [[Paragraph(company_paragraph, styles['Line_Data_Large']),
              image,
              Paragraph(proposal_invoice_paragraph, styles['Line_Data_Large'])]]

    t1 = Table(data1, colWidths=(6 * cm, 8 * cm, 4.6 * cm))
    t1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    story.append(t1)

    # Add Proposal or Invoice Title to PDF
    if invoice:
        pdf_type = 'Invoice'
    else:
        pdf_type = 'Proposal'

    data1 = [[Paragraph(pdf_type, styles["Line_Data_Largest"])]]

    t1 = Table(data1, colWidths=(18.6 * cm))
    t1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))

    story.append(t1)
    story.append(Spacer(2, 32))

    # Add Customer Info and Job Description
    telephone = obj.customer.telephone
    telephone = "({}) {}-{}".format(telephone[:3], telephone[3:6], telephone[6:])

    if obj.customer.company_name:
        company = "{}<br />".format(obj.customer.company_name)
    else:
        company = ""

    location_paragraph = """
        {first} {last}<br />
        {company}
        {street}<br />
        {city}, {state} {zip}<br />
        {telephone}<br />
        {email}""".format(first=obj.customer.first_name, last=obj.customer.last_name, company=company,
                          street=obj.address.street, city=obj.address.city, state=obj.address.state,
                          zip=obj.address.zip, telephone=telephone, email=obj.customer.email)

    if invoice:
        if len(obj.billto_telephone) == 10:
            billto_telephone = obj.billto_telephone
            billto_telephone = "({}) {}-{}".format(billto_telephone[:3], billto_telephone[3:6], billto_telephone[6:])

        billto_paragraph = """
        {name}<br />
        {street}<br />
        {city_st_zip}<br />
        {telephone}""".format(name=obj.billto_name,
                              street=obj.billto_street,
                              city_st_zip=obj.billto_city_st_zip,
                              telephone=billto_telephone)
    else:
        billto_paragraph = location_paragraph

    description_paragraph = obj.description

    if invoice:
        data1 = [[Paragraph('Bill To Address', styles["Line_Data_Large"]),
                  Paragraph('Job Address', styles["Line_Data_Large"])],

                 [Paragraph(billto_paragraph, styles["Line_Data_Large"]),
                  Paragraph(location_paragraph, styles["Line_Data_Large"])]
                 ]

        t1 = Table(data1)
        t1.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey)
        ]))

        story.append(t1)
        story.append(Spacer(4, 20))

        data1 = [[Paragraph('Job Description', styles["Line_Data_Large"])],
                 [Paragraph(description_paragraph, styles["Line_Data_Large"])]]

        t1 = Table(data1)
        t1.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey)
        ]))

        story.append(t1)

    else:

        data1 = [[Paragraph('Job Address', styles["Line_Data_Large"]),
                  Paragraph('Job Description', styles["Line_Data_Large"])],

                 [Paragraph(billto_paragraph, styles["Line_Data_Large"]),
                  Paragraph(description_paragraph, styles["Line_Data_Large"])]
                 ]

        t1 = Table(data1, colWidths=(7 * cm, 11.6 * cm))
        t1.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey)
        ]))

        story.append(t1)

    # Add Bid Items to PDF
    story.append(Spacer(4, 32))

    for job_name, items in bid_item_dict.items():
        title = [[Paragraph(job_name, styles["Line_Data_Large"]),
                  Paragraph('', styles["Line_Data_Large"])]
                 ]

        t1 = Table(title, colWidths=(15 * cm, 3.6 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), .25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey)
        ]))

        story.append(t1)

        data1 = [[Paragraph(str(item.description), styles["Line_Data_Large"]),
                  Paragraph(str("{0:.2f}".format(round(item.total, 2))), styles["Line_Data_Large_Right"])] for item in
                 items]

        t1 = Table(data1, colWidths=(15 * cm, 3.6 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        story.append(t1)

        # Calculate total per job and add to PDF
        total = items.aggregate(Sum('total'))['total__sum']
        data1 = [[Paragraph('Total', styles["Line_Data_Large"]),
                  Paragraph(str("${0:.2f}".format(total)), styles['Line_Data_Large_Right'])]
                 ]

        t1 = Table(data1, colWidths=(15 * cm, 3.6 * cm))
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), .25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey)
        ]))

        story.append(t1)
        story.append(Spacer(4, 12))

    # Calculate Bid Total
    items = BidItem.objects.all().filter(bid=obj.id)
    bid_total = items.aggregate(Sum('total'))['total__sum']

    # We Propose Section
    if not invoice:

        if obj.custom_down_payment:
            down_payment = obj.custom_down_payment
            final_payment = bid_total - down_payment
        else:
            down_payment = bid_total / 2
            final_payment = bid_total - down_payment

        we_propose = 'Hereby to furnish material and labor complete in accordance with above specifications,' \
                     ' for the sum of'

        acceptance = """The above prices, specifications and conditions are satisfactory and are hereby accepted.
        You are authorized to do the work as specified. Payment will be made as outlined above.
        I have received a copy of the Pre-Lien notice."""

        data1 = [
            [Paragraph('We Propose', styles["Line_Data_Large"]),
             None],
            [Paragraph(we_propose, styles["Line_Data_Large"]),
             Paragraph(str("${0:.2f}".format(round(bid_total, 2))), styles["Line_Data_Large_Right"])],
            [Paragraph('Payment Outline', styles["Line_Data_Large"]),
             None],
            [Paragraph('Deposit', styles["Line_Data_Large"]),
             Paragraph(str("${0:.2f}".format(round(down_payment, 2))), styles["Line_Data_Large_Right"])],
            [Paragraph('Remaining Balance Due Upon Completion of the Contract', styles["Line_Data_Large"]),
             Paragraph(str("${0:.2f}".format(round(final_payment, 2))), styles["Line_Data_Large_Right"])],
            [Paragraph('Acceptance of Proposal', styles["Line_Data_Large"]),
             None],
            [Paragraph(acceptance, styles["Line_Data_Large"]),
             None],
            [Paragraph('Signature:', styles["Line_Label"]),
             Paragraph('Date:', styles["Line_Label"])],
            [Paragraph('X__________________________________________________________________', styles["Line_Label"]),
             Paragraph('_____________________', styles["Line_Label"])],
        ]

        t1 = Table(data1, colWidths=(14 * cm, 4.6 * cm))
        t1.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), .25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # we propose
            ('BACKGROUND', (0, 2), (-1, 2), colors.lightgrey),  # payment outline
            ('BACKGROUND', (0, 5), (-1, 5), colors.lightgrey),  # acceptance of proposal
            ('SPAN', (0, 6), (-1, 6)),  # span acceptance text across both columns
            ('BOTTOMPADDING', (0, 7), (-1, 7), 40)
        ]))

        story.append(KeepTogether(t1))




    # Add Grand Total to PDF
    # items = BidItem.objects.all().filter(bid=obj.id)
    # total = items.aggregate(Sum('total'))['total__sum']
    # data1 = [[Paragraph('Grand Total', styles["Line_Data_Large"]),
    #           Paragraph(str("${0:.2f}".format(total)), styles['Line_Data_Large_Right'])]
    #          ]
    #
    # t1 = Table(data1, colWidths=(16 * cm, 3.6 * cm))
    # t1.setStyle(TableStyle([
    #     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #     ('BOX', (0, 0), (-1, -1), .25, colors.black),
    #     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    #     ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey)
    # ]))
    #
    # story.append(t1)

    # doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer, canvasmaker=NumberedCanvas)
    doc.build(story, canvasmaker=NumberedCanvas)

    pdf = buff.getvalue()
    buff.close()

    if save_to_disk:
        myfile = ContentFile(pdf)
        db_model = PDFImage()
        db_model.bid = obj
        db_model.filename.save('', myfile)
        messages.success(request, "PDF was saved successfully!")
        return redirect('bid_app:bid_update', pk=obj.id)

    filename = obj.customer.__str__().replace(' ', '_').lower()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename={}.pdf'.format(filename)
    response.write(pdf)

    return response
