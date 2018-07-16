import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView
from .forms import UploadForm
from .models import Uploads
from users.models import UserAuth
# Create your views here.

class Home(ListView):
    template_name='rolls/home.html'
    model = Uploads

    def get_queryset(self):
        return Uploads.objects.filter(is_approved=True).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_pending'] = Uploads.objects.filter(is_approved=False).count()
        return context



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
            if request.user.is_owner:
                obj.is_approved=True
                messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your Photo Has Been Uploaded!!')
            else:
                messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your Photo Has Been Uploaded But Will NOT Be Visible Untill Jane Or Joe Approve It.')
            obj.save()

            return redirect('rolls:home')
        else:
            messages.add_message(request,messages.ERROR,'File is NOT an Image')
            return redirect('rolls:upload')
      
class Manage(ListView):
    template_name = 'rolls/manage.html'
    model = Uploads

    def get_queryset(self):
        return Uploads.objects.filter(is_approved=False).order_by('-date_posted')

    def post(self,request, *args, **kwargs):
        for key,val in request.POST.items():
            if key == 'csrfmiddlewaretoken':
                pass
            else:
                obj = Uploads.objects.get(id=val)
                print(obj)
                obj.is_approved = True
                obj.save()
        return redirect('rolls:home')

@require_POST
def like(request):
    """
    Not A View that returns an HTML Page.
    Handles AJAX calls from the Like Button.
    """
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug',None)
        photo = get_object_or_404(Uploads,slug=slug)

        if photo.likes.filter(id=user.id).exists():
            photo.likes.remove(user)
        else:
            photo.likes.add(user)

    context = {'likes_count':photo.total_likes}
    return HttpResponse(json.dumps(context),content_type='applications/json')
