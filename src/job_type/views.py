from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from job_type.models import JobType
from job_type.forms import JobTypeForm


class JobTypeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'job_type/jobtype_form.html'
    form_class = JobTypeForm
    success_message = "Successfully Created Job Type"

    def get_success_url(self):
        return reverse('job_type_app:job_type_list')


class JobTypeUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = JobType
    form_class = JobTypeForm
    success_message = "Successfully Updated Job Type"


class JobTypeDelete(LoginRequiredMixin, DeleteView):
    model = JobType

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('job_type_app:job_type_list')


class JobTypeList(LoginRequiredMixin, ListView):
    model = JobType

    def get_queryset(self):
        queryset_list = JobType.objects.order_by('description')
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(description__icontains=query)
               ).distinct()

        return queryset_list



