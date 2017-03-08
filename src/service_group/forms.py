from django import forms
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Div

from job_type.models import JobType
from service.models import Service

import sys
# http://stackoverflow.com/questions/42024101/problems-with-migrations
# http://stackoverflow.com/questions/39535983/migration-clashes-with-forms-py
if 'makemigrations' in sys.argv or 'migrate' in sys.argv or 'showmigrations' in sys.argv:
    "Prevent querying of DB while initializing the applications, will fail to migrate otherwise"

    def get_queryset(category_name):
        pass


    def get_one_object(service_name):
        pass
else:

    def get_queryset(category_name):
        return Service.objects.all().filter(category__name__exact=category_name)


    def get_one_object(service_name):
        my_obj = Service.objects.get(description=service_name)
        return my_obj.pk


class StandardConcreteForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    length = forms.IntegerField(label='Length in Feet', required=False)
    width = forms.IntegerField(label='Width in Feet', required=False)
    sq_ft = forms.FloatField(label='Enter Square Feet Instead of Length and Width', required=False)
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

    def clean(self):
        cleaned_data = super(StandardConcreteForm, self).clean()
        width = cleaned_data.get('width')
        length = cleaned_data.get('length')
        sq_ft = cleaned_data.get('sq_ft')

        if width and length and sq_ft:
            raise forms.ValidationError('Enter Only Length and Width or Sq_Ft but not both!')

        if not width and not length and not sq_ft:
            raise forms.ValidationError('You must enter Length and Width or Sq_Ft')

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
    length = forms.IntegerField(label='Length in Feet', required=False)
    width = forms.IntegerField(label='Width in Feet', required=False)
    sq_ft = forms.FloatField(label='Enter Square Feet Instead of Length and Width', required=False)
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

    def clean(self):
        cleaned_data = super(DecorativeConcreteForm, self).clean()
        width = cleaned_data.get('width')
        length = cleaned_data.get('length')
        sq_ft = cleaned_data.get('sq_ft')

        if width and length and sq_ft:
            raise forms.ValidationError('Enter Only Length and Width or Sq_Ft but not both!')

        if not width and not length and not sq_ft:
            raise forms.ValidationError('You must enter Length and Width or Sq_Ft')

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
    length = forms.IntegerField(label='Length of Landing in Inches')
    width = forms.IntegerField(label='Width of Landing in Inches')
    num_steps = forms.IntegerField(label='Total Number of Steps, Count the Landing as a Step')
    concrete_type = forms.ModelChoiceField(queryset=get_queryset('Concrete'),
                                           initial=get_one_object('Concrete Steps'))
    removal = forms.FloatField(label='Cost to Remove Existing Steps or Blank for None', required=False)
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


class FloatingSlabForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    length = forms.IntegerField(label='Length in Feet')
    width = forms.IntegerField(label='Width in Feet')
    thickness = forms.IntegerField(label='Thickness in Inches', initial=4)
    concrete_type = forms.ModelChoiceField(queryset=get_queryset('Concrete'),
                                           initial=get_one_object('Concrete Floating Slab'))
    rebar_type = forms.ModelChoiceField(queryset=get_queryset('Rebar'), required=False,
                                        initial=get_one_object('Rebar 1/2 Non-Coated'))
    forming = forms.ModelChoiceField(queryset=get_queryset('Forming'), required=False,
                                     initial=get_one_object('Forming, Grading and Setup Floating Slab'))
    finishing = forms.ModelChoiceField(queryset=get_queryset('Finishing'),
                                       initial=get_one_object('Pour, Finish, Control Joints Floating Slab'))
    sealer = forms.ModelChoiceField(queryset=get_queryset('Sealer'), required=False,
                                    initial=get_one_object('Sealer - Cure n Seal'))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Floating Slab', css_class='btn=primary'))


class BlockFoundationForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    linear_feet = forms.FloatField(label='Linear Feet')
    width = forms.ChoiceField(label='Width', choices=((8, "8 inches"), (12, "12 Inches")))
    height = forms.FloatField(label='Height of Foundation in Inches')
    concrete = forms.ModelChoiceField(queryset=get_queryset('Concrete'),
                                      initial=get_one_object('Concrete Block Foundation'))
    rebar_type = forms.ModelChoiceField(queryset=get_queryset('Rebar'), required=False,
                                        initial=get_one_object('Rebar 1/2 Non-Coated Block Foundation'))
    forming = forms.ModelChoiceField(queryset=get_queryset('Forming'), required=False,
                                     initial=get_one_object('Forming, Grading and Setup Block Foundation'))
    finishing = forms.ModelChoiceField(queryset=get_queryset('Finishing'),
                                       initial=get_one_object('Pour, Finish, Control Joints Block Foundation'))
    backhoe = forms.BooleanField(required=False, initial=False)
    waterproofing = forms.BooleanField(required=False, initial=False)
    pump_truck = forms.BooleanField(required=False, initial=False)
    bobcat_hours = forms.IntegerField(label='Enter Number of Hours for Bobcat Work or Blank for None', required=False)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Block Foundation', css_class='btn=primary'))

    """
    length
    width
    height
    removal_sqft
    removal_unit
    add_footing to this form


      -Block foundation- Footing included. I just need to enter in linear feet and put a value to that.
      Footings are always the same linear feet as the foundation. The only difference would be 8" or 12" wide
      foundation. It would be nice to have the concrete volume come up automatically so i don't have to figure out how
      much concrete to order every time. 8 inches thick divided by 41 square feet. Foundation = Length x Height divided
      by 41, plus footing = 20" wide(always) x 12" thick(always) x total linear length. 12 inches thick divided by 27
      square feet. I can put a value on the concrete volume figured.


    """


class PierFootingsForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    length = forms.IntegerField(label='Length of Footing in Inches')
    width = forms.IntegerField(label='Width of Footing in Inches')
    height = forms.IntegerField(label='Depth of Footing in Inches')
    auger = forms.BooleanField(required=False, initial=True)
    sonotube = forms.BooleanField(required=False, initial=True)
    quantity = forms.IntegerField(label='Number of Footings')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Egress Window', css_class='btn=primary'))

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


class RetainingWallForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    linear_foot = forms.IntegerField(label='Enter Linear Feet of Wall')
    height = forms.IntegerField(label='Enter Height of Wall in Feet')
    block_type = forms.ModelChoiceField(queryset=get_queryset('Block'))
    cap_type = forms.ModelChoiceField(queryset=get_queryset('Block'), required=False)

    removal_cost = forms.FloatField(label='Enter Price to Remove Existing Wall', required=False)
    geogrid = forms.IntegerField(label='Enter number of rolls of GeoGrid', required=False)
    rock = forms.BooleanField(initial=False)
    drain_tile = forms.BooleanField(initial=False)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Retaining Wall', css_class='btn=primary'))