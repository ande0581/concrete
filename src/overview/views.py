from django.views.generic.list import ListView

from bid.models import Bid


class OverviewList(ListView):
    model = Bid
    template_name = 'overview/overview_list.html'
    # TODO look at returning query in specified date order

    # def get_queryset(self):
    #     queryset_list = Customer.objects.order_by('name')
    #
    #     return queryset_list
