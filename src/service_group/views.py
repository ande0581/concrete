from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
import math

from bid.models import Bid
from bid_item.models import BidItem
from service.models import Service

from service_group.forms import StepsForm, BlockFoundationForm, PierFootingsForm, EgressWindowForm, FloatingSlabForm, \
    RetainingWallForm

# Enable Print Statements to Facilitate Debugging
DEBUG_SERVICE_GROUP = False


def calculate_square_feet(length, width):
    square_feet = length * width
    return round(square_feet, 1)


def calculate_cubic_yards(length, width, thickness):
    """
    :param length: length in feet
    :param width: width in feet
    :param thickness: thickness in inches
    :return: cubic_yards
    """
    cubic_yards = (length * width * (thickness / 12)) / 27

    # add 5% extra
    cubic_yards *= 1.05
    return round(cubic_yards, 2)


def calculate_cubic_yards_using_sq_ft(sq_ft, thickness):
    cubic_yards = (sq_ft * (thickness / 12)) / 27

    # add 5% extra
    cubic_yards *= 1.05
    return round(cubic_yards, 2)


def calculate_cubic_yards_cylinder(diameter, depth):
    diameter /= 12
    depth /= 12
    area = math.pi * math.pow((diameter / 2), 2)
    cubic_yards = (area * depth) / 27

    # add 5% extra
    cubic_yards *= 1.05
    return round(cubic_yards, 2)


def get_one_object(service_name):
    obj = Service.objects.get(description=service_name)
    return obj


def insert_bid_item(**item_details):
    item = BidItem(**item_details)
    item.save()


def calculate_steps_cubic_yards(length, width, num_steps):
    """
    standard step depth is 12"
    standard step height is 7.5"
    """
    total_area = []
    for i in range(num_steps):
        area = calculate_cubic_yards(length=length, width=width, thickness=7.5)
        total_area.append(area)
        length += 1  # add one foot for the depth of each step

    return round(sum(total_area), 2)


def calculate_steps_square_feet(length, width, num_steps):

    total_sq_ft = []
    for i in range(num_steps):
        if i == 0:
            surface = length * width
        else:
            surface = width * 1

        left_side = length * 1
        front_side = width * 1
        right_side = length * 1
        total = left_side + front_side + right_side + surface
        total_sq_ft.append(total)
        length += 1  # add one foot for each new step

        if DEBUG_SERVICE_GROUP:
            print("calculate_steps_square_feet Step Count:", i)
            print('calculate_steps_square_feet Step Surface Sq-Ft:', surface)
            print('calculate_steps_square_feet Step Sq-Ft:', total)
            print("_" * 30)

    return round(sum(total_sq_ft), 2)


def calculate_railing_length(length, num_steps):
    railing_length = length + ((num_steps - 1) * 1)
    return math.ceil(railing_length)


def calculate_number_of_block(linear_feet, height, block_obj):

    blocks_per_row = (linear_feet * 12) / block_obj.width
    number_of_rows = math.ceil((height * 12) / block_obj.height)
    total_blocks = blocks_per_row * number_of_rows

    if DEBUG_SERVICE_GROUP:
        print('calculate_number_of_block Blocks Per Row:', blocks_per_row)
        print('calculate_number_of_block Number of Block Rows:', number_of_rows)
        print('calculate_number_of_block Total Blocks:', total_blocks)

    # Add 10% extra
    total_blocks *= 1.10

    if DEBUG_SERVICE_GROUP:
        print('calculate_number_of_block Total Blocks Plus Waste:', total_blocks)

    return math.ceil(total_blocks)


def calculate_number_of_block_caps(linear_feet, cap_obj):
    caps_per_row = math.ceil((linear_feet * 12) / cap_obj.width)

    # Add 10% extra
    caps_per_row *= 1.10
    return math.ceil(caps_per_row)


class ConcreteCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """
    (length x width x thickness) / 27 = yards

    """
    template_name = 'service_group/service_group_form.html'

    def get_success_url(self):
        messages.success(self.request, "Concrete Estimated")
        return reverse('bid_app:bid_detail', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):
        if DEBUG_SERVICE_GROUP:
            print("ConcreteCreate Post Form Save:", form.cleaned_data)
        job_type = form.cleaned_data['job_type']
        length = form.cleaned_data['length']
        width = form.cleaned_data['width']
        thickness = form.cleaned_data['thickness']
        sq_ft = form.cleaned_data['sq_ft']
        concrete = form.cleaned_data['concrete_type']
        washout = form.cleaned_data.get('washout', None)
        rebar = form.cleaned_data['rebar_type']
        removal = form.cleaned_data['removal']
        saw_cutting_qty = form.cleaned_data['saw_cutting']
        expansion_felt_qty = form.cleaned_data['expansion_felt']
        forming = form.cleaned_data['forming']
        fill = form.cleaned_data['fill']
        finishing = form.cleaned_data['finishing']
        stamps = form.cleaned_data.get('stamps', None)
        sealer = form.cleaned_data['sealer']

        if not sq_ft:
            sq_ft = calculate_square_feet(length, width)
            cubic_yards = calculate_cubic_yards(length, width, thickness)
        else:
            cubic_yards = calculate_cubic_yards_using_sq_ft(sq_ft, thickness)

        bid_obj = Bid.objects.get(pk=self.kwargs['bid'])

        concrete_obj = get_one_object(concrete)
        concrete_record = {'bid': bid_obj,
                           'job_type': job_type,
                           'quantity': cubic_yards,
                           'cost': concrete_obj.cost,
                           'description': concrete_obj.description,
                           'total': (concrete_obj.cost * cubic_yards)}
        insert_bid_item(**concrete_record)

        # Check For Short Load Fee
        if cubic_yards < 5:
            short_load_obj = get_one_object('Minimum Load Charge')
            short_load_record = {'bid': bid_obj,
                                 'job_type': job_type,
                                 'quantity': 1,
                                 'cost': short_load_obj.cost,
                                 'description': short_load_obj.description,
                                 'total': short_load_obj.cost}
            insert_bid_item(**short_load_record)

        if washout:
            washout_obj = get_one_object('Concrete Truck Washout Fee')
            washout_record = {'bid': bid_obj,
                              'job_type': job_type,
                              'quantity': 1,
                              'cost': washout_obj.cost,
                              'description': washout_obj.description,
                              'total': washout_obj.cost}
            insert_bid_item(**washout_record)

        if rebar:
            rebar_obj = get_one_object(rebar)
            rebar_record = {'bid': bid_obj,
                            'job_type': job_type,
                            'quantity': sq_ft,
                            'cost': rebar_obj.cost,
                            'description': rebar_obj.description,
                            'total': (rebar_obj.cost * sq_ft)}
            insert_bid_item(**rebar_record)

        if removal:
            removal_obj = get_one_object(removal)
            removal_record = {'bid': bid_obj,
                              'job_type': job_type,
                              'quantity': sq_ft,
                              'cost': removal_obj.cost,
                              'description': removal_obj.description,
                              'total': (removal_obj.cost * sq_ft)}
            insert_bid_item(**removal_record)

        if saw_cutting_qty:
            saw_cutting_obj = get_one_object('Saw Cutting')
            saw_cutting_record = {'bid': bid_obj,
                                  'job_type': job_type,
                                  'quantity': saw_cutting_qty,
                                  'cost': saw_cutting_obj.cost,
                                  'description': saw_cutting_obj.description,
                                  'total': (saw_cutting_obj.cost * saw_cutting_qty)}
            insert_bid_item(**saw_cutting_record)

        if forming:
            forming_obj = get_one_object(forming)
            forming_record = {'bid': bid_obj,
                              'job_type': job_type,
                              'quantity': sq_ft,
                              'cost': forming_obj.cost,
                              'description': forming_obj.description,
                              'total': (forming_obj.cost * sq_ft)}
            insert_bid_item(**forming_record)

        if expansion_felt_qty:
            expansion_felt_obj = get_one_object('Expansion Felt')
            expansion_felt_record = {'bid': bid_obj,
                                     'job_type': job_type,
                                     'quantity': expansion_felt_qty,
                                     'cost': expansion_felt_obj.cost,
                                     'description': expansion_felt_obj.description,
                                     'total': (expansion_felt_obj.cost * expansion_felt_qty)}
            insert_bid_item(**expansion_felt_record)

        if fill:
            fill_obj = get_one_object(fill)
            fill_record = {'bid': bid_obj,
                           'job_type': job_type,
                           'quantity': 1,
                           'cost': fill_obj.cost,
                           'description': fill_obj.description,
                           'total': fill_obj.cost}
            insert_bid_item(**fill_record)

        finishing_obj = get_one_object(finishing)
        finishing_record = {'bid': bid_obj,
                            'job_type': job_type,
                            'quantity': sq_ft,
                            'cost': finishing_obj.cost,
                            'description': finishing_obj.description,
                            'total': (finishing_obj.cost * sq_ft)}
        insert_bid_item(**finishing_record)

        if stamps:
            stamp_obj = get_one_object(stamps)
            stamp_record = {'bid': bid_obj,
                            'job_type': job_type,
                            'quantity': 1,
                            'cost': stamp_obj.cost,
                            'description': stamp_obj.description,
                            'total': stamp_obj.cost}
            insert_bid_item(**stamp_record)

        if sealer:
            sealer_obj = get_one_object(sealer)
            sealer_record = {'bid': bid_obj,
                             'job_type': job_type,
                             'quantity': sq_ft,
                             'cost': sealer_obj.cost,
                             'description': sealer_obj.description,
                             'total': (sealer_obj.cost * sq_ft)}
            insert_bid_item(**sealer_record)

        return super(ConcreteCreate, self).form_valid(form)


class FloatingSlabCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = FloatingSlabForm

    def get_success_url(self):
        messages.success(self.request, "Floating Slab Estimated")
        return reverse('bid_app:bid_detail', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        job_type = form.cleaned_data['job_type']
        length = form.cleaned_data['length']
        width = form.cleaned_data['width']
        thickness = form.cleaned_data['thickness']
        concrete = form.cleaned_data['concrete_type']
        rebar = form.cleaned_data['rebar_type']
        forming = form.cleaned_data['forming']
        finishing = form.cleaned_data['finishing']
        sealer = form.cleaned_data['sealer']

        linear_ft = (length + width) * 2
        cubic_yards_floor = calculate_cubic_yards(length=length, width=width, thickness=thickness)
        cubic_yards_perimeter = calculate_cubic_yards(length=linear_ft, width=1.25, thickness=12)
        cubic_yards_perimeter_triangle = calculate_cubic_yards(length=linear_ft, width=1, thickness=12) / 2
        cubic_yards = cubic_yards_floor + cubic_yards_perimeter + cubic_yards_perimeter_triangle

        sq_ft_floor = calculate_square_feet(length=length, width=width)
        sq_ft_perimeter = calculate_square_feet(length=linear_ft, width=3)
        sq_ft = sq_ft_floor + sq_ft_perimeter

        if DEBUG_SERVICE_GROUP:
            print('FloatingSlabCreate Post Form Save:', form.cleaned_data)
            print('FloatingSlabCreate Cubic Yards Floor', cubic_yards_floor)
            print('FloatingSlabCreate Cubic Yards Perimeter', cubic_yards_perimeter)
            print('FloatingSlabCreate Cubic Yards Perimeter Triangle', cubic_yards_perimeter_triangle)
            print('FloatingSlabCreate Cubic Yards Total', cubic_yards)
            print('FloatingSlabCreate SqFt Floor', sq_ft_floor)
            print('FloatingSlabCreate SqFt Perimeter', sq_ft_perimeter)
            print('FloatingSlabCreate SqFt Total', sq_ft)

        bid_obj = Bid.objects.get(pk=self.kwargs['bid'])

        concrete_obj = get_one_object(concrete)
        concrete_record = {'bid': bid_obj,
                           'job_type': job_type,
                           'quantity': cubic_yards,
                           'cost': concrete_obj.cost,
                           'description': concrete_obj.description,
                           'total': (concrete_obj.cost * cubic_yards)}
        insert_bid_item(**concrete_record)

        # Check For Short Load Fee
        if cubic_yards < 5:
            short_load_obj = get_one_object('Minimum Load Charge')
            short_load_record = {'bid': bid_obj,
                                 'job_type': job_type,
                                 'quantity': 1,
                                 'cost': short_load_obj.cost,
                                 'description': short_load_obj.description,
                                 'total': short_load_obj.cost}
            insert_bid_item(**short_load_record)

        if rebar:
            rebar_obj = get_one_object(rebar)
            rebar_record = {'bid': bid_obj,
                            'job_type': job_type,
                            'quantity': sq_ft,
                            'cost': rebar_obj.cost,
                            'description': rebar_obj.description,
                            'total': (rebar_obj.cost * sq_ft)}
            insert_bid_item(**rebar_record)

        if forming:
            forming_obj = get_one_object(forming)
            forming_record = {'bid': bid_obj,
                              'job_type': job_type,
                              'quantity': sq_ft,
                              'cost': forming_obj.cost,
                              'description': forming_obj.description,
                              'total': (forming_obj.cost * sq_ft)}
            insert_bid_item(**forming_record)

        finishing_obj = get_one_object(finishing)
        finishing_record = {'bid': bid_obj,
                            'job_type': job_type,
                            'quantity': sq_ft,
                            'cost': finishing_obj.cost,
                            'description': finishing_obj.description,
                            'total': (finishing_obj.cost * sq_ft)}
        insert_bid_item(**finishing_record)

        if sealer:
            sealer_obj = get_one_object(sealer)
            sealer_record = {'bid': bid_obj,
                             'job_type': job_type,
                             'quantity': sq_ft,
                             'cost': sealer_obj.cost,
                             'description': sealer_obj.description,
                             'total': (sealer_obj.cost * sq_ft)}
            insert_bid_item(**sealer_record)

        return super(FloatingSlabCreate, self).form_valid(form)


class StepsCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = StepsForm

    def get_success_url(self):
        messages.success(self.request, "Steps Estimated")
        return reverse('bid_app:bid_detail', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        job_type = form.cleaned_data['job_type']
        length = form.cleaned_data['length'] / 12
        width = form.cleaned_data['width'] / 12
        num_steps = form.cleaned_data['num_steps']
        concrete = form.cleaned_data['concrete_type']
        removal = form.cleaned_data['removal']
        short_load = form.cleaned_data['short_load']
        railing = form.cleaned_data['railing']
        sealer = form.cleaned_data['sealer']

        cubic_yards = calculate_steps_cubic_yards(length=length, width=width, num_steps=num_steps)
        sq_ft = calculate_steps_square_feet(length=length, width=width, num_steps=num_steps)
        railing_length = calculate_railing_length(length=length, num_steps=num_steps)

        if DEBUG_SERVICE_GROUP:
            print("StepsCreate Post Form Save", form.cleaned_data)
            print('StepsCreate job_type:', job_type)
            print('StepsCreate cubic_yards:', cubic_yards)
            print('StepsCreate num_steps:', num_steps)
            print('StepsCreate concrete:', concrete)
            print('StepsCreate removal:', removal)
            print('StepsCreate short_load:', short_load)
            print('StepsCreate railing:', railing)
            print('StepsCreate sealer:', sealer)

        bid_obj = Bid.objects.get(pk=self.kwargs['bid'])

        if removal:
            removal_record = {'bid': bid_obj,
                              'job_type': job_type,
                              'quantity': 1,
                              'cost': removal,
                              'description': 'Remove Existing Steps',
                              'total': removal}
            insert_bid_item(**removal_record)

        concrete_obj = get_one_object(concrete)
        concrete_record = {'bid': bid_obj,
                           'job_type': job_type,
                           'quantity': cubic_yards,
                           'cost': concrete_obj.cost,
                           'description': concrete_obj.description,
                           'total': (concrete_obj.cost * cubic_yards)}
        insert_bid_item(**concrete_record)

        if short_load:
            short_load_obj = get_one_object('Minimum Load Charge')
            short_load_record = {'bid': bid_obj,
                                 'job_type': job_type,
                                 'quantity': 1,
                                 'cost': short_load_obj.cost,
                                 'description': short_load_obj.description,
                                 'total': short_load_obj.cost}
            insert_bid_item(**short_load_record)

        if railing:
            railing_obj = get_one_object(railing)
            railing_record = {'bid': bid_obj,
                              'job_type': job_type,
                              'quantity': railing_length,
                              'cost': railing_obj.cost,
                              'description': railing_obj.description,
                              'total': railing_obj.cost * railing_length}
            insert_bid_item(**railing_record)

        if sealer:
            sealer_obj = get_one_object(sealer)
            sealer_record = {'bid': bid_obj,
                             'job_type': job_type,
                             'quantity': sq_ft,
                             'cost': sealer_obj.cost,
                             'description': sealer_obj.description,
                             'total': (sealer_obj.cost * sq_ft)}
            insert_bid_item(**sealer_record)

        return super(StepsCreate, self).form_valid(form)


class BlockFoundationCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = BlockFoundationForm

    def get_success_url(self):
        messages.success(self.request, "Block Foundation Estimated")
        return reverse('bid_app:bid_detail', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        job_type = form.cleaned_data['job_type']
        linear_feet = form.cleaned_data['linear_feet']
        width = int(form.cleaned_data['width'])
        height = form.cleaned_data['height'] / 12
        concrete = form.cleaned_data['concrete']
        rebar = form.cleaned_data['rebar_type']
        forming = form.cleaned_data['forming']
        finishing = form.cleaned_data['finishing']
        backhoe = form.cleaned_data['backhoe']
        waterproofing = form.cleaned_data['waterproofing']
        pump_trunk = form.cleaned_data['pump_truck']
        bobcat_hours = form.cleaned_data['bobcat_hours']

        # Calculate Cubic Yards
        if width == 8:
            cubic_yards_footing = calculate_cubic_yards(length=linear_feet, width=1.25, thickness=12)
        else:  # width == 12
            cubic_yards_footing = calculate_cubic_yards(length=linear_feet, width=1.67, thickness=12)

        cubic_yards_foundation = calculate_cubic_yards(length=linear_feet, width=height, thickness=width)
        cubic_yards = round(cubic_yards_footing + cubic_yards_foundation, 2)

        # Calculate Square Footage
        sq_ft_footing = calculate_square_feet(length=linear_feet, width=1)
        sq_ft_foundation = calculate_square_feet(length=linear_feet, width=height)
        sq_ft = round(sq_ft_footing + sq_ft_foundation, 2)

        if DEBUG_SERVICE_GROUP:
            print('BlockFoundationCreate post form save:', form.cleaned_data)
            print('BlockFoundationCreate cubic yards footings:', cubic_yards_footing)
            print('BlockFoundationCreate cubic yards foundation:', cubic_yards_foundation)
            print('BlockFoundationCreate cubic yards total:', cubic_yards)
            print('BlockFoundationCreate sq ft footings:', sq_ft_footing)
            print('BlockFoundationCreate sq ft foundation:', sq_ft_foundation)
            print('BlockFoundationCreate sq ft total:', sq_ft)

        bid_obj = Bid.objects.get(pk=self.kwargs['bid'])

        concrete_obj = get_one_object(concrete)
        concrete_record = {'bid': bid_obj,
                           'job_type': job_type,
                           'quantity': cubic_yards,
                           'cost': concrete_obj.cost,
                           'description': concrete_obj.description,
                           'total': (concrete_obj.cost * cubic_yards)}
        insert_bid_item(**concrete_record)

        # Check For Short Load Fee
        if cubic_yards < 5:
            short_load_obj = get_one_object('Minimum Load Charge')
            short_load_record = {'bid': bid_obj,
                                 'job_type': job_type,
                                 'quantity': 1,
                                 'cost': short_load_obj.cost,
                                 'description': short_load_obj.description,
                                 'total': short_load_obj.cost}
            insert_bid_item(**short_load_record)

        if rebar:
            rebar_obj = get_one_object(rebar)
            rebar_record = {'bid': bid_obj,
                            'job_type': job_type,
                            'quantity': sq_ft,
                            'cost': rebar_obj.cost,
                            'description': rebar_obj.description,
                            'total': (rebar_obj.cost * sq_ft)}
            insert_bid_item(**rebar_record)

        if forming:
            forming_obj = get_one_object(forming)
            forming_record = {'bid': bid_obj,
                              'job_type': job_type,
                              'quantity': sq_ft,
                              'cost': forming_obj.cost,
                              'description': forming_obj.description,
                              'total': (forming_obj.cost * sq_ft)}
            insert_bid_item(**forming_record)

        finishing_obj = get_one_object(finishing)
        finishing_record = {'bid': bid_obj,
                            'job_type': job_type,
                            'quantity': sq_ft,
                            'cost': finishing_obj.cost,
                            'description': finishing_obj.description,
                            'total': (finishing_obj.cost * sq_ft)}
        insert_bid_item(**finishing_record)

        if backhoe:
            backhoe_obj = get_one_object(backhoe)
            backhoe_record = {'bid': bid_obj,
                              'job_type': job_type,
                              'quantity': 1,
                              'cost': backhoe_obj.cost,
                              'description': backhoe_obj.description,
                              'total': backhoe_obj.cost}
            insert_bid_item(**backhoe_record)

        if waterproofing:
            waterproofing_obj = get_one_object(waterproofing)
            waterproofing_record = {'bid': bid_obj,
                                    'job_type': job_type,
                                    'quantity': sq_ft_foundation,
                                    'cost': waterproofing_obj.cost,
                                    'description': waterproofing_obj.description,
                                    'total': (waterproofing_obj.cost * sq_ft_foundation)}
            insert_bid_item(**waterproofing_record)

        if pump_trunk:
            pump_trunk_obj = get_one_object(pump_trunk)
            pump_trunk_record = {'bid': bid_obj,
                                 'job_type': job_type,
                                 'quantity': 1,
                                 'cost': pump_trunk_obj.cost,
                                 'description': pump_trunk_obj.description,
                                 'total': pump_trunk_obj.cost}
            insert_bid_item(**pump_trunk_record)

        if bobcat_hours:
            bobcat_obj = get_one_object('General Bobcat Labor')
            bobcat_record = {'bid': bid_obj,
                             'job_type': job_type,
                             'quantity': bobcat_hours,
                             'cost': bobcat_obj.cost,
                             'description': bobcat_obj.description,
                             'total': (bobcat_obj.cost * bobcat_hours)}
            insert_bid_item(**bobcat_record)

        return super(BlockFoundationCreate, self).form_valid(form)


class PierFootingsCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = PierFootingsForm

    def get_success_url(self):
        messages.success(self.request, "Pier Footings Estimated")
        return reverse('bid_app:bid_detail', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        job_type = form.cleaned_data['job_type']
        diameter = form.cleaned_data['diameter']
        depth = form.cleaned_data['depth']
        concrete = form.cleaned_data['concrete']
        auger = form.cleaned_data['auger']
        sonotube = form.cleaned_data['sonotube']
        setup = form.cleaned_data['setup']
        quantity = form.cleaned_data['quantity']

        if DEBUG_SERVICE_GROUP:
            print("PierFootingsCreate Post Form Save:", form.cleaned_data)
            print('PierFootingsCreate Job Type:', job_type)
            print('PierFootingsCreate Diameter:', diameter)
            print('PierFootingsCreate Depth:', depth)
            print('PierFootingsCreate Concrete', concrete)
            print('PierFootingsCreate Auger:', auger)
            print('PierFootingsCreate Sonotube:', sonotube)
            print('PierFootingsCreate Setup:', setup)
            print('PierFootingsCreate Quantity:', quantity)

        cubic_yards = calculate_cubic_yards_cylinder(diameter=diameter, depth=depth)
        if DEBUG_SERVICE_GROUP:
            print('PierFootingsCreate Cubic Yards Before Quantity', cubic_yards)
        cubic_yards *= quantity
        if DEBUG_SERVICE_GROUP:
            print('PierFootingsCreate Cubic Yards After Quantity', cubic_yards)

        bid_obj = Bid.objects.get(pk=self.kwargs['bid'])

        concrete_obj = get_one_object(concrete)
        concrete_record = {'bid': bid_obj,
                           'job_type': job_type,
                           'quantity': cubic_yards,
                           'cost': concrete_obj.cost,
                           'description': concrete_obj.description,
                           'total': (concrete_obj.cost * cubic_yards)}
        insert_bid_item(**concrete_record)

        # Check For Short Load Fee
        if cubic_yards < 5:
            short_load_obj = get_one_object('Minimum Load Charge')
            short_load_record = {'bid': bid_obj,
                                 'job_type': job_type,
                                 'quantity': 1,
                                 'cost': short_load_obj.cost,
                                 'description': short_load_obj.description,
                                 'total': short_load_obj.cost}
            insert_bid_item(**short_load_record)

        if auger:
            auger_obj = get_one_object(auger)
            auger_record = {'bid': bid_obj,
                            'job_type': job_type,
                            'quantity': quantity,
                            'cost': auger_obj.cost,
                            'description': auger_obj.description,
                            'total': (auger_obj.cost * quantity)}
            insert_bid_item(**auger_record)

        if sonotube:
            sonotube_obj = get_one_object(sonotube)
            sonotube_record = {'bid': bid_obj,
                               'job_type': job_type,
                               'quantity': quantity,
                               'cost': sonotube_obj.cost,
                               'description': sonotube_obj.description,
                               'total': (sonotube_obj.cost * quantity)}
            insert_bid_item(**sonotube_record)

        if setup:
            setup_record = {'bid': bid_obj,
                            'job_type': job_type,
                            'quantity': quantity,
                            'cost': setup,
                            'description': 'Footing Layout and Setup',
                            'total': (setup * quantity)}
            insert_bid_item(**setup_record)

        return super(PierFootingsCreate, self).form_valid(form)


class EgressWindowCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = EgressWindowForm

    def get_success_url(self):
        messages.success(self.request, "Egress Window Estimated")
        return reverse('bid_app:bid_detail', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        job_type = form.cleaned_data['job_type']
        wood = form.cleaned_data['wood']
        dig_out = form.cleaned_data['dig_out']
        flashing = form.cleaned_data['flashing']
        window = form.cleaned_data['window']
        window_well = form.cleaned_data['window_well']
        fasteners = form.cleaned_data['fasteners']
        permit = form.cleaned_data['permit']
        rock = form.cleaned_data['rock']

        if DEBUG_SERVICE_GROUP:
            print('EgressWindowCreate Post Form Save:', form.cleaned_data)
            print('EgressWindowCreate job_type:', job_type)
            print('EgressWindowCreate wood:', wood)
            print('EgressWindowCreate dig_out:', dig_out)
            print('EgressWindowCreate flashing:', flashing)
            print('EgressWindowCreate window:', window)
            print('EgressWindowCreate window_well', window_well)
            print('EgressWindowCreate fasteners:', fasteners)
            print('EgressWindowCreate permit:', permit)
            print('EgressWindowCreate rock:', rock)

        bid_obj = Bid.objects.get(pk=self.kwargs['bid'])

        wood_obj = get_one_object(wood)
        wood_record = {'bid': bid_obj,
                       'job_type': job_type,
                       'quantity': 1,
                       'cost': wood_obj.cost,
                       'description': wood_obj.description,
                       'total': wood_obj.cost}
        insert_bid_item(**wood_record)

        dig_out_obj = get_one_object(dig_out)
        dig_out_record = {'bid': bid_obj,
                          'job_type': job_type,
                          'quantity': 1,
                          'cost': dig_out_obj.cost,
                          'description': dig_out_obj.description,
                          'total': dig_out_obj.cost}
        insert_bid_item(**dig_out_record)

        flashing_obj = get_one_object(flashing)
        flashing_record = {'bid': bid_obj,
                           'job_type': job_type,
                           'quantity': 1,
                           'cost': flashing_obj.cost,
                           'description': flashing_obj.description,
                           'total': flashing_obj.cost}
        insert_bid_item(**flashing_record)

        window_obj = get_one_object(window)
        window_record = {'bid': bid_obj,
                         'job_type': job_type,
                         'quantity': 1,
                         'cost': window_obj.cost,
                         'description': window_obj.description,
                         'total': window_obj.cost}
        insert_bid_item(**window_record)

        window_well_obj = get_one_object(window_well)
        window_well_record = {'bid': bid_obj,
                              'job_type': job_type,
                              'quantity': 1,
                              'cost': window_well_obj.cost,
                              'description': window_well_obj.description,
                              'total': window_obj.cost}
        insert_bid_item(**window_well_record)

        fasteners_obj = get_one_object(fasteners)
        fasteners_record = {'bid': bid_obj,
                            'job_type': job_type,
                            'quantity': 1,
                            'cost': fasteners_obj.cost,
                            'description': fasteners_obj.description,
                            'total': fasteners_obj.cost}
        insert_bid_item(**fasteners_record)

        permit_obj = get_one_object(permit)
        permit_record = {'bid': bid_obj,
                         'job_type': job_type,
                         'quantity': 1,
                         'cost': permit_obj.cost,
                         'description': permit_obj.description,
                         'total': permit_obj.cost}
        insert_bid_item(**permit_record)

        rock_obj = get_one_object(rock)
        rock_record = {'bid': bid_obj,
                       'job_type': job_type,
                       'quantity': 1,
                       'cost': rock_obj.cost,
                       'description': rock_obj.description,
                       'total': rock_obj.cost}
        insert_bid_item(**rock_record)

        return super(EgressWindowCreate, self).form_valid(form)


class RetainingWallCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = RetainingWallForm

    def get_success_url(self):
        messages.success(self.request, "Retaining Wall Estimated")
        return reverse('bid_app:bid_detail', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        job_type = form.cleaned_data['job_type']
        linear_feet = form.cleaned_data['linear_feet']
        height = form.cleaned_data['height']
        block_type = form.cleaned_data['block_type']
        cap_type = form.cleaned_data['cap_type']
        removal_cost = form.cleaned_data['removal_cost']
        geogrid_type = form.cleaned_data['geogrid_type']
        geogrid_count = form.cleaned_data['geogrid_count']
        rock = form.cleaned_data['rock']
        drain_tile = form.cleaned_data['drain_tile']

        if DEBUG_SERVICE_GROUP:
            print('RetainingWallCreate Post Form Save:', form.cleaned_data)
            print('RetainingWallCreate Job Type:', job_type)
            print('RetainingWallCreate Linear Feet:', linear_feet)
            print('RetainingWallCreate Height:', height)
            print('RetainingWallCreate Block Type:', block_type)
            print('RetainingWallCreate Cap Type:', cap_type)
            print('RetainingWallCreate removal_cost:', removal_cost)
            print('RetainingWallCreate GeoGrid Type:', geogrid_type)
            print('RetainingWallCreate GeoGrid Count:', geogrid_count)
            print('RetainingWallCreate Rock:', rock)
            print('RetainingWallCreate Drain Tile:', drain_tile)

        bid_obj = Bid.objects.get(pk=self.kwargs['bid'])

        block_obj = get_one_object(block_type)
        block_count = calculate_number_of_block(linear_feet=linear_feet, height=height, block_obj=block_obj)
        block_record = {'bid': bid_obj,
                        'job_type': job_type,
                        'quantity': block_count,
                        'cost': block_obj.cost,
                        'description': block_obj.description,
                        'total': (block_obj.cost * block_count)}
        insert_bid_item(**block_record)

        if cap_type:
            cap_obj = get_one_object(cap_type)
            cap_count = calculate_number_of_block_caps(linear_feet=linear_feet, cap_obj=cap_obj)
            cap_record = {'bid': bid_obj,
                          'job_type': job_type,
                          'quantity': cap_count,
                          'cost': cap_obj.cost,
                          'description': cap_obj.description,
                          'total': (cap_obj.cost * cap_count)}
            insert_bid_item(**cap_record)

        if removal_cost:
            removal_cost_record = {'bid': bid_obj,
                                   'job_type': job_type,
                                   'quantity': 1,
                                   'cost': removal_cost,
                                   'description': 'Remove Existing Wall',
                                   'total': removal_cost}
            insert_bid_item(**removal_cost_record)

        if geogrid_type:
            geogrid_obj = get_one_object(geogrid_type)
            geogrid_record = {'bid': bid_obj,
                              'job_type': job_type,
                              'quantity': geogrid_count,
                              'cost': geogrid_obj.cost,
                              'description': geogrid_obj.description,
                              'total': (geogrid_obj.cost * geogrid_count)}
            insert_bid_item(**geogrid_record)

        if rock:
            rock_cubic_yards = calculate_cubic_yards(length=linear_feet, width=height, thickness=12)
            rock_obj = get_one_object(rock)
            rock_record = {'bid': bid_obj,
                           'job_type': job_type,
                           'quantity': rock_cubic_yards,
                           'cost': rock_obj.cost,
                           'description': rock_obj.description,
                           'total': (rock_obj.cost * rock_cubic_yards)}
            insert_bid_item(**rock_record)

        if drain_tile:
            drain_tile_obj = get_one_object(drain_tile)
            drain_tile_record = {'bid': bid_obj,
                                 'job_type': job_type,
                                 'quantity': linear_feet,
                                 'cost': drain_tile_obj.cost,
                                 'description': drain_tile_obj.description,
                                 'total': (drain_tile_obj.cost * linear_feet)}
            insert_bid_item(**drain_tile_record)

        return super(RetainingWallCreate, self).form_valid(form)
