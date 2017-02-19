import datetime
from decimal import Decimal, ROUND_HALF_UP
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
from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

from bid_item.models import BidItem
from payment.models import Payment
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


def generate_pdf(request, obj, bid_item_dict, invoice, employee, save_to_disk=False, return_file_object=False):
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
    styles.add(ParagraphStyle(name='Line_Data_Large_Center', alignment=TA_CENTER, fontSize=12, leading=12))
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
        """.format(datetime.date.today().strftime('%x'), obj.id)
    else:
        proposal_invoice_paragraph = """
            Submitted By: <br />
            Tom Madsen <br />
            Date: {}<br />
            Proposal #: {:04d} <br />
        """.format(datetime.date.today().strftime('%x'), obj.id)

    data1 = [[Paragraph(company_paragraph, styles['Line_Data_Large']),
              image,
              Paragraph(proposal_invoice_paragraph, styles['Line_Data_Large'])]]

    t1 = Table(data1, colWidths=(6.7 * cm, 8 * cm, 4.6 * cm))
    t1.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    story.append(t1)

    # Add Proposal or Invoice Title to PDF
    if invoice:
        pdf_type = 'Invoice'
    elif employee:
        pdf_type = 'Employee Copy'
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

    if obj.billto_city_st_zip:  # check if this is an alternate billto field populated
        if len(obj.billto_telephone) == 10:
            billto_telephone = obj.billto_telephone
            billto_telephone = "({}) {}-{}".format(billto_telephone[:3], billto_telephone[3:6], billto_telephone[6:])
        else:
            billto_telephone = obj.billto_telephone

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
        data1 = [[Paragraph('Bill To', styles["Line_Data_Large"]),
                  Paragraph('Job Address', styles["Line_Data_Large"])],

                 [Paragraph(billto_paragraph, styles["Line_Data_Large"]),
                  Paragraph(location_paragraph, styles["Line_Data_Large"])]
                 ]

        t1 = Table(data1, colWidths=(9.3 * cm, 9.3 * cm))
        t1.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey)
        ]))

        story.append(t1)
        story.append(Spacer(4, 20))

        data1 = [[Paragraph('Job Description', styles["Line_Data_Large"])],
                 [Paragraph(description_paragraph, styles["Line_Data_Large"])]]

        t1 = Table(data1, colWidths=(18.6 * cm))
        t1.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey)
        ]))

        story.append(t1)

    else:  # Proposal

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

        if obj.notes:
            story.append(Spacer(2, 10))
            data1 = [[Paragraph('Notes', styles["Line_Data_Large"])],
                     [Paragraph(obj.notes, styles["Line_Data_Large"])]]

            t1 = Table(data1, colWidths=(18.6 * cm))
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

        if employee:  # Add quantities but remove pricing
            data1 = [[Paragraph(str(item.description), styles["Line_Data_Large"]),
                      Paragraph(str(item.quantity), styles["Line_Data_Large_Right"])] for item in
                     items]

            t1 = Table(data1, colWidths=(15 * cm, 3.6 * cm))
            t1.setStyle(TableStyle([
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            story.append(t1)
            story.append(Spacer(4, 32))

        else:  # Add pricing but not quantity for end customer
            data1 = [[Paragraph(str(item.description), styles["Line_Data_Large"]),
                      Paragraph(str("{0:.2f}".format(round(item.total, 2))), styles["Line_Data_Large_Right"])] for item
                     in
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
            total_text = "{} Total".format(job_name)
            data1 = [[Paragraph(total_text, styles["Line_Data_Large"]),
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
            story.append(Spacer(4, 32))

    # Calculate Bid Total
    items = BidItem.objects.all().filter(bid=obj.id)
    bid_total = items.aggregate(Sum('total'))['total__sum']

    if not bid_total:
        bid_total = 0

    if invoice:  # Calculate Balance Due and Payment History for Invoice
        payments = Payment.objects.all().filter(bid=obj.id)
        payment_total = payments.aggregate(Sum('amount'))['amount__sum']

        cents = Decimal('0.01')
        if payment_total:
            remaining_balance = Decimal(bid_total - payment_total).quantize(cents, ROUND_HALF_UP)
        else:
            remaining_balance = bid_total

        data1 = [
            [Paragraph('Invoice Summary', styles["Line_Data_Large"]),
             None],
            [Paragraph('Initial Balance', styles["Line_Data_Large"]),
             Paragraph(str("{0:.2f}".format(round(bid_total, 2))), styles["Line_Data_Large_Right"])],
        ]

        data2 = [[Paragraph(str("Received Payment on {}".format(payment.date.strftime('%x'))),
                            styles["Line_Data_Large"]),
                  Paragraph(str("-{0:.2f}".format(round(payment.amount, 2))), styles["Line_Data_Large_Right"])] for
                 payment in payments]

        last_row = len(data2) + 2

        data3 = [[Paragraph('Remaining Balance Due', styles["Line_Data_Large"]),
                 Paragraph(str("${0:.2f}".format(round(remaining_balance, 2))),
                           styles["Line_Data_Large_Right"])]]

        all_data = data1 + data2 + data3

        t1 = Table(all_data, colWidths=(14 * cm, 4.6 * cm))
        t1.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), .25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # we propose
            ('BACKGROUND', (0, last_row), (-1, last_row), colors.lightgrey),  # payment outline
        ]))

        story.append(KeepTogether(t1))

    elif employee:  # If employee skip rest of bid info
        pass

    else:  # Proposal

        if obj.custom_down_payment and obj.custom_down_payment != -1:
            down_payment = obj.custom_down_payment
        elif obj.custom_down_payment == -1:
            down_payment = 0
        else:
            if bid_total:
                down_payment = bid_total / 2
            else:
                down_payment = 0

        if bid_total:
            cents = Decimal('0.01')
            final_payment = Decimal(bid_total - down_payment).quantize(cents, ROUND_HALF_UP)
        else:
            final_payment = 0

        if not bid_total:
            bid_total = 0

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

        # Add Pre-Lien Notice to PDF
        story.append(PageBreak())

        pre_lien_notice = """
        <br />
        ANY PERSON OR COMPANY SUPPLYING LABOR OR MATERIALS FOR THIS IMPROVEMENT TO YOUR PROPERTY MAY FILE A LIEN
        AGAINST YOUR PROPERTY IF THAT PERSON OR COMPANY IS NOT PAID FOR THE CONTRIBUTIONS.<br /><br />

        UNDER MINNESOTA LAW, YOU HAVE THE RIGHT TO PAY PERSONS WHO SUPPLIED LABOR OR MATERIALS FOR THIS IMPROVEMENT
         DIRECTLY AND DEDUCT THIS AMOUNT FROM OUR CONTRACT PRICE, OR WITHHOLD THE AMOUNTS DUE THEM FROM US UNTIL
         120 DAYS AFTER COMPLETION OF THE IMPROVEMENT UNLESS WE GIVE YOU A LIEN WAIVER SIGNED BY PERSONS WHO SUPPLIED
         ANY LABOR OR MATERIAL FOR THE IMPROVEMENT AND WHO GAVE YOU TIMELY NOTICE.
        """

        data1 = [
            [Paragraph('PRE-LIEN NOTICE', styles["Line_Data_Large_Center"])],
            [Paragraph(pre_lien_notice, styles["Line_Data_Large"])]
            ]

        t1 = Table(data1)
        story.append(t1)

    # doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer, canvasmaker=NumberedCanvas)
    doc.build(story, canvasmaker=NumberedCanvas)

    pdf = buff.getvalue()
    buff.close()

    if return_file_object:
        # For send pdf to employee which isnt stored to database, return the file object
        return pdf

    if save_to_disk:
        myfile = ContentFile(pdf)
        db_model = PDFImage()
        db_model.bid = obj
        if invoice:
            filename_temp = 'invoice'
        else:
            filename_temp = 'proposal'

        db_model.filename.save(filename_temp, myfile)
        messages.success(request, "PDF was saved successfully!")
        return redirect('bid_app:bid_detail', pk=obj.id)

    if invoice:
        filename = "{}_invoice_{}".format(obj.customer.__str__().replace(' ', '_').lower(), datetime.date.today())
    else:
        filename = "{}_proposal_{}".format(obj.customer.__str__().replace(' ', '_').lower(), datetime.date.today())
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename={}.pdf'.format(filename)
    response.write(pdf)

    return response
