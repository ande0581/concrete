import datetime
from django.http import HttpResponse
from django.templatetags.static import static
from django.utils.six import BytesIO
import os
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import cm
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak

from bid_item.models import BidItem


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
        self.drawRightString(200 * mm, 15 * mm + (0.2 * inch),
                             "Page {} of {}".format(self._pageNumber, page_count))


def generate_pdf(filename, obj):

    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename={}'.format(pdf_name)
    response['Content-Disposition'] = 'filename={}'.format(filename)

    buff = BytesIO()

    doc = SimpleDocTemplate(buff, rightMargin=.5 * cm, leftMargin=.5 * cm,
                            topMargin=.5 * cm, bottomMargin=1.5 * cm)

    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = Paragraph('This is a multi-line footer.  It goes on every page.   ' * 5, styles['Normal'])
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
    styles.add(ParagraphStyle(name='Line_Data_Largest', alignment=TA_LEFT, fontSize=14, leading=15))
    styles.add(ParagraphStyle(name='Line_Label', font='Helvetica-Bold', fontSize=7, leading=6, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Line_Label_Center', font='Helvetica-Bold', fontSize=7, alignment=TA_CENTER))


    # TODO figure out static diretory url
    # current_directory = os.path.dirname(os.path.realpath(__file__))
    # logo = os.path.join(current_directory, 'images/checked.png')

    logo = '/Users/janderson/PycharmProjects/concrete/src/static/img/logo.jpg'
    divider = 5
    image = Image(logo, width=800/divider, height=269/divider)

    # Add Company Info

    company_paragraph = """
        179 Marvy ST<br />
        Lino Lakes, MN 55014<br />
        (612) 508-2484 <br />
        concrete@madsenconcrete.com
        """

    invoice_paragraph = """
        Date: {date}<br />
        Invoice #: {invoice} <br />
    """.format(date=datetime.date.today(), invoice=obj.id)

    data1 = [[Paragraph(company_paragraph, styles['Line_Data']),
              image,
             Paragraph(invoice_paragraph, styles['Line_Data'])],
             [None, None, None]]

    #t1 = Table(data1, colWidths=(15 * cm, 4.6 * cm,))
    t1 = Table(data1)
    t1.setStyle(TableStyle([
        #('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
        #('BOX', (0, 0), (-1, -1), .25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    story.append(t1)
    story.append(Spacer(4, 32))

    # Add customer info to PDF

    telephone = obj.customer.telephone
    telephone = "({}) {}-{}".format(telephone[:3], telephone[3:6], telephone[6:])

    if obj.customer.company_name:
        company = "{}<br />".format(obj.customer.company_name)
    else:
        company = ""

    customer_paragraph = """
        {first} {last}<br />
        {company}
        {street}<br />
        {city}, {state} {zip}<br />
        {telephone}<br />
        {email}""".format(first=obj.customer.first_name, last=obj.customer.last_name, company=company,
                                          street=obj.address.street, city=obj.address.city, state=obj.address.state,
                                          zip=obj.address.zip, telephone=telephone, email=obj.customer.email)

    description_paragraph = obj.description

    data1 = [[Paragraph('To:', styles["Line_Label"]),
              Paragraph('Job Description:', styles["Line_Label"])],

             [Paragraph(customer_paragraph, styles["Line_Data_Large"]),
              Paragraph(description_paragraph, styles["Line_Data_Large"])]
             ]

    t1 = Table(data1)
    t1.setStyle(TableStyle([
        #('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
        #('INNERGRID', (0, 1), (1, 1), 0.25, colors.black),
        #('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    story.append(t1)


    #### Add Items to Bid

    story.append(Spacer(4, 32))
    data1 = [[Paragraph('Description', styles["Line_Data_Large"]),
              Paragraph('Total', styles["Line_Data_Large_Right"])]
             ]

    #print('Column Width', 1.7+1.3+2+7+1+1.5+1.5+1.8+1.8)  # 19.6cm

    t1 = Table(data1, colWidths=(16 * cm, 3.6 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 1.25, colors.green),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('BACKGROUND', (0, 0), (-1, -1), colors.green)
    ]))

    story.append(t1)

    items = BidItem.objects.all().filter(bid=obj.id)

    data1 = [[Paragraph(str(item.description), styles["Line_Data_Large"]),
              Paragraph(str(item.total), styles["Line_Data_Large_Right"])] for item in items]

    t1 = Table(data1, colWidths=(16 * cm, 3.6 * cm))
    t1.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(t1)

    #doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer, canvasmaker=NumberedCanvas)
    doc.build(story, canvasmaker=NumberedCanvas)
    response.write(buff.getvalue())
    buff.close()

    return response
