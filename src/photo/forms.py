from django import forms
from multiupload.fields import MultiFileField


class UploadForm(forms.Form):
    attachments = MultiFileField(min_num=1, max_num=10, help_text='You can upload multiple photos at the same time.')
