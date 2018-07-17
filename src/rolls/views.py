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

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs['order'] not in [None,'date-desc',
                                        'date-asc','likes-desc',
                                        'likes-asc']:
            return redirect('rolls:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query_set = Uploads.objects.filter(is_approved=True)
        query = self.kwargs['order']
        if query is not None:
            if query == 'date-desc':
                return query_set.order_by('-date_posted') 
            elif query == 'date-asc':
                return query_set.order_by('date_posted') 
            elif query == 'likes-desc':
                return query_set.order_by('-total') 
            elif query == 'likes-asc':  
                return query_set.order_by('total')
        else:
            return query_set

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

    def get(self, request, *args, **kwargs):
        if request.user.is_owner:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('rolls:home')

    def get_queryset(self):
        return Uploads.objects.filter(is_approved=False).order_by('-date_posted')

    def post(self,request, *args, **kwargs):
        if request.user.is_owner:
            for key,val in request.POST.items():
                if key == 'csrfmiddlewaretoken':
                    pass
                else:
                    obj = Uploads.objects.get(id=val)
                    print(obj)
                    obj.is_approved = True
                    obj.save()
            return redirect('rolls:home')
        else:
            return redirect('home:home')

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
            photo.total -=1
            photo.save()
        else:
            photo.likes.add(user)
            photo.total+=1
            photo.save()

    context = {'likes_count':photo.total_likes}
    return HttpResponse(json.dumps(context),content_type='applications/json')
