from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.hashers import make_password

from .forms import UserLoginForm
from users.models import UserAuth
# Create your views here.

class Redir(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect('home:home')

class Home(TemplateView):
    '''
    Contains a login form
    '''
    template_name = 'home/index.html'

    def post(self,request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            try:
                email = UserAuth.objects.get(email=form.cleaned_data['email'])
                password = form.cleaned_data['password']
                user = authenticate(username=email,password=password)
                if user is None:
                    raise ValidationError(message='Validation Failed')
            except (ObjectDoesNotExist,ValidationError):
                messages.add_message(request,messages.ERROR,'Username Or Password Does Not Match')
                return redirect('home:home')
            login(request,user)
            messages.add_message(request,messages.SUCCESS,'You Have Been Logged In!')
            return redirect('rolls:home')
        else:
            messages.add_message(request,messages.ERROR,'Invalid Form')
            return redirect('home:home')

class SignUp(TemplateView):
    template_name = 'home/signup.html'

    def post(self,request):
        email = request.POST['email']
        pw1 = request.POST['password1']
        pw2 = request.POST['password2']
        if pw1 != pw2:
            messages.add_message(request,messages.ERROR,'Passwords Do Not Match!')
            return redirect('home:signup')
        else:
            try:
                pw = make_password(pw1)
                user = UserAuth.objects.create(email=email,password=pw)
            except:
                messages.add_message(request,messages.ERROR,'User Already Exists')
                return redirect('home:signup')
            messages.add_message(request,messages.SUCCESS,
		    'Your Account Has Been Created! Go Ahead and Log in!!')
            return redirect('home:home')


class Logout(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request,messages.SUCCESS,'You Have Been Logged Out!')
        return redirect('home:home')