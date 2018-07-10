from .modules import View, render, redirect, reverse_lazy, login_required, messages
from website.forms import LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class IndexView(View):
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            self.template_name = 'website/landing.html'

        return render(request, self.template_name)

class AuthView(View):
    template_name = 'website/login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        context = { 'form': self.form() }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        login_form = self.form(request.POST)


        if login_form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                nextt = request.GET.get('next')
                return redirect(nextt) if nextt else redirect(reverse_lazy('website:index_view'))
            else:
                messages.error(request, 'There is no such user, please check the information provided.')

        context = { 'form': login_form }
        return render(request, self.template_name, context)

@login_required
def logout_view(request):
    logout(request)
    return redirect(index)
