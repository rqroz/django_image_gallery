import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from website.paths import url_gallery_img, url_gallery_img_small

class UploadedImage(models.Model):
    PENDING = 'Pending'
    REFUSED = 'Refused'
    ACCEPTED = 'Accepted'
    STATUS_CHOICES = (
        (PENDING, PENDING),
        (REFUSED, REFUSED),
        (ACCEPTED, ACCEPTED),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.ImageField(upload_to=url_gallery_img)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "%s uploaded %s"%(self.user.username, self.get_filename())

    def get_filename(self):
        # Gets the filename and removes the 'b' inserted at the begining when them model is saved
        return os.path.basename(self.upload.name)[1:]


class ImageLike(models.Model):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "%s liked %s"%(self.user.username, self.image.upload.name)


# Deleting files from storage when database object is deleted
@receiver(pre_delete, sender=UploadedImage)
def img_post_delete(sender, instance, **kwargs):
    # Pass false so that FileField deletes the file but doesn't save the model.
    instance.upload.delete(False)
