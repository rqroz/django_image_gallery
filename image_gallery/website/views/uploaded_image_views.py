from .modules import CreateView, login_required, method_decorator, reverse_lazy
from website.models import UploadedImage
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

@method_decorator(login_required, name='dispatch')
class UploadedImageView(CreateView):
    model = UploadedImage
    fields = ['upload', 'date_taken']
    template_name = 'website/user_uploads.html'
    success_url = reverse_lazy('website:upload_img_view')

    def create_low_quality_img(self, img_data):
        img = Image.open(img_data)
        print(img)
        img_width, img_height = img.size
        new_width = 250
        new_height = int(img_height * (new_width/img_width)); # keep proportion

        resized_img = img.resize((new_width, new_height))
        img_bytes = BytesIO()
        resized_img.save(img_bytes, format='JPEG', quality=100)
        print(resized_img)
        cf = ContentFile(img_bytes.getvalue())
        print(cf)
        return cf


    def form_valid(self, form):
         form.instance.user = self.request.user
         low_quality_img = self.create_low_quality_img(form.cleaned_data['upload'])

         form.instance.sample.save('sample.jpg', low_quality_img)
         return super(UploadedImageView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UploadedImageView, self).get_context_data(**kwargs)
        uploads = UploadedImage.objects.filter(user=self.request.user)
        context['uploaded_images'] = uploads
        return context
