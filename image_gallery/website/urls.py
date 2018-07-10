from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'website'
urlpatterns = [
    path('', IndexView.as_view(), name='index_view'),
    path('img/', UploadedImageView.as_view(), name='upload_img_view'),
    path('login/', AuthView.as_view(), name='login_view'),
]
