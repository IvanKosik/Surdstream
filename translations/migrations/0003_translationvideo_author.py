# Generated by Django 2.0.1 on 2018-01-22 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0002_auto_20180120_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationvideo',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
