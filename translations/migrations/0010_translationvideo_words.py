# Generated by Django 2.0.1 on 2018-02-20 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0009_auto_20180220_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationvideo',
            name='words',
            field=models.ManyToManyField(related_name='videos', through='translations.VideoWord', to='translations.Word'),
        ),
    ]
