from .modules import ListView, View, render, redirect, reverse_lazy, method_decorator, login_required, csrf_protect, messages, manager_only
from website.forms import UploadStatusForm, UploadedImage
from django.contrib.auth.models import User
from django.db.models import Q

class IndexView(View):
    """
        Index View
        Displays the landing page if the user is annonymous, otherwise redirects to Gallery View.
    """
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.template_name = 'website/landing/landing.html'
            return render(request, self.template_name)
        else:
            return redirect(reverse_lazy('website:gallery_view'))

@method_decorator([login_required, manager_only], name='dispatch')
class SearchView(ListView):
    """
        Search View
        Displays the result of a search query on users
        Fields Searched: First Name and Last Name
    """
    template_name = 'website/search.html'
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get('search')
        return User.objects.filter(
                                    Q(first_name__contains=search) | Q(last_name__contains=search)
                                ).exclude(pk=self.request.user.pk).order_by('first_name')

@method_decorator([csrf_protect, login_required], name='dispatch')
class StatusView(ListView):
    """
        Generic List View used to filter UploadedImages by their status
    """
    paginate_by = 10
    status_form = UploadStatusForm
    status = UploadedImage.ACCEPTED

    def replace_status(self, temp_status):
        if temp_status is None: return
        for key, value in UploadedImage.STATUS_CHOICES:
            if temp_status == value:
                self.status = value
                break

    def get(self, request, *args, **kwargs):
        self.replace_status(request.GET.get('status'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.status
        context['status_form'] = self.status_form(initial={'status':self.status})
        return context
