from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Category
from .forms import CategoryForm


class CategoryCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'category/category_form.html'
    form_class = CategoryForm
    success_message = "Successfully Created Category"

    def get_success_url(self):
        return reverse('category_app:category_list')


class CategoryUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_message = "Successfully Updated Category"


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category

    def get_object(self, queryset=None):
        # Do not allow the deletion of a protected category which is hardcoded in queries
        obj = super(CategoryDelete, self).get_object()
        if obj.protected:
            raise PermissionDenied()
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('category_app:category_list')


class CategoryList(LoginRequiredMixin, ListView):
    model = Category

