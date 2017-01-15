from django import forms
from service.models import Service

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div


def get_queryset(category_name):
    return Service.objects.all().filter(category__name__exact=category_name)


def get_one_object(service_name):
    my_obj = Service.objects.get(description=service_name)
    return my_obj.pk


class DrivewayForm(forms.Form):
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


class ColoredConcrete(forms.Form):
    pass

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


class Steps(forms.Form):
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


class Foundation(forms.Form):
    pass

    """
    length
    width
    height
    removal_sqft
    removal_unit
    add_footing to this form
    """


class Footings(forms.Form):
    pass

    """
    length
    width
    height
    """


class Pillars(forms.Form):
    pass

    """
    wait on this one
    """


class Tuckpointing(forms.Form):
    pass

    """
    wait on this one
    """


class EgressWindow(forms.Form):
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
