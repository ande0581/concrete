from django import forms
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div

from service.models import Service


def get_queryset(category_name):
    return Service.objects.all().filter(category__name__exact=category_name)


def get_one_object(service_name):
    my_obj = Service.objects.get(description=service_name)
    return my_obj.pk


class StandardConcreteForm(forms.Form):
# TODO http://stackoverflow.com/questions/32383978/no-such-column-error-in-django-models, an issue??

    job_type = forms.CharField(label='description of job being performed')
    length = forms.IntegerField(label='Length in Feet')
    width = forms.IntegerField(label='Width in Feet')
    thickness = forms.IntegerField(label='Thickness in Inches', initial=4)
    concrete_type = forms.ModelChoiceField(queryset=get_queryset('Concrete'),
                                           initial=get_one_object('Concrete Driveway Mix'))
    rebar_type = forms.ModelChoiceField(queryset=get_queryset('Rebar'), required=False,
                                        initial=get_one_object('Rebar 1/2 Non-Coated'))
    removal = forms.ModelChoiceField(queryset=get_queryset('Removal-Square-Foot'), required=False,
                                     initial=get_one_object('Removal - Concrete/Tar'))
    saw_cutting = forms.IntegerField(label='Saw Cutting in Feet or Blank for None', required=False)
    forming = forms.ModelChoiceField(queryset=get_queryset('Forming'), required=False,
                                     initial=get_one_object('Forming, Grading and Setup'))
    expansion_felt = forms.IntegerField(label='Expansion Felt in Feet or Blank for None', required=False)
    fill = forms.ModelChoiceField(queryset=get_queryset('Fill'), required=False, empty_label="(Nothing)")
    finishing = forms.ModelChoiceField(queryset=get_queryset('Finishing'),
                                       initial=get_one_object('Pour, Finish, Control Joints'))
    sealer = forms.ModelChoiceField(queryset=get_queryset('Sealer'), required=False,
                                    initial=get_one_object('Sealer - Cure n Seal'))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Driveway', css_class='btn=primary'))



    """
    1. removal -required(no), default=Removal - Concrete/Tar (sq/ft)
    2. saw cutting  -required(no), default=nothing
    3. forming grading and setup - required(no), default=Forming / Grading / Setup (sq/ft)
    3.1 fill - required(no), default(none)
    4. rebar - required(no), default (1/2 non-coated), option for none
    5. felt - required(no), float field
    5.1 pour finish control joint - required=true, default=calculated on sq
    6. cement (min load load charge, less than 5 yards), add %5 extra, required=yes
    7. sealer (required=no), default=(Sealer - Cure n Seal)
    """


class DecorativeConcreteForm(forms.Form):

    length = forms.IntegerField(label='Length in Feet')
    width = forms.IntegerField(label='Width in Feet')
    thickness = forms.IntegerField(label='Thickness in Inches', initial=4)
    concrete_type = forms.ModelChoiceField(queryset=get_queryset('Concrete'),
                                           initial=get_one_object('Concrete Colored $$'))
    rebar_type = forms.ModelChoiceField(queryset=get_queryset('Rebar'), required=False,
                                        initial=get_one_object('Rebar 1/2 Non-Coated'))
    removal = forms.ModelChoiceField(queryset=get_queryset('Removal-Square-Foot'), required=False,
                                     initial=get_one_object('Removal - Concrete/Tar'))
    saw_cutting = forms.IntegerField(label='Saw Cutting in Feet or Blank for None', required=False)
    forming = forms.ModelChoiceField(queryset=get_queryset('Forming'), required=False,
                                     initial=get_one_object('Forming, Grading and Setup'))
    expansion_felt = forms.IntegerField(label='Expansion Felt in Feet or Blank for None', required=False)
    fill = forms.ModelChoiceField(queryset=get_queryset('Fill'), required=False, empty_label="(Nothing)")
    finishing = forms.ModelChoiceField(queryset=get_queryset('Finishing'),
                                       initial=get_one_object('Pour, Finish, Control Joints Colored/Stamped'))
    stamps = forms.BooleanField(required=True, initial=False)
    sealer = forms.ModelChoiceField(queryset=get_queryset('Sealer'), required=False,
                                    initial=get_one_object('Sealer - Lumiseal Plus'))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Driveway', css_class='btn=primary'))

    """
    1. removal -required(no), default=Removal - Concrete/Tar (sq/ft).
    2. saw cutting  -required(no), default=nothing
    3. forming grading and setup - required(no), default=Forming / Grading / Setup (sq/ft)
    3.1 fill - required(no), default(none)
    4. rebar - required(no), default (1/2 non-coated), option for none
    5. felt - required(no), float field
    5.1 pour finish control joint - required=true, default=calculated on sq, more expensive for colored
    6. cement (min load load charge, less than 5 yards), add %5 extra, required=yes, more expensive
    7. colored washout fee ($60), always
    8. stamps (true/false)
    9 7. sealer (required=no), default=(Sealer - Lumiseal +)
    """


class StepsForm(forms.Form):
    pass

    """
    length (required)
    width (required)
    risers (int, required)
    removal = float field
    short_load_fee = true/false, default=none
    railing (required=no, default=none)
    sealer (required=no), default=(Sealer - Lumiseal +)
    """


class FoundationForm(forms.Form):
    pass

    """
    length
    width
    height
    removal_sqft
    removal_unit
    add_footing to this form
    """


class FootingsForm(forms.Form):
    pass

    """
    length
    width
    height
    """


class EgressWindowForm(forms.Form):
    pass

    """
    treated_wood, always true (value=?)
    digging out, always true (value=?)
    flashing (always true (value=?)
    window = (always true (std window)
    window well includes ladder (pick list)
    fasteners (always true, value(you provide)
    building permits (always true, $120)
    rock 3/8- rock (always true, flat rate)

    """
