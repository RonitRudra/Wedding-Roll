from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from users.models import UserAuth
# Create your models here.


class Uploads(models.Model):
    photo_url = models.ImageField(upload_to='uploaded_files', verbose_name='uploads')
    date_posted = models.DateTimeField(default=now)
    uploader = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    description = models.TextField(default='')

    class Meta:
        verbose_name = _('upload')
        verbose_name_plural = _('uploads')

    def __str__(self):
        return str(self.uploader.email)