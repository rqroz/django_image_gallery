# Generated by Django 2.0.4 on 2018-07-10 23:15

from django.db import migrations, models
import website.paths


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20180710_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedimage',
            name='sample',
            field=models.ImageField(default=1, upload_to=website.paths.url_gallery_thumbnail),
            preserve_default=False,
        ),
    ]
