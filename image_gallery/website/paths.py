import os

def url_gallery_img(instance, filename):
    return 'gallery/users/%d/uploads/%s'%(instance.user.pk, filename.encode('utf-8'))

def url_gallery_img_small(instance, filename):
    return 'gallery/users/%d/uploads/small/%s'%(instance.user.pk, filename.encode('utf-8'))
