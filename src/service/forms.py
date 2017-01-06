from django import forms
from service.models import Service
from category.models import Category


class ServiceForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Service
        fields = ('description', 'cost', 'category')

    # def save(self, commit=True, *args, **kwargs):
    #     obj = super(ServiceForm, self).save(commit=False, *args, **kwargs)
    #
    #     print('object.category:', obj.category_id)
    #     #print('object.id:', obj.id)
    #
    #     #obj.category_id = obj.category_id.id
    #
    #     if commit:
    #         obj.save()
    #     return obj


