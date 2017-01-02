from django import forms
from bid.models import Bid


class BidInitialForm(forms.ModelForm):
    description = forms.CharField(max_length=2000, widget=forms.Textarea)
    scheduled_bid_date = forms.DateTimeField(widget=forms.DateTimeInput())

    class Meta:
        model = Bid
        fields = ('description', 'scheduled_bid_date', 'status')


class BidForm(forms.ModelForm):
    description = forms.CharField(max_length=2000, help_text="Please enter the description")
    scheduled_bid_date = forms.DateTimeField(help_text="Please enter the scheduled bid date")

    class Meta:
        model = Bid
        fields = ('description', 'scheduled_bid_date')