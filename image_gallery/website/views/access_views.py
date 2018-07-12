from .modules import ListView, render, redirect, reverse_lazy, method_decorator, login_required, csrf_protect, messages, manager_only, get_object_or_404
from website.forms import LoginForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Q
from website.models import UserData

class AnonymousFormView(View):
    form = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: return redirect(self.success_url)

        context = { 'form': self.form() }
        return render(request, self.template_name, context)


@method_decorator(csrf_protect, name='dispatch')
class AuthView(AnonymousFormView):
    template_name = 'website/landing/login.html'
    form = LoginForm
    success_url = reverse_lazy('website:index_view')

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

@method_decorator(csrf_protect, name='dispatch')
class RequestAcessView(AnonymousFormView):
    template_name = 'website/landing/request_access.html'
    form = UserForm
    success_url = reverse_lazy('website:index_view')

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            if not User.objects.filter(username=form.cleaned_data['email']).exists():
                new_user = form.save(commit=False)
                new_user.username = new_user.email
                new_user.set_password(form.cleaned_data['password'])
                new_user.is_active = False
                new_user.save()
                UserData.objects.create(user=new_user)
                messages.success(request, 'Your request was place. When approved, we will send you a confirmation email.<br/>(Not Really as this is for testing purposes, but you get the ideia...)')
                return redirect(self.success_url)
            else:
                messages.error(request, 'There is a user with the email you provided, please provide another email.')
        context = { 'form': form }
        return render(request, self.template_name, context)
