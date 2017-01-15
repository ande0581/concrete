import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concrete_project.settings')

import django
django.setup()
from category.models import Category
from service.models import Service


def populate():

    category_records = [
        {'name': 'Concrete'},
        {'name': 'Control-Joint'},
        {'name': 'Drain-Tile'},
        {'name': 'Expansion-Felt'},
        {'name': 'Fasteners'},
        {'name': 'Fill'},
        {'name': 'Forming'},
        {'name': 'Flashing'},
        {'name': 'Permits'},
        {'name': 'Railing'},
        {'name': 'Rebar'},
        {'name': 'Removal-Per-Load'},
        {'name': 'Removal-Square-Foot'},
        {'name': 'Rock'},
        {'name': 'Saw-Cutting'},
        {'name': 'Sealer'},
        {'name': 'Soil'},
        {'name': 'Stamps'},
        {'name': 'Short-Load'},
        {'name': 'Steps'},
        {'name': 'Washout'},
        {'name': 'Window'},
        {'name': 'Window-Well'},
        {'name': 'Wood'}
    ]

    service_records = [
        # TODO Landscape??
        {'description': '10-ton Class 5 Fill', 'cost': 400, 'category': 'Fill', 'measurement': 'each'},
        {'description': '5-ton Class 5 Fill', 'cost': 225, 'category': 'Fill', 'measurement': 'each'},
        {'description': '5 Yards Black Dirt Soil', 'cost': 450, 'category': 'Soil', 'measurement': 'each'},
        {'description': 'Concrete Driveway Mix', 'cost': 100, 'category': 'Concrete', 'measurement': 'cubic_yard'},
        {'description': 'Concrete Exposed', 'cost': 120, 'category': 'Concrete', 'measurement': 'cubic_yard'},
        {'description': 'Concrete Colored $', 'cost': 150, 'category': 'Concrete', 'measurement': 'cubic_yard'},
        {'description': 'Concrete Colored $$', 'cost': 175, 'category': 'Concrete', 'measurement': 'cubic_yard'},
        {'description': 'Concrete Colored $$$', 'cost': 200, 'category': 'Concrete', 'measurement': 'cubic_yard'},
        {'description': 'Concrete Stamps', 'cost': 215, 'category': 'Stamps', 'measurement': 'each'},
        {'description': 'Concrete Truck Washout Fee', 'cost': 60, 'category': 'Washout', 'measurement': 'each'},
        {'description': 'Drain Tile Socked', 'cost': 60, 'category': 'Drain-Tile', 'measurement': 'linear_foot'},
        {'description': 'Expansion Felt', 'cost': 1.0, 'category': 'Expansion-Felt', 'measurement': 'linear_foot'},
        {'description': 'Forming, Grading and Setup', 'cost': .73, 'category': 'Forming', 'measurement': 'square_foot'},
        {'description': 'Minimum Load Charge', 'cost': 120, 'category': 'Short-Load', 'measurement': 'each'},
        {'description': 'Pour, Finish, Control Joints', 'cost': .78, 'category': 'Control-Joint', 'measurement': 'square_foot'},
        {'description': 'Pour, Finish, Control Joints Colored/Stamped', 'cost': 1.75, 'category': 'Control-Joint', 'measurement': 'square_foot'},
        {'description': 'Railing Painted', 'cost': 70, 'category': 'Railing', 'measurement': 'linear_foot'},
        {'description': 'Railing Powder Coated', 'cost': 90, 'category': 'Railing', 'measurement': 'linear_foot'},
        {'description': 'Rebar 1/2 Non-Coated', 'cost': .84, 'category': 'Rebar', 'measurement': 'square_foot'},
        {'description': 'Rebar 1/2 Coated', 'cost': .71, 'category': 'Rebar', 'measurement': 'square_foot'},
        {'description': 'Rebar 3/8 Non-Coated', 'cost': .64, 'category': 'Rebar', 'measurement': 'square_foot'},
        {'description': 'Rebar 3/8 Coated', 'cost': .77, 'category': 'Rebar', 'measurement': 'square_foot'},
        {'description': 'Removal - Dirt/Gravel/Sod', 'cost': .6, 'category': 'Removal-Square-Foot', 'measurement': 'square_foot'},
        {'description': 'Removal - Clay', 'cost': 1.4, 'category': 'Removal-Square-Foot', 'measurement': 'square_foot'},
        {'description': 'Removal - Concrete/Tar', 'cost': .9, 'category': 'Removal-Square-Foot', 'measurement': 'square_foot'},
        {'description': 'Removal - Clay Per Load', 'cost': 650, 'category': 'Removal-Per-Load', 'measurement': 'each'},
        {'description': 'Removal - Concrete/Tar Per Load', 'cost': 450, 'category': 'Removal-Per-Load', 'measurement': 'each'},
        {'description': 'Removal - Dirt/Gravel/Sod Per Load', 'cost': 300, 'category': 'Removal-Per-Load', 'measurement': 'each'},
        {'description': 'Saw Cutting', 'cost': 5, 'category': 'Saw-Cutting', 'measurement': 'linear_foot'},
        {'description': 'Sealer - Cure n Seal', 'cost': .53, 'category': 'Sealer', 'measurement': 'square_foot'},
        {'description': 'Sealer - Lumiseal Plus', 'cost': .8, 'category': 'Sealer', 'measurement': 'square_foot'},
        {'description': 'Steps', 'cost': 500, 'category': 'Steps', 'measurement': 'each'},
        {'description': 'Egress Window AAxBB', 'cost': 1400, 'category': 'Window', 'measurement': 'each'},
        {'description': 'Fasteners', 'cost': 20, 'category': 'Fasteners', 'measurement': 'each'},
        {'description': 'Flashing', 'cost': 25, 'category': 'Flashing', 'measurement': 'each'},
        {'description': 'Egress Window Building Permit', 'cost': 120, 'category': 'Permits', 'measurement': 'each'},
        {'description': 'Rock for Window Well', 'cost': 25, 'category': 'Rock', 'measurement': 'each'},
        {'description': 'Egress Window Well Option A', 'cost': 250, 'category': 'Window-Well', 'measurement': 'each'},
        {'description': 'Egress Window Well Option B', 'cost': 300, 'category': 'Window-Well', 'measurement': 'each'},
        {'description': 'Pressure Treated Wood', 'cost': 30, 'category': 'Wood', 'measurement': 'each'},


    ]

    for record in category_records:
        add_category(record)

    for record in service_records:
        add_service(record)


def add_category(category_entry):
    print('Category:', category_entry['name'])
    item = Category(**category_entry)
    item.save()


def add_service(service_entry):
    print('Service:', service_entry['description'])
    category_obj = Category.objects.get(name=service_entry['category'])
    service_entry['category'] = category_obj
    item = Service(**service_entry)
    item.save()


if __name__ == '__main__':
    print("Starting concrete services population script...")
    populate()
