from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .forms import UploadForm
from users.models import UserAuth
# Create your views here.

class Home(TemplateView):
    template_name='rolls/home.html'

    def get(self,request, *args, **kwargs):
        form = UploadForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request, *args, **kwargs):
        form=UploadForm(request.POST,request.FILES,instance=UserAuth.objects.get(email=request.user))
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Your Photo Was Uploaded!')
            return redirect('rolls:home')
        else:
            messages.add_message(request,messages.ERROR,'File is NOT an Image')
            return redirect('home:home')
        