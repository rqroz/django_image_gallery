from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'website'
urlpatterns = [
    # AUTH
    path('login/', AuthView.as_view(), name='login_view'),
    path('logout/', logout_view, name='logout_view'),

    # Home Page
    path('', IndexView.as_view(), name='index_view'),

    #
    path('uploads/<int:pk>/', UserImagesView.as_view(), name='user_gallery_view'),
]
