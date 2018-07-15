from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
# Create your views here.

class Home(TemplateView):
	template_name = 'home/index.html'

class SignUp(TemplateView):
	template_name = 'home/signup.html'

	def post(self,request):
		messages.add_message(request,messages.SUCCESS,
			'Your Account Has Been Created! Go Ahead and Log in!!')
		return redirect('home:home')