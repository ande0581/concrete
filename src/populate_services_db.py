import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concrete_project.settings')

import django
django.setup()
from category.models import Category
from job_type.models import JobType
from service.models import Service


def populate():

    category_records = [
        {'name': 'Concrete'},
        {'name': 'Drain-Tile'},
        {'name': 'Expansion-Felt'},
        {'name': 'Fasteners'},
        {'name': 'Fill'},
        {'name': 'Finishing'},
        {'name': 'Forming'},
        {'name': 'Flashing'},
        {'name': 'Permit'},
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
        {'name': 'Window-Dig-Out'},
        {'name': 'Window-Well'},
        {'name': 'Wood'}
    ]

    service_records = [
        # TODO Landscape??
        {'description': '10-ton Class 5 Fill', 'cost': 400, 'category': 'Fill', 'measurement': 'each',
         'protected': False},
        {'description': '5-ton Class 5 Fill', 'cost': 225, 'category': 'Fill', 'measurement': 'each',
         'protected': False},
        {'description': '5 Yards Black Dirt Soil', 'cost': 450, 'category': 'Soil', 'measurement': 'each',
         'protected': False},
        {'description': 'Concrete Driveway Mix', 'cost': 100, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': True},
        {'description': 'Concrete Exposed', 'cost': 120, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': False},
        {'description': 'Concrete Colored $', 'cost': 150, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': False},
        {'description': 'Concrete Colored $$', 'cost': 175, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': True},
        {'description': 'Concrete Colored $$$', 'cost': 200, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': False},
        {'description': 'Concrete Steps', 'cost': 350, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': True},
        {'description': 'Concrete Stamps', 'cost': 215, 'category': 'Stamps', 'measurement': 'each',
         'protected': True},
        {'description': 'Concrete Truck Washout Fee', 'cost': 60, 'category': 'Washout', 'measurement': 'each',
         'protected': True},
        {'description': 'Drain Tile Socked', 'cost': 60, 'category': 'Drain-Tile', 'measurement': 'linear_foot',
         'protected': False},
        {'description': 'Expansion Felt', 'cost': 1.0, 'category': 'Expansion-Felt', 'measurement': 'linear_foot',
         'protected': False},
        {'description': 'Forming, Grading and Setup', 'cost': .73, 'category': 'Forming', 'measurement': 'square_foot',
         'protected': False},
        {'description': 'Minimum Load Charge', 'cost': 120, 'category': 'Short-Load', 'measurement': 'each',
         'protected': True},
        {'description': 'Pour, Finish, Control Joints', 'cost': .78, 'category': 'Finishing',
         'measurement': 'square_foot', 'protected': True},
        {'description': 'Pour, Finish, Control Joints Colored/Stamped', 'cost': 1.75, 'category': 'Finishing',
         'measurement': 'square_foot', 'protected': True},
        {'description': 'Railing Painted', 'cost': 70, 'category': 'Railing', 'measurement': 'linear_foot',
         'protected': False},
        {'description': 'Railing Powder Coated', 'cost': 90, 'category': 'Railing', 'measurement': 'linear_foot',
         'protected': False},
        {'description': 'Rebar 1/2 Non-Coated', 'cost': .84, 'category': 'Rebar', 'measurement': 'square_foot',
         'protected': True},
        {'description': 'Rebar 1/2 Coated', 'cost': .71, 'category': 'Rebar', 'measurement': 'square_foot',
         'protected': False},
        {'description': 'Rebar 3/8 Non-Coated', 'cost': .64, 'category': 'Rebar', 'measurement': 'square_foot',
         'protected': False},
        {'description': 'Rebar 3/8 Coated', 'cost': .77, 'category': 'Rebar', 'measurement': 'square_foot',
         'protected': False},
        {'description': 'Removal - Dirt/Gravel/Sod', 'cost': .6, 'category': 'Removal-Square-Foot',
         'measurement': 'square_foot', 'protected': False},
        {'description': 'Removal - Clay', 'cost': 1.4, 'category': 'Removal-Square-Foot', 'measurement': 'square_foot',
         'protected': False},
        {'description': 'Removal - Concrete/Tar', 'cost': .9, 'category': 'Removal-Square-Foot',
         'measurement': 'square_foot', 'protected': True},
        {'description': 'Removal - Clay Per Load', 'cost': 650, 'category': 'Removal-Per-Load',
         'measurement': 'each', 'protected': False},
        {'description': 'Removal - Concrete/Tar Per Load', 'cost': 450, 'category': 'Removal-Per-Load',
         'measurement': 'each', 'protected': False},
        {'description': 'Removal - Dirt/Gravel/Sod Per Load', 'cost': 300, 'category': 'Removal-Per-Load',
         'measurement': 'each', 'protected': False},
        {'description': 'Saw Cutting', 'cost': 5, 'category': 'Saw-Cutting', 'measurement': 'linear_foot',
         'protected': False},
        {'description': 'Sealer - Cure n Seal', 'cost': .53, 'category': 'Sealer', 'measurement': 'square_foot',
         'protected': True},
        {'description': 'Sealer - Lumiseal Plus', 'cost': .8, 'category': 'Sealer', 'measurement': 'square_foot',
         'protected': True},
        {'description': 'Standard Egress Window', 'cost': 1400, 'category': 'Window', 'measurement': 'each',
         'protected': True},
        {'description': 'Window Fasteners', 'cost': 20, 'category': 'Fasteners', 'measurement': 'each',
         'protected': False},
        {'description': 'Flashing', 'cost': 25, 'category': 'Flashing', 'measurement': 'each', 'protected': True},
        {'description': 'Egress Window Building Permit', 'cost': 120, 'category': 'Permit', 'measurement': 'each',
         'protected': True},
        {'description': 'Rock for Window Well', 'cost': 25, 'category': 'Rock', 'measurement': 'each',
         'protected': True},
        {'description': 'Standard Window Well', 'cost': 250, 'category': 'Window-Well', 'measurement': 'each',
         'protected': True},
        {'description': 'Large Window Well', 'cost': 300, 'category': 'Window-Well', 'measurement': 'each',
         'protected': False},
        {'description': 'Pressure Treated Wood', 'cost': 30, 'category': 'Wood', 'measurement': 'each',
         'protected': True},
        {'description': 'Dig Out Window Well', 'cost': 30, 'category': 'Window-Dig-Out', 'measurement': 'each',
         'protected': True},



    ]

    job_type_records = [
        {'description': 'Basement Floor'},
        {'description': 'Block Foundation'},
        {'description': 'Curb'},
        {'description': 'Driveway'},
        {'description': 'Egress Window'},
        {'description': 'Garage Floor'},
        {'description': 'Patio'},
        {'description': 'Retaining Wall'},
        {'description': 'Sidewalk'},
        {'description': 'Steps'},
    ]

    for record in category_records:
        add_category(record)

    for record in service_records:
        add_service(record)

    for record in job_type_records:
        add_job_type(record)


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


def add_job_type(job_type_entry):
        print('Job Type:', job_type_entry['description'])
        item = JobType(**job_type_entry)
        item.save()


if __name__ == '__main__':
    print("Starting concrete services population script...")
    populate()
