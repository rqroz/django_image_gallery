from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'website'
urlpatterns = [
    # path('', TemplateView.as_view(template_name="dip/dip.html"), name='dip_view'),
    path('', IndexView.as_view(), name='index_view'),
    path('img/', UploadedImageView.as_view(), name='upload_img_view'),
]
