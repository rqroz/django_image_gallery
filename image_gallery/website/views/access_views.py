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
                if not UserData.objects.filter(user=user).exists():
                    UserData.objects.create(user=user)
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
            new_user = form.save(commit=False)
            new_user.username = new_user.email
            new_user.is_active = False
            new_user.save()
            messages.success(request, 'Your request was place. When approved, we will send you a confirmation email.')
            return redirect(self.success_url)
        else:
            context = { 'form': form }
            return render(request, self.template_name, context)

@method_decorator([csrf_protect, login_required, manager_only], name='dispatch')
class UserApprovalView(ListView):
    template_name = 'website/user/user_approval.html'
    paginate_by = 10
    success_url = reverse_lazy('website:user_approval_view')

    def get_queryset(self):
        return User.objects.filter(is_active=False).order_by('first_name', 'last_name')

    def post(self, request, *args, **kwargs):
        data = dict(request.POST.lists())
        data.pop('csrfmiddlewaretoken')
        for key, val in data.items():
            user = get_object_or_404(User, pk=key)
            if val[0] == 'Accepted':
                user.is_active = True
                user.save()
            else:
                user.delete()

        return redirect(self.success_url)
