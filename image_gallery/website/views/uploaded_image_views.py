from .modules import CreateView, login_required, method_decorator, reverse_lazy
from website.models import UploadedImage

@method_decorator(login_required, name='dispatch')
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
