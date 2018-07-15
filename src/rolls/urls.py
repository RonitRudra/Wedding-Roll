from django.conf.urls import url
from .views import Home

# New in Django 2.0
# the app_name attribute needs to be set to facilitate include in root urls.py
app_name = 'rolls'

urlpatterns = [url(r'^$',Home.as_view(),name='home'), 
]