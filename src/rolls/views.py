from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import UploadForm
# Create your views here.

class Home(TemplateView):
    template_name='rolls/home.html'

    def get(self,request, *args, **kwargs):
        form = UploadForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request, *args, **kwargs):
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            return redirect('rolls:home')
        else:
            return redirect('home:home')
        