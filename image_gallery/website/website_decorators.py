from django.http import Http404
from website.helper import is_user_a_manager

def manager_only(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if is_user_a_manager(request.user):
            return view_func(request, *args, **kwargs)
        else:
            raise Http404()
    return _wrapped_view_func
