from .modules import login_required, csrf_protect, method_decorator, reverse_lazy, redirect, render, messages
from website.models import UploadedImage
from website.forms import UploadStatusForm
from website.helper import is_user_a_manager
from website.website_decorators import manager_only
from django.http import Http404, JsonResponse

from .main_views import StatusView

@method_decorator([login_required, csrf_protect, manager_only], name='dispatch')
class PhotoApprovalView(StatusView):
    template_name = 'website/gallery/photo_approval.html'

    def get_queryset(self):
        return UploadedImage.objects.filter(status=self.status).order_by('-uploaded_on')
