from django import forms
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div

from job_type.models import JobType
from service.models import Service


def get_queryset(category_name):
    return Service.objects.all().filter(category__name__exact=category_name)


def get_one_object(service_name):
    my_obj = Service.objects.get(description=service_name)
    return my_obj.pk


class StandardConcreteForm(forms.Form):
# TODO http://stackoverflow.com/questions/32383978/no-such-column-error-in-django-models, an issue??

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
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
    fill = forms.ModelChoiceField(queryset=get_queryset('Fill'), required=False)
    finishing = forms.ModelChoiceField(queryset=get_queryset('Finishing'),
                                       initial=get_one_object('Pour, Finish, Control Joints'))
    sealer = forms.ModelChoiceField(queryset=get_queryset('Sealer'), required=False,
                                    initial=get_one_object('Sealer - Cure n Seal'))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Standard Concrete', css_class='btn=primary'))



    """
    x1. removal -required(no), default=Removal - Concrete/Tar (sq/ft)
    x2. saw cutting  -required(no), default=nothing
    x3. forming grading and setup - required(no), default=Forming / Grading / Setup (sq/ft)
    x3.1 fill - required(no), default(none)
    x4. rebar - required(no), default (1/2 non-coated), option for none
    x5. felt - required(no), float field
    x5.1 pour finish control joint - required=true, default=calculated on sq
    x6. cement (min load load charge, less than 5 yards), add %5 extra, required=yes
    x7. sealer (required=no), default=(Sealer - Cure n Seal)
    """


class DecorativeConcreteForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    length = forms.IntegerField(label='Length in Feet')
    width = forms.IntegerField(label='Width in Feet')
    thickness = forms.IntegerField(label='Thickness in Inches', initial=4)
    concrete_type = forms.ModelChoiceField(queryset=get_queryset('Concrete'),
                                           initial=get_one_object('Concrete Colored $$'))
    washout = forms.ModelChoiceField(queryset=get_queryset('Washout'),
                                     initial=get_one_object('Concrete Truck Washout Fee'))
    rebar_type = forms.ModelChoiceField(queryset=get_queryset('Rebar'), required=False,
                                        initial=get_one_object('Rebar 1/2 Non-Coated'))
    removal = forms.ModelChoiceField(queryset=get_queryset('Removal-Square-Foot'), required=False,
                                     initial=get_one_object('Removal - Concrete/Tar'))
    saw_cutting = forms.IntegerField(label='Saw Cutting in Feet or Blank for None', required=False)
    forming = forms.ModelChoiceField(queryset=get_queryset('Forming'), required=False,
                                     initial=get_one_object('Forming, Grading and Setup'))
    expansion_felt = forms.IntegerField(label='Expansion Felt in Feet or Blank for None', required=False)
    fill = forms.ModelChoiceField(queryset=get_queryset('Fill'), required=False)
    finishing = forms.ModelChoiceField(queryset=get_queryset('Finishing'),
                                       initial=get_one_object('Pour, Finish, Control Joints Colored/Stamped'))
    stamps = forms.BooleanField(required=False)
    sealer = forms.ModelChoiceField(queryset=get_queryset('Sealer'), required=False,
                                    initial=get_one_object('Sealer - Lumiseal Plus'))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Decorative Concrete', css_class='btn=primary'))

    """
    x1. removal -required(no), default=Removal - Concrete/Tar (sq/ft).
    x2. saw cutting  -required(no), default=nothing
    x3. forming grading and setup - required(no), default=Forming / Grading / Setup (sq/ft)
    x3.1 fill - required(no), default(none)
    x4. rebar - required(no), default (1/2 non-coated), option for none
    x5. felt - required(no), float field
    x5.1 pour finish control joint - required=true, default=calculated on sq, more expensive for colored
    x6. cement (min load load charge, less than 5 yards), add %5 extra, required=yes, more expensive
    x7. colored washout fee ($60), always
    x8. stamps (true/false)
    x9  sealer (required=no), default=(Sealer - Lumiseal +)
    """


class StepsForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    length = forms.IntegerField(label='Depth of Steps in Feet')
    width = forms.IntegerField(label='Width of Steps in Feet')
    thickness = forms.IntegerField(label='Height of Steps in Inches')
    num_risers = forms.IntegerField(label='Total Number of Steps')
    concrete_type = forms.ModelChoiceField(queryset=get_queryset('Concrete'),
                                           initial=get_one_object('Concrete Driveway Mix'))
    removal = forms.FloatField(label='Cost to Remove Existing Steps or Blank for None')
    short_load = forms.BooleanField(required=False)
    railing = forms.ModelChoiceField(queryset=get_queryset('Railing'), required=False)
    sealer = forms.ModelChoiceField(queryset=get_queryset('Sealer'), required=False,
                                    initial=get_one_object('Sealer - Lumiseal Plus'))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Steps', css_class='btn=primary'))

    """
    xlength (required)
    xwidth (required)
    xthickness (required)
    xrisers (int, required)
    xremoval = float field
    xshort_load_fee = true/false, default=none
    xrailing (required=no, default=none)
    xsealer (required=no), default=(Sealer - Lumiseal +)

    revised 2/9/2017
    landing width
    landing depth
    standard step depth is 12"
    standard step height is 7.5"
    recursion
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

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    length = forms.IntegerField(label='Length of Footing')
    width = forms.IntegerField(label='Width of Footing')
    thickness = forms.IntegerField(label='Depth of Footing')
    quantity = forms.IntegerField(label='Number of Footings')

    """
    length
    width
    height
    quantity
    """


class EgressWindowForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    wood = forms.ModelChoiceField(queryset=get_queryset('Wood'),
                                  initial=get_one_object('Pressure Treated Wood'))
    dig_out = forms.ModelChoiceField(queryset=get_queryset('Window-Dig-Out'),
                                     initial=get_one_object('Dig Out Window Well'))
    flashing = forms.ModelChoiceField(queryset=get_queryset('Flashing'),
                                      initial=get_one_object('Flashing'))
    window = forms.ModelChoiceField(queryset=get_queryset('Window'),
                                    initial=get_one_object('Standard Egress Window'))
    window_well = forms.ModelChoiceField(queryset=get_queryset('Window-Well'),
                                         initial=get_one_object('Standard Window Well'))
    fasteners = forms.ModelChoiceField(queryset=get_queryset('Fasteners'),
                                       initial=get_one_object('Window Fasteners'))
    permit = forms.ModelChoiceField(queryset=get_queryset('Permit'),
                                    initial=get_one_object('Egress Window Building Permit'), required=False)
    rock = forms.ModelChoiceField(queryset=get_queryset('Rock'),
                                  initial=get_one_object('Rock for Window Well'))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Egress Window', css_class='btn=primary'))


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


# Place holder to start db from nothing
# class StandardConcreteForm:
#     pass
#
#
# class DecorativeConcreteForm:
#     pass
#
#
# class StepsForm:
#     pass
#
#
# class FoundationForm:
#     pass
#
#
# class FootingsForm:
#     pass
#
#
# class EgressWindowForm:
#     pass