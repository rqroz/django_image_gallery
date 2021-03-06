import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from website.paths import *
from website.validators import *

class UserData(models.Model):
    """
        Represents user's extra information (data) not presented in Django's default User model.
    """
    user = models.OneToOneField(User, related_name="data", on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, null=True, upload_to=url_user_img)

    def __str__(self):
        return self.user.username

class UploadedImage(models.Model):
    """
        Represents the image object that will contain each image uploaded by the users.
    """

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
    thumbnail = models.ImageField(upload_to=url_gallery_thumbnail)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    uploaded_on = models.DateTimeField(auto_now_add=True, editable=False)
    date_taken = models.DateField(validators=[deny_future_date])

    def __str__(self):
        return "%s uploaded %s"%(self.user.username, self.get_filename())

    def get_filename(self):
        # Gets the filename and removes the 'b' inserted at the begining when them model is saved
        return os.path.basename(self.upload.name)[1:]

    def number_of_likes(self):
        return self.imagelike_set.count()

    def user_liked(self, user):
        return self.imagelike_set.filter(liked_by__pk=user.pk).exists()

    def like(self, user):
        likeRelation, created = ImageLike.objects.get_or_create(liked_by=user, image=self)
        if created:
            likeRelation.save()
        else:
            likeRelation.delete()

        data = {
            'likes': self.number_of_likes(),
            'liked': created
            }
        return data


class ImageLike(models.Model):
    """
        Holds the relation between a user and the image they liked
    """
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "%s liked %s"%(self.liked_by.username, self.image.upload.name)


# Deleting files from storage when database object is deleted
@receiver(pre_delete, sender=UploadedImage)
def img_post_delete(sender, instance, **kwargs):
    # Pass false so that FileField deletes the file but doesn't save the model.
    instance.upload.delete(False)
    instance.thumbnail.delete(False)

@receiver(pre_delete, sender=UserData)
def img_post_delete(sender, instance, **kwargs):
    instance.profile_picture.delete(False)
