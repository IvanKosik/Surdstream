from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User


class User(AbstractUser):
    pass
#    rated_videos = models.ManyToManyField('TranslationVideo', related_name='voted_users', through='UserVote')


class Word(models.Model):
    word_text = models.CharField(max_length=200)

    def __str__(self):
        return self.word_text

# class WordTranslationVideo(models.Model):
#     word = models.ForeignKey(Word, on_delete=models.CASCADE)
#     translation_video = models.ForeignKey(TranslationVideo, on_delete=models.CASCADE)


class TranslationVideo(models.Model):
    words = models.ManyToManyField(Word, related_name='videos')
    video_url = models.CharField(max_length=500)
    votes = models.IntegerField(default=0)
    voted_users = models.ManyToManyField(User, related_name='rated_videos', through='UserVote')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        words_str = '['
        for w in self.words.all():
            words_str += w.word_text + ', '
        words_str += ']'
        print('WORDS: ', self.words.all())
        return 'Video ' + self.video_url + ' ' + words_str

    @staticmethod
    def new_videos():
        return TranslationVideo.objects.order_by('upload_date')[:5]


class UserVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(TranslationVideo, on_delete=models.CASCADE)
    vote = models.IntegerField()
    last_modified_date = models.DateTimeField(auto_now=True)
