from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from bid.models import Bid


class OverviewList(LoginRequiredMixin, ListView):
    model = Bid
    template_name = 'overview/overview_list.html'

    # login_url = "/account/login/"
    # redirect_field_name = "jimmy"
    # #raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(OverviewList, self).get_context_data(**kwargs)
        bid_obj_list = Bid.objects.all()
        context['jobs_needing_bid'] = bid_obj_list.filter(status='Needs Bid').order_by('scheduled_bid_date')
        context['jobs_in_progress'] = bid_obj_list.filter(status='Job Started').order_by('actual_start')
        context['jobs_in_queue'] = bid_obj_list.filter(status='Job Accepted').order_by('tentative_start')
        context['jobs_awaiting_acceptance'] = bid_obj_list.filter(status='Awaiting Customer Acceptance')\
            .order_by('-scheduled_bid_date')

        return context
