import os

def url_user_img(instance, filename):
    return 'users/%d/profile/%s'%(instance.user.pk, filename.encode('utf-8'))

def url_gallery_img(instance, filename):
    return 'gallery/users/%d/uploads/%s'%(instance.user.pk, filename.encode('utf-8'))

def url_gallery_thumbnail(instance, filename):
    return 'gallery/users/%d/uploads/thumbnails/%s'%(instance.user.pk, filename.encode('utf-8'))
