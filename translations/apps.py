from django.apps import AppConfig
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from django.core.files import File

import os


class TranslationsConfig(AppConfig):
    name = 'translations'

    def ready(self):
        from .models import UserVote, User, TranslationVideo, DeletedTranslationVideo
        pre_save.connect(pre_save_user_vote, sender=UserVote, dispatch_uid="pre_save_user_vote_uid")
        pre_delete.connect(pre_delete_user, sender=User, dispatch_uid="pre_delete_user_uid")

        pre_save.connect(pre_save_translation_video, sender=TranslationVideo,
                         dispatch_uid="pre_save_translation_video_uid")
        post_save.connect(post_save_translation_video, sender=TranslationVideo,
                          dispatch_uid="post_save_translation_video_uid")
        pre_delete.connect(pre_delete_translation_video, sender=TranslationVideo,
                           dispatch_uid="pre_delete_translation_video_uid")
        post_delete.connect(post_delete_translation_video, sender=TranslationVideo,
                            dispatch_uid="post_delete_translation_video_uid")

        post_delete.connect(post_delete_deleted_translation_video, sender=DeletedTranslationVideo,
                            dispatch_uid="post_delete_deleted_translation_video_uid")


def pre_save_user_vote(sender, instance, **kwargs):  # instance: new_user_vote
    from .models import UserVote
    try:
        old_user_vote = UserVote.objects.get(id=instance.id)
        old_vote_value = old_user_vote.vote
    except UserVote.DoesNotExist:
        old_vote_value = 0

    instance.video.votes += instance.vote - old_vote_value
    instance.video.save()


def pre_delete_user(sender, instance, **kwargs):  # instance: deleted_user
    from .models import UserVote
    UserVote.rollback_user_votes(instance)


def translation_video_cache(instance):
    return {
        'author_name': instance.author.username if instance.author else None,
        'words': ','.join([str(w) for w in instance.words.all()]),
        'video_file': instance.video_file,
        'votes': instance.votes,
        'upload_date': instance.upload_date
    }


def mark_translation_video_as_deleted(instance_cache):
    from .models import DeletedTranslationVideo
    deleted_video = DeletedTranslationVideo(author_name=instance_cache['author_name'],
                                            words=instance_cache['words'],
                                            video_file=instance_cache['video_file'],
                                            votes=instance_cache['votes'],
                                            upload_date=instance_cache['upload_date'])
    deleted_video.save()


def pre_save_translation_video(sender, instance, **kwargs):
    # Retrieve the old instance from the database to get old values
    old_instance = sender.objects.filter(pk=instance.id).first()
    if old_instance is not None:
        # Keep the original value inside a cache
        instance.cache = translation_video_cache(old_instance)


def post_save_translation_video(sender, instance, **kwargs):
    if hasattr(instance, 'cache') and instance.cache['video_file'] \
            and instance.cache['video_file'] != instance.video_file:
        mark_translation_video_as_deleted(instance.cache)


def pre_delete_translation_video(sender, instance, **kwargs):
    instance.cache = translation_video_cache(instance)


def post_delete_translation_video(sender, instance, **kwargs):  # instance: deleted_translation_video
    mark_translation_video_as_deleted(instance.cache)

#    with open(instance.video_file.path, 'rb') as f:
#        deleted_video.video_file.save(name=os.path.basename(instance.video_file.name),
#                                      content=File(f))


def post_delete_deleted_translation_video(sender, instance, **kwargs):
    instance.video_file.delete(save=False)
