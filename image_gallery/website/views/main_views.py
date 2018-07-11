from .modules import render, redirect, reverse_lazy, method_decorator, login_required, csrf_protect, messages
from website.forms import LoginForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import ListView
from website.forms import UploadStatusForm, UploadedImage

class IndexView(View):
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.template_name = 'website/landing/landing.html'

        return render(request, self.template_name)

@method_decorator(csrf_protect, name='dispatch')
class AuthView(View):
    template_name = 'website/landing/login.html'
    form = LoginForm
    success_url = reverse_lazy('website:index_view')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: return redirect(self.success_url)

        context = { 'form': self.form() }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        login_form = self.form(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                nextt = request.GET.get('next')
                return redirect(nextt) if nextt else redirect(self.success_url)
            else:
                messages.error(request, 'Could not find a user matching your credentials.<br/>Please double check the information provided.')

        context = { 'form': login_form }
        return render(request, self.template_name, context)

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('website:index_view'))


@method_decorator([csrf_protect, login_required], name='dispatch')
class StatusView(ListView):
    """
        Generic List View used to filter UploadedImages by their status
    """
    paginate_by = 10
    status_form = UploadStatusForm
    status = UploadedImage.PENDING

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
