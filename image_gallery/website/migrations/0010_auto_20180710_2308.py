# Generated by Django 2.0.4 on 2018-07-10 23:08

from django.db import migrations, models
import website.paths


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20180710_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=website.paths.url_user_img),
        ),
    ]