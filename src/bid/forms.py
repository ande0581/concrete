from django import forms
from bid.models import Bid


class BidInitialForm(forms.ModelForm):
    description = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'rows': 3, 'cols': 20}))
    scheduled_bid_date = forms.DateTimeField()

    class Meta:
        model = Bid
        fields = ('description', 'scheduled_bid_date')


class BidForm(forms.ModelForm):
    description = forms.CharField(max_length=2000, help_text="Enter the description")
    scheduled_bid_date = forms.DateTimeField(help_text="Enter the scheduled bid date")

    class Meta:
        model = Bid
        fields = ('description', 'scheduled_bid_date')