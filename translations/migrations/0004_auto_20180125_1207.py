# Generated by Django 2.0.1 on 2018-01-25 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0003_translationvideo_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translationvideo',
            name='video_url',
        ),
        migrations.AddField(
            model_name='translationvideo',
            name='video_file',
            field=models.FileField(default='settings.MEDIA_ROOT/files/media/videos/Video5.webm', upload_to=''),
            preserve_default=False,
        ),
    ]
