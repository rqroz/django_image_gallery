from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from website.models import UploadedImage

# Create your views here.
class IndexView(View):
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class UploadedImageView(CreateView):
    model = UploadedImage
    fields = ['upload']
    template_name = 'website/test.html'
    success_url = reverse_lazy('website:upload_img_view')

    def form_valid(self, form):
         form.instance.user = self.request.user
         return super(UploadedImageView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UploadedImageView, self).get_context_data(**kwargs)
        uploads = UploadedImage.objects.all()
        context['uploaded_images'] = uploads
        return context
