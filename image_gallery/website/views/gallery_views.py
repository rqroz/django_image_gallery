from .modules import View, ListView, login_required, csrf_protect, method_decorator, reverse_lazy, redirect, render, messages, get_object_or_404, manager_only
from website.models import UploadedImage
from website.forms import UploadStatusForm, GalleryFilterForm
from website.helper import is_user_a_manager
from django.http import Http404, JsonResponse
from django.db.models import Count
from .main_views import StatusView

@method_decorator([login_required], name='dispatch')
class GalleryView(ListView):
    paginate_by = 100
    template_name = 'website/gallery/gallery.html'
    form = GalleryFilterForm
    filter_by = GalleryFilterForm.DATE_TAKEN

    def get_queryset(self):
        queryset = UploadedImage.objects.filter(status=UploadedImage.ACCEPTED)
        print(queryset[0])
        if self.filter_by == GalleryFilterForm.DATE_TAKEN:
            return queryset.order_by('-date_taken')
        elif self.filter_by == GalleryFilterForm.NUMBER_OF_LIKES:
            q = queryset.extra(select = {
                                    'likes' :
                                        """
                                            SELECT COUNT(*)
                                            FROM website_uploadedimage
                                            JOIN website_imagelike on website_imagelike.image_id = website_uploadedimage.id
                                            WHERE website_imagelike.image_id = website_uploadedimage.id
                                        """
                                }).order_by('-likes')
            for w in q:
                print("%s has %d likes"%(w.pk, w.likes))
            return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form(initial={'filter_by':self.filter_by})
        return context

    def get(self, request, *args, **kwargs):
        filter_form = self.form(request.GET)
        if filter_form.is_valid():
            self.filter_by = filter_form.cleaned_data['filter_by']
        return super().get(request, *args, **kwargs)

@method_decorator([login_required, csrf_protect, manager_only], name='dispatch')
class PhotoApprovalView(StatusView):
    template_name = 'website/gallery/photo_approval.html'
    success_url = reverse_lazy('website:photo_approval_view')
    paginate_by = 10

    def get_queryset(self):
        return UploadedImage.objects.filter(status=self.status).order_by('-uploaded_on')

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
    def post(self, request, *args, **kwargs):
        uploaded_image = get_object_or_404(UploadedImage, pk=request.POST.get('pk'))
        data = uploaded_image.like(request.user)
        return JsonResponse(data)
