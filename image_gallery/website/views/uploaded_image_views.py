from .modules import login_required, method_decorator, reverse_lazy, redirect, render, messages
from website.models import UploadedImage
from website.forms import UploadedImageForm, UploadStatusForm
from website.helper import is_user_a_manager


from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse

from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin
from django.core.files.base import ContentFile
from PIL import Image, ExifTags
from io import BytesIO
import os

class UserImagesView(SingleObjectMixin, ListView):
    paginate_by = 10
    template_name = "website/user/uploads.html"
    form = UploadedImageForm
    status = UploadedImage.PENDING
    status_form = UploadStatusForm

    def replace_status(self, temp_status):
        if temp_status is None: return
        for key, value in UploadedImage.STATUS_CHOICES:
            if temp_status == value:
                self.status = value
                break

    def get(self, request, *args, **kwargs):
        self.user_pk = kwargs.get('pk')
        if is_user_a_manager(request.user) or self.user_pk == request.user.pk:
            self.replace_status(request.GET.get('status'))
            self.object = get_object_or_404(User, pk=kwargs.get('pk'))
            return super().get(request, *args, **kwargs)
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        context['upload_form'] = self.form()
        context['status_form'] = self.status_form(initial={'status':self.status})
        context['same_user'] = self.request.user.pk == self.user_pk
        return context

    def get_queryset(self):
        return self.object.uploadedimage_set.filter(status=self.status).order_by('-date_taken')

    def get_proper_dimensions(self, width, height, max=600):
        ratio = min(max/width, max/height)
        new_width = int(width*ratio)
        new_height = int(height*ratio)

        return new_width, new_height

    def rotate_image(self, image):
        try:
            exif=dict((ExifTags.TAGS[k], v) for k, v in image._getexif().items() if k in ExifTags.TAGS)
        except:
            print("Could not resolve photo's metadata. If the photo was taken with the camera in vertical, its thumbnail will be rotated.")
        else:
            orientation = exif.get('Orientation')
            if orientation is not None:
                degrees = 0
                if orientation == 3:
                    degrees = 180
                elif orientation == 6:
                    degrees = 270
                elif orientation == 8:
                    degrees = 90

                return image.rotate(degrees, expand=True)

        return image

    def create_low_quality_img(self, img_data):
        img = Image.open(img_data)
        img_width, img_height = img.size
        new_width, new_height = self.get_proper_dimensions(img_width, img_height)

        img.thumbnail((new_width, new_height))
        img_bytes = BytesIO()

        rotated = self.rotate_image(img)
        rotated.save(img_bytes, format='JPEG')
        return ContentFile(img_bytes.getvalue())

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        context = {'success': False}

        if form.is_valid():
            form.instance.user = self.request.user
            low_quality_img = self.create_low_quality_img(form.instance.upload.file)
            upload_name = os.path.splitext(form.instance.upload.name)[0]
            thumbnail_name = "%s-thumbnail.jpg"%(upload_name)
            form.instance.thumbnail.save(thumbnail_name, low_quality_img)
            if is_user_a_manager(form.instance.user):
                form.instance.status = UploadedImage.ACCEPTED
            form.save()
        else:
            messages.error(request, 'Fill the form correctly!<br/>Make sure you have not selected a future date.')

        return redirect(reverse_lazy('website:user_gallery_view', kwargs={'pk': request.user.pk}))
