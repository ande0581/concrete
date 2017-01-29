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
    return round(cubic_yards, 2)


def get_one_object(service_name):
    obj = Service.objects.get(description=service_name)
    return obj


def insert_bid_item(**item_details):
    item = BidItem(**item_details)
    item.save()


class StandardConcreteCreate(SuccessMessageMixin, FormView):
    """
    (length x width x thickness) / 27 = yards

    """
    template_name = 'service_group/service_group_form.html'
    form_class = StandardConcreteForm

    def get_success_url(self):
        messages.success(self.request, "Standard Concrete Estimated")
        return reverse('bid_app:bid_update', kwargs={'pk': self.kwargs['bid']})

    # def get_context_data(self, **kwargs):
    #     context = super(DrivewayCreate, self).get_context_data(**kwargs)
    #     #print('VIEW:', context['view'])
    #     #print('FORM:', context['form'])
    #     return context

    def form_valid(self, form):
        #print('%%%%%%%', form.__dict__)
        print("POST FORM SAVE:", form.cleaned_data)
        length = form.cleaned_data['length']
        width = form.cleaned_data['width']
        thickness = form.cleaned_data['thickness']
        concrete = form.cleaned_data['concrete_type']
        rebar = form.cleaned_data['rebar_type']
        removal = form.cleaned_data['removal']
        saw_cutting_qty = form.cleaned_data['saw_cutting']
        expansion_felt_qty = form.cleaned_data['expansion_felt']
        forming = form.cleaned_data['forming']
        fill = form.cleaned_data['fill']
        finishing = form.cleaned_data['finishing']
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

        bid_obj = Bid.objects.get(pk=self.kwargs['bid'])

        concrete_obj = get_one_object(concrete)
        concrete_record = {'bid': bid_obj,
                           'quantity': cubic_yards,
                           'cost': concrete_obj.cost,
                           'description': concrete_obj.description,
                           'total': (concrete_obj.cost * cubic_yards)}
        insert_bid_item(**concrete_record)

        if rebar:
            rebar_obj = get_one_object(rebar)
            rebar_record = {'bid': bid_obj,
                            'quantity': sq_ft,
                            'cost': rebar_obj.cost,
                            'description': rebar_obj.description,
                            'total': (rebar_obj.cost * sq_ft)}
            insert_bid_item(**rebar_record)

        if removal:
            removal_obj = get_one_object(removal)
            removal_record = {'bid': bid_obj,
                              'quantity': sq_ft,
                              'cost': removal_obj.cost,
                              'description': removal_obj.description,
                              'total': (removal_obj.cost * sq_ft)}
            insert_bid_item(**removal_record)

        if saw_cutting_qty:
            saw_cutting_obj = get_one_object('Saw Cutting')
            saw_cutting_record = {'bid': bid_obj,
                                  'quantity': saw_cutting_qty,
                                  'cost': saw_cutting_obj.cost,
                                  'description': saw_cutting_obj.description,
                                  'total': (saw_cutting_obj.cost * saw_cutting_qty)}
            insert_bid_item(**saw_cutting_record)

        if forming:
            forming_obj = get_one_object(forming)
            forming_record = {'bid': bid_obj,
                              'quantity': sq_ft,
                              'cost': forming_obj.cost,
                              'description': forming_obj.description,
                              'total': (forming_obj.cost * sq_ft)}
            insert_bid_item(**forming_record)

        if expansion_felt_qty:
            expansion_felt_obj = get_one_object('Expansion Felt')
            expansion_felt_record = {'bid': bid_obj,
                                     'quantity': expansion_felt_qty,
                                     'cost': expansion_felt_obj.cost,
                                     'description': expansion_felt_obj.description,
                                     'total': (expansion_felt_obj.cost * expansion_felt_qty)}
            insert_bid_item(**expansion_felt_record)

        if fill:
            fill_obj = get_one_object(fill)
            fill_record = {'bid': bid_obj,
                           'quantity': 1,
                           'cost': fill_obj.cost,
                           'description': fill_obj.description,
                           'total': fill_obj.cost}
            insert_bid_item(**fill_record)

        finishing_obj = get_one_object(finishing)
        finishing_record = {'bid': bid_obj,
                            'quantity': sq_ft,
                            'cost': finishing_obj.cost,
                            'description': finishing_obj.description,
                            'total': (finishing_obj.cost * sq_ft)}
        insert_bid_item(**finishing_record)

        if sealer:
            sealer_obj = get_one_object(sealer)
            sealer_record = {'bid': bid_obj,
                             'quantity': sq_ft,
                             'cost': sealer_obj.cost,
                             'description': sealer_obj.description,
                             'total': (sealer_obj.cost * sq_ft)}
            insert_bid_item(**sealer_record)

        return super(StandardConcreteCreate, self).form_valid(form)


class DecorativeConcreteCreate(SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = DecorativeConcreteForm

    def get_success_url(self):
        messages.success(self.request, "Decorative Concrete Estimated")
        return reverse('bid_app:bid_update', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

        return super(DecorativeConcreteCreate, self).form_valid(form)


class StepsCreate(SuccessMessageMixin, FormView):

    template_name = 'service_group/service_group_form.html'
    form_class = StepsForm

    def get_success_url(self):
        messages.success(self.request, "Steps Estimated")
        return reverse('bid_app:bid_update', kwargs={'pk': self.kwargs['bid']})

    def form_valid(self, form):

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

        return super(EgressWindowCreate, self).form_valid(form)
