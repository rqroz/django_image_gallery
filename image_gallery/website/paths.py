import os

def url_gallery_img(instance, filename):
    return 'gallery/users/%d/uploads/%s'%(instance.user.pk, filename.encode('utf-8'))
