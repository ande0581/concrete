import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concrete_project.settings')

import django
django.setup()
from category.models import Category
from job_type.models import JobType
from service.models import Service


def populate():

    category_records = [
        {'name': 'Auger', 'protected': True},
        {'name': 'Backhoe', 'protected': True},
        {'name': 'Block', 'protected': True},
        {'name': 'Block-Cap', 'protected': True},
        {'name': 'Bobcat', 'protected': True},
        {'name': 'Concrete', 'protected': True},
        {'name': 'Drain-Tile', 'protected': False},
        {'name': 'Expansion-Felt', 'protected': True},
        {'name': 'Fasteners', 'protected': True},
        {'name': 'Fill', 'protected': True},
        {'name': 'Finishing', 'protected': True},
        {'name': 'Forming', 'protected': True},
        {'name': 'Flashing', 'protected': True},
        {'name': 'GeoGrid', 'protected': True},
        {'name': 'Permit', 'protected': True},
        {'name': 'Pump-Truck', 'protected': True},
        {'name': 'Railing', 'protected': True},
        {'name': 'Rebar', 'protected': True},
        {'name': 'Removal-Per-Load', 'protected': False},
        {'name': 'Removal-Square-Foot', 'protected': True},
        {'name': 'Rock', 'protected': True},
        {'name': 'Saw-Cutting', 'protected': True},
        {'name': 'Sealer', 'protected': True},
        {'name': 'Sonotube', 'protected': True},
        {'name': 'Soil', 'protected': False},
        {'name': 'Stamps', 'protected': True},
        {'name': 'Short-Load', 'protected': True},
        {'name': 'Washout', 'protected': True},
        {'name': 'Waterproofing', 'protected': True},
        {'name': 'Window', 'protected': True},
        {'name': 'Window-Dig-Out', 'protected': True},
        {'name': 'Window-Well', 'protected': True},
        {'name': 'Wood', 'protected': True}
    ]

    service_records = [
        # TODO Landscape??
        {'description': '10-ton Class 5 Fill', 'cost': 400, 'category': 'Fill', 'measurement': 'each',
         'protected': False},
        {'description': '5-ton Class 5 Fill', 'cost': 225, 'category': 'Fill', 'measurement': 'each',
         'protected': False},
        {'description': '5 Yards Black Dirt Soil', 'cost': 450, 'category': 'Soil', 'measurement': 'each',
         'protected': False},
        {'description': 'Concrete Block Foundation Mix', 'cost': 250, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': True},
        {'description': 'Concrete Colored $', 'cost': 150, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': False},
        {'description': 'Concrete Colored $$', 'cost': 175, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': True},
        {'description': 'Concrete Colored $$$', 'cost': 200, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': False},
        {'description': 'Concrete Driveway Mix', 'cost': 100, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': True},
        {'description': 'Concrete Exposed Mix', 'cost': 120, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': False},
        {'description': 'Concrete Floating Slab Mix', 'cost': 200, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': True},
        {'description': 'Concrete Pier Footings Mix', 'cost': 300, 'category': 'Concrete', 'measurement': 'cubic_yard',
         'protected': True},
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
        {'description': 'Forming, Grading and Setup Floating Slab', 'cost': 1.0, 'category': 'Forming', 'measurement':
         'square_foot', 'protected': True},
        {'description': 'Forming, Grading and Setup Block Foundation', 'cost': 1.5, 'category': 'Forming', 'measurement':
         'square_foot', 'protected': True},
        {'description': 'Minimum Load Charge', 'cost': 120, 'category': 'Short-Load', 'measurement': 'each',
         'protected': True},
        {'description': 'Pour, Finish, Control Joints', 'cost': .78, 'category': 'Finishing',
         'measurement': 'square_foot', 'protected': True},
        {'description': 'Pour, Finish, Control Joints Colored/Stamped', 'cost': 1.75, 'category': 'Finishing',
         'measurement': 'square_foot', 'protected': True},
        {'description': 'Pour, Finish, Control Joints Floating Slab', 'cost': 1.03, 'category': 'Finishing',
         'measurement': 'square_foot', 'protected': True},
        {'description': 'Pour, Finish, Control Joints Block Foundation', 'cost': 1.15, 'category': 'Finishing',
         'measurement': 'square_foot', 'protected': True},
        {'description': 'Railing Painted', 'cost': 70, 'category': 'Railing', 'measurement': 'linear_foot',
         'protected': False},
        {'description': 'Railing Powder Coated', 'cost': 90, 'category': 'Railing', 'measurement': 'linear_foot',
         'protected': False},
        {'description': 'Rebar 1/2 Non-Coated', 'cost': .84, 'category': 'Rebar', 'measurement': 'square_foot',
         'protected': True},
        {'description': 'Rebar 1/2 Non-Coated Block Foundation', 'cost': 1.10, 'category': 'Rebar', 'measurement':
         'square_foot', 'protected': True},
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
        {'description': 'Rock for Retaining Wall', 'cost': 50, 'category': 'Rock', 'measurement': 'cubic_yard',
         'protected': True},
        {'description': 'Standard Window Well', 'cost': 250, 'category': 'Window-Well', 'measurement': 'each',
         'protected': True},
        {'description': 'Large Window Well', 'cost': 300, 'category': 'Window-Well', 'measurement': 'each',
         'protected': False},
        {'description': 'Pressure Treated Wood', 'cost': 30, 'category': 'Wood', 'measurement': 'each',
         'protected': True},
        {'description': 'Dig Out Window Well', 'cost': 30, 'category': 'Window-Dig-Out', 'measurement': 'each',
         'protected': True},
        {'description': 'General Bobcat Labor', 'cost': 65, 'category': 'Bobcat', 'measurement': 'each',
         'protected': True},
        {'description': 'Standard Foundation Waterproofing', 'cost': .7, 'category': 'Waterproofing',
         'measurement': 'square_foot', 'protected': False},
        {'description': 'Standard Concrete Pump Truck', 'cost': 1200, 'category': 'Pump-Truck', 'measurement': 'each',
         'protected': False},
        {'description': 'Large Backhoe', 'cost': 300, 'category': 'Backhoe', 'measurement': 'each',
         'protected': False},
        {'description': 'Small Backhoe', 'cost': 200, 'category': 'Backhoe', 'measurement': 'each',
         'protected': False},
        {'description': 'Sonotube 8in x 4ft', 'cost': 5.15, 'category': 'Sonotube', 'measurement': 'each',
         'protected': False},
        {'description': 'Sonotube 10in x 4ft', 'cost': 7.58, 'category': 'Sonotube', 'measurement': 'each',
         'protected': False},
        {'description': 'GeoGrid 6ft x 150ft', 'cost': 250, 'category': 'GeoGrid', 'measurement': 'each',
         'protected': False},
        {'description': 'GeoGrid 4ft x 45ft', 'cost': 60, 'category': 'GeoGrid', 'measurement': 'each',
         'protected': False},
        {'description': 'Auger 8in x 4ft Hole', 'cost': 15, 'category': 'Auger', 'measurement': 'each',
         'protected': False},
        {'description': 'Auger 10in x 4ft Hole', 'cost': 17, 'category': 'Auger', 'measurement': 'each',
         'protected': False},
        {'description': 'Clifton Wall Straight 8" x 18" x 12"', 'cost': 4.79, 'category': 'Block', 'measurement': 'each',
         'protected': False, 'height': 8, 'width': 18, 'depth': 12},
        {'description': 'Crestone 3 1/2" x 11 1/2" x 7"', 'cost': 1.25, 'category': 'Block', 'measurement': 'each',
         'protected': False, 'height': 3.5, 'width': 11.5, 'depth': 7},
        {'description': 'Clifton Wall XL Straight Cap 3 1/2" x 18" x 13"', 'cost': 4.75, 'category': 'Block-Cap',
         'measurement': 'each', 'protected': False, 'height': 3.5, 'width': 18, 'depth': 13},
        {'description': 'Crestone Cap 2 3/8" x 12" x 7 1/2"', 'cost': 1.78, 'category': 'Block-Cap',
         'measurement': 'each', 'protected': False, 'height': 2.375, 'width': 12, 'depth': 7.5},
    ]

    job_type_records = [
        {'description': 'Basement Floor'},
        {'description': 'Block Foundation'},
        {'description': 'Curb'},
        {'description': 'Driveway'},
        {'description': 'Egress Window'},
        {'description': 'Floating Slab'},
        {'description': 'Garage Floor'},
        {'description': 'Patio'},
        {'description': 'Pier Footings'},
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
