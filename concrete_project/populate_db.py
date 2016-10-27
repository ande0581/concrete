import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concrete_project.settings')

import django
django.setup()
from address.models import Address
from bid.models import Bid
from customer.models import Customer
from item.models import BidItem
from journal.models import Journal
from service.models import Service


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    customer_records = [
        {'name': 'Jeff Johnson', 'email': 'jeff@domain.com', 'telephone': '7635551000', 'pk': 1},
        {'name': 'Tom Olsen', 'email': 'concrete@mybiz.com', 'telephone': '6125551000', 'pk': 2}
    ]

    address_records = [
        {'street': '123 washington ave', 'city': 'duluth', 'state': 'mn', 'zip': '55111', 'customer_id': 1},
        {'street': '456 delaware lane', 'city': 'clearwater', 'state': 'mn', 'zip': '55111', 'customer_id': 2}
    ]

    journal_records = [
        {'body': 'Call customer to follow up on scheduling', 'timestamp': '2016-02-29 10:42:52.509000',
         'customer_id': 1},
        {'body': 'Call customer setup time to seal driveway', 'timestamp': '2016-03-09 11:21:38.934000',
         'customer_id': 2}
    ]

    service_records = [
        {'description': '.5 inch rebar', 'cost': 5.60},
        {'description': 'standard gray concrete', 'cost': 3.25}
    ]

    bid_records = [
        {'description': 'pour new driveway and apron', 'notes': 'no smoking on property', 'customer_id': 1,
         'address_id': 1},
        {'description': 'garage floor 40x60', 'notes': 'use hurricane straps', 'customer_id': 2,
         'address_id': 2},
    ]

    biditem_records = [
        {'bid_id': 1, 'service_id': 1, 'description': '.5 inch rebar', 'cost': 5.60, 'quantity': 15, 'total': 84},
        {'bid_id': 1, 'service_id': 2, 'description': 'standard gray concrete', 'cost': 3.25, 'quantity': 200,
         'total': 650},
        {'bid_id': 2, 'service_id': 1, 'description': '.5 inch rebar', 'cost': 5.60, 'quantity': 10, 'total': 56},
        {'bid_id': 2, 'service_id': 2, 'description': 'standard gray concrete', 'cost': 3.25, 'quantity': 100,
         'total': 325}
    ]

    for record in customer_records:
       add_customer(record)

    for record in address_records:
        add_address(record)


def add_customer(cust_entry):
    print(cust_entry)
    cus_obj = Customer.objects.get_or_create(**cust_entry)[0]
    cus_obj.save()
    return cus_obj


def add_address(addr_entry):
    print(addr_entry)
    cus_obj = Customer.objects.get(pk=addr_entry['customer_id'])
    addr_entry['customer_id'] = cus_obj
    addr_obj = Address.objects.get_or_create(**addr_entry)[0]
    addr_obj.save()
    return addr_obj


"""
    def add_page(cat, title, url, views=0):
        p = Page.objects.get_or_create(category=cat, title=title)[0]
        p.url = url
        p.views = views
        p.save()
        return p
"""

"""
41
42     # If you want to add more catergories or pages,
43     # add them to the dictionaries above.
44
45     # The code below goes through the cats dictionary, then adds each category,
46     # and then adds all the associated pages for that category.
47     # if you are using Python 2.x then use cats.iteritems() see
48     # http://docs.quantifiedcode.com/python-anti-patterns/readability/
49     # for more information about how to iterate over a dictionary properly.
50
51     for cat, cat_data in cats.items():
52         c = add_cat(cat)
53         for p in cat_data["pages"]:
54             add_page(c, p["title"], p["url"])
55
56     # Print out the categories we have added.
57     for c in Category.objects.all():
58         for p in Page.objects.filter(category=c):
59             print("- {0} - {1}".format(str(c), str(p)))
60
61 def add_page(cat, title, url, views=0):
62     p = Page.objects.get_or_create(category=cat, title=title)[0]
63     p.url=url
64     p.views=views
65     p.save()
66     return p
67
68 def add_cat(name):
69     c = Category.objects.get_or_create(name=name)[0]
70     c.save()
71     return c
72
"""


# Start execution here!
if __name__ == '__main__':
    print("Starting concrete project population script...")
    populate()