from django import template
from website.helper import is_user_a_manager
from website.models import UploadedImage

register = template.Library()

@register.filter
def is_manager(user):
    return is_user_a_manager(user)

@register.filter
def get_status_class(status):
    if status == UploadedImage.ACCEPTED:
        return 'status-success'
    elif status == UploadedImage.REFUSED:
        return 'status-danger'
    elif status == UploadedImage.PENDING:
        return 'status-warning'
