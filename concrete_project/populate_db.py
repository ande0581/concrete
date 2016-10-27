import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concrete_project.settings')

import django
django.setup()
from django.utils import timezone
from address.models import Address
from bid.models import Bid
from customer.models import Customer
from item.models import BidItem
from journal.models import Journal
from service.models import Service


def populate():
    print("Current Time with TZ:", timezone.now(),)

    customer_records = [
        {'name': 'Jeff Johnson', 'email': 'jeff@domain.com', 'telephone': '7635551000', 'pk': 1},
        {'name': 'Tom Olsen', 'email': 'concrete@mybiz.com', 'telephone': '6125551000', 'pk': 2}
    ]

    address_records = [
        {'street': '123 washington ave', 'city': 'duluth', 'state': 'mn', 'zip': '55111', 'customer_id': 1, 'pk': 1},
        {'street': '456 delaware lane', 'city': 'clearwater', 'state': 'mn', 'zip': '55111', 'customer_id': 2, 'pk': 2}
    ]

    journal_records = [
        {'body': 'Call customer to follow up on scheduling', 'timestamp': timezone.now(),
         'customer_id': 1, 'pk': 1},
        {'body': 'Call customer setup time to seal driveway', 'timestamp': timezone.now(),
         'customer_id': 2, 'pk': 2}
    ]

    service_records = [
        {'description': '.5 inch rebar', 'cost': 5.60},
        {'description': 'standard gray concrete', 'cost': 3.25}
    ]

    bid_records = [
        {'description': 'pour new driveway and apron', 'notes': 'no smoking on property', 'customer_id': 1,
         'address_id': 1, 'timestamp': timezone.now(), 'pk': 1},
        {'description': 'garage floor 40x60', 'notes': 'use hurricane straps', 'customer_id': 2,
         'address_id': 2, 'timestamp': timezone.now(), 'pk': 2}
    ]

    bid_item_records = [
        {'bid_id': 1, 'description': '.5 inch rebar', 'cost': 5.60, 'quantity': 15, 'total': 84},
        {'bid_id': 1, 'description': 'standard gray concrete', 'cost': 3.25, 'quantity': 200,
         'total': 650},
        {'bid_id': 2, 'description': '.5 inch rebar', 'cost': 5.60, 'quantity': 10, 'total': 56},
        {'bid_id': 2, 'description': 'standard gray concrete', 'cost': 3.25, 'quantity': 100,
         'total': 325}
    ]

    for record in customer_records:
       add_customer(record)

    for record in address_records:
        add_address(record)

    for record in journal_records:
        add_journal(record)

    for record in service_records:
        add_service(record)

    for record in bid_records:
        add_bid(record)

    for record in bid_item_records:
        add_bid_item(record)


def add_customer(cust_entry):
    print("Customer:", cust_entry)
    cus_obj = Customer.objects.get_or_create(**cust_entry)[0]
    cus_obj.save()
    return cus_obj


def add_address(addr_entry):
    print("Address:", addr_entry)
    cus_obj = Customer.objects.get(pk=addr_entry['customer_id'])
    addr_entry['customer_id'] = cus_obj
    addr_obj = Address.objects.get_or_create(**addr_entry)[0]
    addr_obj.save()
    return addr_obj


def add_journal(journal_entry):
    print("Journal:", journal_entry)
    cus_obj = Customer.objects.get(pk=journal_entry['customer_id'])
    journal_entry['customer_id'] = cus_obj
    journal_obj = Journal.objects.get_or_create(**journal_entry)[0]
    journal_obj.save()
    return journal_obj


def add_service(service_entry):
    print("Service:", service_entry)
    service_obj = Service.objects.get_or_create(**service_entry)[0]
    service_obj.save()
    return service_obj


def add_bid(bid_entry):
    print("Bid:", bid_entry)
    addr_obj = Address.objects.get(pk=bid_entry['address_id'])
    cus_obj = Customer.objects.get(pk=bid_entry['customer_id'])
    bid_entry['address_id'] = addr_obj
    bid_entry['customer_id'] = cus_obj
    bid_obj = Bid.objects.get_or_create(**bid_entry)[0]
    bid_obj.save()
    return bid_obj


def add_bid_item(bid_item_entry):
    print("Bid Item:", bid_item_entry)
    bid_obj = Bid.objects.get(pk=bid_item_entry['bid_id'])
    bid_item_entry['bid_id'] = bid_obj
    bid_item_obj = BidItem.objects.get_or_create(**bid_item_entry)[0]
    bid_item_obj.save()
    return bid_item_obj


# Start execution here!
if __name__ == '__main__':
    print("Starting concrete project population script...")
    populate()