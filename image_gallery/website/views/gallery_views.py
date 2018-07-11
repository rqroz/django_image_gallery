from .modules import ListView, login_required, csrf_protect, method_decorator, reverse_lazy, redirect, render, messages, get_object_or_404, manager_only
from website.models import UploadedImage
from website.forms import UploadStatusForm
from website.helper import is_user_a_manager
from django.http import Http404, JsonResponse

from .main_views import StatusView

@method_decorator([login_required], name='dispatch')
class GalleryView(ListView):
    paginate_by = 100
    template_name = 'website/gallery/gallery.html'

    def get_queryset(self):
        return UploadedImage.objects.filter(status=UploadedImage.ACCEPTED).order_by('-uploaded_on')


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
