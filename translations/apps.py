from django.apps import AppConfig

from django.db.models.signals import pre_delete, pre_save


class TranslationsConfig(AppConfig):
    name = 'translations'

    def ready(self):
        from .models import UserVote, User
        pre_save.connect(pre_save_user_vote, sender=UserVote, dispatch_uid="pre_save_user_vote_uid")
        pre_delete.connect(pre_delete_user, sender=User, dispatch_uid="pre_delete_user_uid")


def pre_save_user_vote(sender, **kwargs):
    new_user_vote = kwargs['instance']

    from .models import UserVote
    try:
        old_user_vote = UserVote.objects.get(id=new_user_vote.id)
        old_vote_value = old_user_vote.vote
    except UserVote.DoesNotExist:
        old_vote_value = 0

    new_user_vote.video.votes += new_user_vote.vote - old_vote_value
    new_user_vote.video.save()


def pre_delete_user(sender, **kwargs):
    from .models import UserVote
    deleted_user = kwargs['instance']
    UserVote.rollback_user_votes(deleted_user)
