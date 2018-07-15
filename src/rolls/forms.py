from django import forms
from .models import Uploads
from users.models import UserAuth

class UploadForm(forms.ModelForm):
    class Meta:
        model = Uploads
        fields = ('photo_url','description')
        exclude = ('uploader','date_posted','is_approved')

    def __init__(self, *args, **kwargs):
        super(UploadForm,self).__init__(*args,**kwargs)
        f = self.fields.get('user_permissions',None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
