from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from category.models import Category
from category.forms import CategoryForm


class CategoryCreate(SuccessMessageMixin, CreateView):
    template_name = 'category/category_form.html'
    form_class = CategoryForm
    success_message = "Successfully Created Category"

    def get_success_url(self):
        return reverse('category_app:category_list')


class CategoryUpdate(SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_message = "Successfully Updated Category"


class CategoryDelete(DeleteView):
    model = Category

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('category_app:category_list')


class CategoryList(ListView):
    model = Category

