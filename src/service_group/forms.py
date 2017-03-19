from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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
    stamps = forms.ModelChoiceField(queryset=get_queryset('Stamps'), required=False)
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


class StepsForm(forms.Form):
    """
    standard step depth is 12"
    standard step height is 7.5"
    """

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


class FloatingSlabForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    length = forms.IntegerField(label='Length in Feet')
    width = forms.IntegerField(label='Width in Feet')
    thickness = forms.IntegerField(label='Thickness in Inches', initial=4)
    concrete_type = forms.ModelChoiceField(queryset=get_queryset('Concrete'),
                                           initial=get_one_object('Concrete Floating Slab Mix'))
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
                                      initial=get_one_object('Concrete Block Foundation Mix'))
    rebar_type = forms.ModelChoiceField(queryset=get_queryset('Rebar'), required=False,
                                        initial=get_one_object('Rebar 1/2 Non-Coated Block Foundation'))
    forming = forms.ModelChoiceField(queryset=get_queryset('Forming'), required=False,
                                     initial=get_one_object('Forming, Grading and Setup Block Foundation'))
    finishing = forms.ModelChoiceField(queryset=get_queryset('Finishing'),
                                       initial=get_one_object('Pour, Finish, Control Joints Block Foundation'))
    backhoe = forms.ModelChoiceField(queryset=get_queryset('Backhoe'), required=False)
    waterproofing = forms.ModelChoiceField(queryset=get_queryset('Waterproofing'), required=False)
    pump_truck = forms.ModelChoiceField(queryset=get_queryset('Pump-Truck'), required=False)
    bobcat_hours = forms.IntegerField(label='Enter Number of Hours for Bobcat Work or Blank for None', required=False)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Block Foundation', css_class='btn=primary'))


class PierFootingsForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    diameter = forms.IntegerField(label='Diameter of Footing in Inches')
    depth = forms.IntegerField(label='Depth of Footing in Inches')
    concrete = forms.ModelChoiceField(queryset=get_queryset('Concrete'),
                                      initial=get_one_object('Concrete Pier Footings Mix'))
    auger = forms.ModelChoiceField(queryset=get_queryset('Auger'), required=False)
    sonotube = forms.ModelChoiceField(queryset=get_queryset('Sonotube'), required=False)
    setup = forms.FloatField(label='Labor Cost Per Hole in Dollars For Setup')
    quantity = forms.IntegerField(label='Number of Footings')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Pier Footings', css_class='btn=primary'))


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


class RetainingWallForm(forms.Form):

    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    linear_feet = forms.IntegerField(label='Enter Linear Feet of Wall')
    height = forms.IntegerField(label='Enter Height of Wall in Feet')
    block_type = forms.ModelChoiceField(queryset=get_queryset('Block'))
    cap_type = forms.ModelChoiceField(queryset=get_queryset('Block-Cap'), required=False)

    removal_cost = forms.FloatField(label='Enter Price to Remove Existing Wall', required=False)
    geogrid_type = forms.ModelChoiceField(queryset=get_queryset('GeoGrid'), required=False)
    geogrid_count = forms.IntegerField(label='Enter number of rolls of GeoGrid', required=False)
    rock = forms.ModelChoiceField(queryset=get_queryset('Rock'), required=False)
    drain_tile = forms.ModelChoiceField(queryset=get_queryset('Drain-Tile'), required=False)

    def clean(self):
        """
        If using GeoGrid, make sure both GeoGrid Type and Number of Rolls are Populated
        """
        cleaned_data = super(RetainingWallForm, self).clean()
        geogrid_type = cleaned_data.get('geogrid_type')
        geogrid_count = cleaned_data.get('geogrid_count')

        if (geogrid_type and not geogrid_count) or (geogrid_count and not geogrid_type):
            raise forms.ValidationError('GeoGrid Type and GeoGrid Roll Count are Both Required!')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Bid Retaining Wall', css_class='btn=primary'))