from django.conf.urls import url
from .views import Home, SignUp, Logout

# New in Django 2.0
# the app_name attribute needs to be set to facilitate include in root urls.py
app_name = 'home'

urlpatterns = [url(r'^$',Home.as_view(),name='home'), 
               url(r'^signup/$',SignUp.as_view(),name='signup'),
               url(r'^logout/$',Logout.as_view(),name='logout'),
    ]