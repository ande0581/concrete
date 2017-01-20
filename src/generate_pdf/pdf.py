# from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
# from reportlab.lib.units import inch
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import mm
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from django.conf import settings
# from reportlab.platypus import Table
# from reportlab.platypus import TableStyle

from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak


from bid_item.models import BidItem

# http://ericsaupe.com/reportlab-and-django-part-3-paragraphs-and-tables/
# https://pypi.python.org/pypi/PyInvoice/0.1.7
# https://github.com/katomaso/django-invoice ## looks nice
# https://github.com/marinho/geraldo
# https://github.com/matthiask/pdfdocument


# class NumberedCanvas(canvas.Canvas):
#     def __init__(self, *args, **kwargs):
#         canvas.Canvas.__init__(self, *args, **kwargs)
#         self._saved_page_states = []
#
#     def showPage(self):
#         self._saved_page_states.append(dict(self.__dict__))
#         self._startPage()
#
#     def save(self):
#         """add page info to each page (page x of y)"""
#         num_pages = len(self._saved_page_states)
#         for state in self._saved_page_states:
#             self.__dict__.update(state)
#             self.draw_page_number(num_pages)
#             canvas.Canvas.showPage(self)
#         canvas.Canvas.save(self)
#
#     def draw_page_number(self, page_count):
#         # Change the position of this to wherever you want the page number to be
#         self.drawRightString(211 * mm, 15 * mm + (0.2 * inch),
#                              "Page %d of %d" % (self._pageNumber, page_count))


class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    @staticmethod
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

    def print_users(self):

        file_path = 'fedex.pdf'
        buffer = self.buffer

        doc = SimpleDocTemplate(file_path, rightMargin=.5 * cm, leftMargin=.5 * cm,
                                topMargin=1.5 * cm, bottomMargin=1.5 * cm)

        story = []

        # Styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
        styles.add(ParagraphStyle(name='Line_Data', alignment=TA_LEFT, fontSize=8, leading=7))
        styles.add(ParagraphStyle(name='Line_Data_Small', alignment=TA_LEFT, fontSize=7, leading=8))
        styles.add(ParagraphStyle(name='Line_Data_Large', alignment=TA_LEFT, fontSize=12, leading=12))
        styles.add(ParagraphStyle(name='Line_Data_Largest', alignment=TA_LEFT, fontSize=14, leading=15))
        styles.add(ParagraphStyle(name='Line_Label', font='Helvetica-Bold', fontSize=7, leading=6, alignment=TA_LEFT))
        styles.add(ParagraphStyle(name='Line_Label_Center', font='Helvetica-Bold', fontSize=7, alignment=TA_CENTER))

        address_paragraph = \
            "Jeff Anderson<br />" \
            "670 Ironton ST NE <br />" \
            "Fridley, MN 55432<br />"

        company_paragraph = \
            "Tom Madsen<br />" \
            "179 Marvy ST<br />" \
            "Lino Lakes, MN 55014<br />"

        data1 = [[Paragraph('SHIPPER/EXPORTER (complete name and address)', styles["Line_Label"]),
                  Paragraph('CONSIGNEE (complete name and address)', styles["Line_Label"])],

                 [Paragraph(address_paragraph, styles["Line_Data_Large"]),
                  Paragraph(company_paragraph, styles["Line_Data_Large"])]
                 ]

        t1 = Table(data1)
        t1.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (1, 0), 0.25, colors.black),
            ('INNERGRID', (0, 1), (1, 1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        story.append(t1)

        doc.build(story)

        # # Get the value of the BytesIO buffer and write it to the response.
        # pdf = buffer.getvalue()
        # buffer.close()
        #
        # return pdf




        # def print_users(self):
    #
    #     # Register Fonts
    #     pdfmetrics.registerFont(TTFont('Arial', settings.STATIC_ROOT + '/fonts/arial.ttf'))
    #     pdfmetrics.registerFont(TTFont('Arial-Bold', settings.STATIC_ROOT + '/fonts/arialbd.ttf'))
    #
    #     # A large collection of style sheets pre-made for us
    #     styles = getSampleStyleSheet()
    #     # Our Custom Style
    #     styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))
    #
    #     buffer = self.buffer
    #     doc = SimpleDocTemplate(buffer,
    #                             rightMargin=72,
    #                             leftMargin=72,
    #                             topMargin=120,
    #                             bottomMargin=72,
    #                             pagesize=self.pagesize)
    #
    #     # Our container for 'Flowable' objects
    #     elements = []
    #
    #     # A large collection of style sheets pre-made for us
    #     styles = getSampleStyleSheet()
    #     styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', alignment=TA_RIGHT))
    #
    #     # Jeff Tests
    #     styles.add(ParagraphStyle(name='LeftAlign', fontName='Arial', alignment=TA_LEFT))
    #     elements.append(Paragraph('Customer Address', styles['LeftAlign']))
    #     elements.append(Paragraph('Project Overview', styles['RightAlign']))
    #     cus_address = "670 Ironton ST NE\nFridley, MN 55432"
    #
    #     address_table = Table(cus_address, colWidths=[doc.width / 3.0] * 3)
    #     address_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #                                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
    #     elements.append(address_table)
    #
    #     # Draw things on the PDF. Here's where the PDF generation happens.
    #     # See the ReportLab documentation for the full list of functionality.
    #     items = BidItem.objects.all()
    #     elements.append(Paragraph('Description', styles['RightAlign']))
    #
    #     # Need a place to store our table rows
    #     table_data = []
    #     for i, item in enumerate(items):
    #         # Add a row to the table
    #         table_data.append([item.description, item.quantity, item.total])
    #
    #     # Create the table
    #     user_table = Table(table_data, colWidths=[doc.width / 3.0] * 3)
    #     user_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #                                     ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
    #     elements.append(user_table)
    #     doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer,
    #               canvasmaker=NumberedCanvas)
    #
    #     # Get the value of the BytesIO buffer and write it to the response.
    #     pdf = buffer.getvalue()
    #     buffer.close()
    #
    #     return pdf