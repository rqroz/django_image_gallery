# Generated by Django 2.0.4 on 2018-07-10 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_uploadedimage_small_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedimage',
            name='small_image',
        ),
    ]