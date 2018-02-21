from .video_uploader import upload_video_to_youtube

from django.db import models
from django.contrib.auth.models import AbstractUser

from typing import Tuple, List


class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    # def video_vote_value(self, video_id: int):
    pass
#    rated_videos = models.ManyToManyField('TranslationVideo', related_name='voted_users', through='UserVote')


class Word(models.Model):
    word_text = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.word_text

# class WordTranslationVideo(models.Model):
#     word = models.ForeignKey(Word, on_delete=models.CASCADE)
#     translation_video = models.ForeignKey(TranslationVideo, on_delete=models.CASCADE)


class TranslationVideo(models.Model):
    author = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
#    words = models.ManyToManyField(Word, related_name='videos')
    words = models.ManyToManyField(Word, related_name='videos', through='VideoWord')
#    video_url = models.CharField(max_length=500)  # models.URLField
#    video_file = models.FileField(upload_to='videos/%Y/%m/', max_length=150)
    youtube_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    votes = models.IntegerField(default=0)
    voted_users = models.ManyToManyField(User, related_name='rated_videos', through='UserVote')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        words_str = '[' + ', '.join(map(str, self.words.all())) + ']'
        return 'Video ' + self.youtube_id + ' ' + words_str

    @staticmethod
    def new_videos():
        return TranslationVideo.objects.order_by('upload_date')[:5]

    def user_vote_value(self, user_id: int) -> int:
        user_vote_records = UserVote.objects.filter(user_id=user_id, video=self)
        assert len(user_vote_records) <= 1, \
            'There can be only one record of UserVote for the specific user and the video'
        return user_vote_records[0].vote if user_vote_records else 0

    @staticmethod
    def upload_video(file, words: List[str]) -> Tuple[int, str]:
        return upload_video_to_youtube(file, words)


class VideoWord(models.Model):
    video = models.ForeignKey(TranslationVideo, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    match = models.FloatField()  # coincidence percent


class DeletedTranslationVideo(models.Model):
    author_name = models.CharField(max_length=100, blank=True, null=True)
    words = models.CharField(max_length=200)
    video_file = models.FileField(max_length=150) #(upload_to='deleted_videos/%Y/%m/', max_length=150)
    votes = models.IntegerField()
    upload_date = models.DateTimeField()
    deleting_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'DeletedVideo ' + self.video_file.url + ' ' + self.words


class UserVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(TranslationVideo, on_delete=models.CASCADE)
    vote = models.IntegerField()
    last_modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "video")

    @staticmethod
    def rollback_user_votes(user: User):
        user_vote_records = UserVote.objects.filter(user=user)
        for user_vote_record in user_vote_records:
            user_vote_record.video.votes -= user_vote_record.vote
            user_vote_record.video.save()
