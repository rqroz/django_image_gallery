from django.contrib import admin

from .models import UploadedImage, ImageLike

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                     'upload__name')


@admin.register(ImageLike)
class ImageLikeAdmin(admin.ModelAdmin):
    search_fields = ('liked_by__username', 'liked_by__first_name', 'liked_by__last_name',
                     'image__user__username', 'image__user__first_name', 'image__user__last_name',
                     'image__upload__name')
