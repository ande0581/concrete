from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from bid.models import Bid
from bid_item.models import BidItem
from service.models import Service
from service_group.forms import StandardConcreteForm, DecorativeConcreteForm, StepsForm, FoundationForm, \
    FootingsForm, EgressWindowForm


def calculate_square_feet(length, width):
    square_feet = length * width
    return round(square_feet, 1)


def calculate_cubic_yards(length, width, thickness):
    cubic_yards = (length * width * (thickness / 12)) / 27

    # add 5% extra
    cubic_yards *= 1.05
    return round(cubic_yards, 2)


def get_one_object(service_name):
    obj = Service.objects.get(description=service_name)
    return obj


def insert_bid_item(**item_details):
    item = BidItem(**item_details)
    item.save()


class ConcreteCreate(SuccessMessageMixin, FormView):
    """
    (length x width x thickness) / 27 = yards

    """
    template_name = 'service_group/service_group_form.html'

    def get_success_url(self):
        messages.success(self.request, "Concrete Estimated")
        return reverse('bid_app:bid_update', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):
        # print("POST FORM SAVE:", form.cleaned_data)
        job_type = form.cleaned_data['job_type']
        length = form.cleaned_data['length']
        width = form.cleaned_data['width']
        thickness = form.cleaned_data['thickness']
        concrete = form.cleaned_data['concrete_type']
        washout = form.cleaned_data.get('washout', None)
        rebar = form.cleaned_data['rebar_type']
        removal = form.cleaned_data['removal']
        saw_cutting_qty = form.cleaned_data['saw_cutting']
        expansion_felt_qty = form.cleaned_data['expansion_felt']
        forming = form.cleaned_data['forming']
        fill = form.cleaned_data['fill']
        finishing = form.cleaned_data['finishing']
        stamps = form.cleaned_data.get('stamps', False)
        sealer = form.cleaned_data['sealer']

        sq_ft = calculate_square_feet(length, width)
        cubic_yards = calculate_cubic_yards(length, width, thickness)
        # print('sq_ft:', sq_ft)
        # print('cubic_yards', cubic_yards)
        # print('concrete:', concrete)
        # print('rebar:', rebar)
        # print('removal:', removal)
        # print('saw_cutting:', saw_cutting_qty)
        # print('expansion_felt:', expansion_felt_qty)
        # print('fill:', fill)
        # print('finishing:', finishing)
        # print('sealer:', sealer)
        # print('washout_fee:', washout)
        # print('stamps:', stamps)

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
            stamp_obj = get_one_object('Concrete Stamps')
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


class StepsCreate(SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = StepsForm

    def get_success_url(self):
        messages.success(self.request, "Steps Estimated")
        return reverse('bid_app:bid_update', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        print("POST FORM SAVE:", form.cleaned_data)
        job_type = form.cleaned_data['job_type']
        length = form.cleaned_data['length']
        width = form.cleaned_data['width']
        thickness = form.cleaned_data['thickness']
        num_risers = form.cleaned_data['num_risers']
        concrete = form.cleaned_data['concrete_type']
        removal = form.cleaned_data['removal']
        short_load = form.cleaned_data['short_load']
        railing = form.cleaned_data['railing']
        sealer = form.cleaned_data['sealer']

        cubic_yards = calculate_cubic_yards(length, width, thickness)

        print('job_type:', job_type)
        print('cubic_yards:', cubic_yards)
        print('num_risers:', num_risers)
        print('concrete:', concrete)
        print('removal:', removal)
        print('short_load:', short_load)
        print('railing:', railing)
        print('sealer:', sealer)

        bid_obj = Bid.objects.get(pk=self.kwargs['bid'])

        # TODO figure out step pricing formula

        return super(StepsCreate, self).form_valid(form)


class FoundationCreate(SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = FoundationForm

    def get_success_url(self):
        messages.success(self.request, "Foundation Estimated")
        return reverse('bid_app:bid_update', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        return super(FoundationCreate, self).form_valid(form)


class FootingsCreate(SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = FootingsForm

    def get_success_url(self):
        messages.success(self.request, "Footings Estimated")
        return reverse('bid_app:bid_update', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        return super(FootingsCreate, self).form_valid(form)


class EgressWindowCreate(SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = EgressWindowForm

    def get_success_url(self):
        messages.success(self.request, "Egress Window Estimated")
        return reverse('bid_app:bid_update', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        # print("POST FORM SAVE:", form.cleaned_data)
        job_type = form.cleaned_data['job_type']
        wood = form.cleaned_data['wood']
        dig_out = form.cleaned_data['dig_out']
        flashing = form.cleaned_data['flashing']
        window = form.cleaned_data['window']
        window_well = form.cleaned_data['window_well']
        fasteners = form.cleaned_data['fasteners']
        permit = form.cleaned_data['permit']
        rock = form.cleaned_data['rock']

        # print('job_type:', job_type)
        # print('wood:', wood)
        # print('dig_out:', dig_out)
        # print('flashing:', flashing)
        # print('window:', window)
        # print('window_well', window_well)
        # print('fasteners:', fasteners)
        # print('permit:', permit)
        # print('rock:', rock)

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
