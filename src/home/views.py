from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from users.models import UserAuth
# Create your views here.

class Home(TemplateView):
	'''
	Contains a login form
	'''
	template_name = 'home/index.html'

	def post(self,request):
		return redirect('rolls:home')

class SignUp(TemplateView):
	template_name = 'home/signup.html'

	def post(self,request):
		email = request.POST['email']
		pw1 = request.POST['password1']
		pw2 = request.POST['password2']
		if pw1 != pw2:
			return redirect('home:signup')
		else:
			try:
				user = UserAuth.objects.create(email=email,password=pw1)
			except:
				return redirect('home:signup')
		messages.add_message(request,messages.SUCCESS,
			'Your Account Has Been Created! Go Ahead and Log in!!')
		return redirect('home:home')
