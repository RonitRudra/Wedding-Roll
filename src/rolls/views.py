from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .forms import UploadForm
from .models import Uploads
from users.models import UserAuth
# Create your views here.

class Home(TemplateView):
    template_name='rolls/home.html'


class Upload(TemplateView):
    template_name = 'rolls/upload.html'

    def get(self,request, *args, **kwargs):
        form = UploadForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request, *args, **kwargs):
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            # Poster ID is required, hence assign through request
            obj = form.save(commit=False)
            obj.uploader = request.user
            obj.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your Photo Has Been Uploaded But Will NOT Be Visible Untill Jane Or Joe Approve It.')
            return redirect('rolls:home')
        else:
            messages.add_message(request,messages.ERROR,'File is NOT an Image')
            return redirect('rolls:upload')
        