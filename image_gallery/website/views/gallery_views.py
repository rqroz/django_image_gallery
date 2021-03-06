from .modules import View, ListView, login_required, csrf_protect, method_decorator, reverse_lazy, redirect, render, messages, get_object_or_404, manager_only
from website.models import UploadedImage
from website.forms import UploadStatusForm, GalleryOrderingForm
from website.helper import is_user_a_manager
from django.http import Http404, JsonResponse
from django.db.models import Count
from .main_views import StatusView

@method_decorator([login_required], name='dispatch')
class GalleryView(ListView):
    """
        Gallery View
        Displays all approved images with correct ordering.

        Note: The 'repeat' context key is for development purposes only. It is used to generate
              100x the content of the first page of the gallery so the developer can check the
              performance of the view without having to actually upload such number of images.
    """
    paginate_by = 100
    template_name = 'website/gallery/gallery.html'
    form = GalleryOrderingForm
    order_by = GalleryOrderingForm.DATE_TAKEN
    descending = True

    def get_queryset(self):
        queryset = UploadedImage.objects.filter(status=UploadedImage.ACCEPTED)
        order = '-' if self.descending else ''
        if self.order_by == GalleryOrderingForm.DATE_TAKEN:
            return queryset.order_by(order+'date_taken')
        elif self.order_by == GalleryOrderingForm.NUMBER_OF_LIKES:
            return queryset.annotate(likes=Count('imagelike')).order_by(order+'likes')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = GalleryOrderingForm.DESCENDING if self.descending else GalleryOrderingForm.ASCENDING
        context['form'] = self.form(initial={'sort_by':self.order_by, 'order': order})

        simulation = self.request.GET.get('simulate-large-data')
        context['repeat'] = 100 if simulation else 1
        return context

    def get(self, request, *args, **kwargs):
        order_form = self.form(request.GET)
        if order_form.is_valid():
            self.order_by = order_form.cleaned_data['sort_by']
            self.descending = order_form.cleaned_data['order'] == 'desc'
        return super().get(request, *args, **kwargs)


@method_decorator([login_required, csrf_protect, manager_only], name='dispatch')
class PhotoApprovalView(StatusView):
    """
        Photo Approval View
        GET: Displays all the images uploaded filtering by its status.
        POST: Changes the status of images and redirect back to the same page with the previous GET parameters.
    """
    template_name = 'website/gallery/photo_approval.html'
    success_url = reverse_lazy('website:photo_approval_view')
    paginate_by = 10
    status = UploadedImage.PENDING

    def get_queryset(self):
        return UploadedImage.objects.filter(status=self.status).order_by('-uploaded_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.status
        return context

    def post(self, request, *args, **kwargs):
        print(self.success_url)

        post_data = dict(request.POST.lists())
        post_data.pop('csrfmiddlewaretoken')
        for (key, value) in post_data.items():
            ui = get_object_or_404(UploadedImage, pk=key)
            ui.status = value[0]
            ui.save()


        status = request.GET.get('status')
        page = request.GET.get('page')
        append_url = ""
        if page or status:
            append_url += "?"
            if page: append_url += "page=%s&"%page
            if status: append_url += "status=%s"%status

        return redirect(self.success_url+append_url)

@method_decorator([login_required, csrf_protect], name='dispatch')
class ImageLikeView(View):
    """
        Image Like View
        Creates a User-Image (ImageLike) relation to represent the like.
    """
    def post(self, request, *args, **kwargs):
        uploaded_image = get_object_or_404(UploadedImage, pk=request.POST.get('pk'))
        data = uploaded_image.like(request.user)
        return JsonResponse(data)
