from django import forms
from .models import Uploads

class UploadForm(forms.Form):
    photo_url = forms.ImageField()