from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = 'website'
urlpatterns = [
    # AUTH
    path('login/', AuthView.as_view(), name='login_view'),
    path('request-access/', RequestAcessView.as_view(), name='request_access_view'),
    path('logout/', logout_view, name='logout_view'),

    # Home Page
    path('', IndexView.as_view(), name='index_view'),

    # UploadedImage Views
    path('uploads/<int:pk>/', UserImagesView.as_view(), name='user_uploads_view'),

    # Gallery Views
    path('gallery/', GalleryView.as_view(), name='gallery_view'),
    path('gallery/approval/', PhotoApprovalView.as_view(), name='photo_approval_view'),

    # Search
    path('search/', SearchView.as_view(), name='search_view'),

    # User
    path('users/approval/', UserApprovalView.as_view(), name='user_approval_view'),
]
