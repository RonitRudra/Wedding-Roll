from django import forms
from django.utils.timezone import now
from users.models import UserAuth



class UserLoginForm(forms.Form):
    """
    Purpose: Facilitate login
	Model Linked: None
	Authentication backend handles appropriate model.
    """
    email = forms.EmailField(max_length=64,label="Email Address")
    password = forms.CharField(max_length=None,widget=forms.widgets.PasswordInput)