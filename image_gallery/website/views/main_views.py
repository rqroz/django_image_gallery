from .modules import View, render, redirect, reverse_lazy, method_decorator, login_required, csrf_protect, messages
from website.forms import LoginForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class IndexView(View):
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.template_name = 'website/landing.html'

        return render(request, self.template_name)

@method_decorator(csrf_protect, name='dispatch')
class AuthView(View):
    template_name = 'website/login.html'
    form = LoginForm
    success_url = reverse_lazy('website:index_view')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.META['HTTP_REFERER'])

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
