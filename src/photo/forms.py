from django import forms
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


class UploadForm(forms.Form):
    attachments = MultiFileField(min_num=1, max_num=10)
