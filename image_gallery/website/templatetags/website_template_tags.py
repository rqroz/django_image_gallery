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
        return 'success'
    elif status == UploadedImage.REFUSED:
        return 'danger'
    elif status == UploadedImage.PENDING:
        return 'warning'

@register.filter
def user_liked_image(uploaded_image, user):
    return uploaded_image.user_liked(user)

@register.filter
def get_total_uploads(user):
    return user.uploadedimage_set.all().count()

@register.filter
def get_status_uploads(user, status):
    return user.uploadedimage_set.filter(status=status).count()

@register.filter
def get_user_image_url(user):
    try:
        return user.data.profile_picture.url
    except:
        return '/static/website/img/default_user_icon.png'

@register.filter
def makelist(upperBound):
    return list(range(upperBound))
