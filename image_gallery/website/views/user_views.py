from .modules import View, ListView, DetailView, login_required, csrf_protect, method_decorator, reverse_lazy, redirect, render, messages, manager_only
from website.models import UploadedImage
from website.forms import UploadedImageForm, UploadStatusForm, UpdateUserForm, UserDataForm
from website.helper import is_user_a_manager
from .main_views import StatusView

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin
from django.core.files.base import ContentFile
from PIL import Image, ExifTags
from io import BytesIO
import os

@method_decorator([csrf_protect, login_required], name='dispatch')
class UserProfileView(DetailView):
    """
        User Profile View
        GET: Displays user information and extra data on a form for editing.
        POST: Updates user non sensible information.
    """
    model = User
    template_name = 'website/user/user_profile.html'
    form = UpdateUserForm
    data_form = UserDataForm
    pass_form = PasswordChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['form'] = self.form(instance=user)
        context['data_form'] = self.data_form(instance=user.data)
        context['pass_form'] = self.pass_form(user=user)
        return context

    def username_exists(self, username):
        return User.objects.filter(username=username).exclude(pk=self.request.user.pk).exists()

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        form = self.form(request.POST, instance=user)
        data_form = self.data_form(request.POST, request.FILES, instance=user.data)

        if form.is_valid() and data_form.is_valid():
            if not self.username_exists(form.instance.email):
                user = form.save(commit=False)
                user.username = user.email
                user.save()
                data_form.save()
                messages.error(request, 'Personal information successfully updated.')
                return redirect(reverse_lazy('website:user_detail_view', kwargs={'pk':user.pk}))
            else:
                messages.error(request, 'There is another user with the email you provided.')

        context = {
            'form': form,
            'data_form': data_form,
            'pass_form': self.pass_form(),
        }
        return render(request, self.template_name, context)


@method_decorator([csrf_protect, login_required], name='dispatch')
class UpdatePasswordView(View):
    """
        User Password View
        Updates user's password.
    """
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        is_valid = form.is_valid()
        data = {'success': is_valid }

        if is_valid:
            form.save()
            update_session_auth_hash(request, form.user)
        else:
            print(form.errors)
            data['errors'] = form.errors

        return JsonResponse(data)

@method_decorator([csrf_protect, login_required, manager_only], name='dispatch')
class UserApprovalView(ListView):
    """
        User Approval View
        GET: Displays a list of (inactive) users who've requested access
        POST: Activates or Deletes a list of unactive users
    """
    template_name = 'website/user/user_approval.html'
    paginate_by = 10
    success_url = reverse_lazy('website:user_approval_view')

    def get_queryset(self):
        return User.objects.filter(is_active=False).order_by('first_name', 'last_name')

    def post(self, request, *args, **kwargs):
        data = dict(request.POST.lists())
        data.pop('csrfmiddlewaretoken')
        for key, val in data.items():
            user = get_object_or_404(User, pk=key)
            if val[0] == 'Accepted':
                user.is_active = True
                user.save()
            else:
                user.delete()

        return redirect(self.success_url)


@method_decorator([login_required, csrf_protect], name='dispatch')
class UserUploadsView(SingleObjectMixin, StatusView):
    """
        User Uploads View
        GET: Displays all the images uploaded by a certain user, filtering by the images status.
        POST: Creates a new UploadedImage object with the information provided.
    """
    template_name = "website/user/user_uploads.html"
    form = UploadedImageForm

    def get(self, request, *args, **kwargs):
        self.user_pk = kwargs.get('pk')
        if is_user_a_manager(request.user) or self.user_pk == request.user.pk:
            self.object = get_object_or_404(User, pk=kwargs.get('pk'))
            return super().get(request, *args, **kwargs)
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        context['upload_form'] = self.form()
        context['same_user'] = self.request.user.pk == self.user_pk
        return context

    def get_queryset(self):
        return self.object.uploadedimage_set.filter(status=self.status).order_by('-date_taken')

    def get_proper_dimensions(self, width, height, max=600):
        """
            retrieves corrected width and height (keeping ratio) of a PIL image based on max parameter
        """
        ratio = min(max/width, max/height)
        new_width = int(width*ratio)
        new_height = int(height*ratio)

        return new_width, new_height

    def rotate_image(self, image):
        """
            Some images are not taken in the "normal" (horizontal) position. For these images,
            PIL opens them in the orientation that it should have been taken.
            For example, if the image in question was taken vertically, PIL will create the image
            in horizontal as it should be the "default" position.
            Since we do not want to rotate these images, we have to read their Orientation attribute
            and rotate them back accordingly so we get the image in the original orientation.
        """
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
        """
            From a given image, this method creates a smaller, lower quality copy sample,
            returning an object that is readable by Django's file save method.
        """
        img = Image.open(img_data)
        img_width, img_height = img.size
        new_width, new_height = self.get_proper_dimensions(img_width, img_height)

        img.thumbnail((new_width, new_height))
        img_bytes = BytesIO()

        rotated = self.rotate_image(img)
        rotated.save(img_bytes, format='JPEG')
        return ContentFile(img_bytes.getvalue())

    def post(self, request, *args, **kwargs):
        """
            This will create a new UploadedImage object if the data in request.POST is valid.
            It will create a lower quality copy of the image that is uploaded in order to save it
            in the thumbnail attribute of the object. That is so the views that load mulitple images
            are not loaded with heavy data.
        """
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

        return redirect(reverse_lazy('website:user_uploads_view', kwargs={'pk': request.user.pk}))
