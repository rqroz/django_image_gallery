from .modules import login_required, method_decorator, reverse_lazy, redirect, render, messages
from website.models import UploadedImage
from website.helper import is_user_a_manager
from website.website_decorators import manager_only
from django.http import Http404, JsonResponse

from django.views.generic import ListView

@method_decorator([login_required, manager_only], name='dispatch')
class PhotoApprovalView(ListView):
    template_name = 'website/gallery/photo_approval.html'
    paginate_by = 50

    def get_queryset(self):
        return UploadedImage.objects.filter(status=UploadedImage.PENDING).order_by('-uploaded_on')
