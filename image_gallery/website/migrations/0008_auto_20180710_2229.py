# Generated by Django 2.0.4 on 2018-07-10 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_userdefaults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdefaults',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]