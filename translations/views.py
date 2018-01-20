from .models import Word, TranslationVideo, UserVote

from django.shortcuts import render, get_object_or_404


def index(request):
    word_list = Word.objects.all()
    context = {'words': word_list, 'new_videos': TranslationVideo.new_videos()}
    return render(request, 'translations/index.html', context)


def detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    word_videos = word.videos.all()
    user_votes = [video.user_vote_value(request.user.id) for video in word_videos]
    return render(request, 'translations/detail.html',
                  {'word': word, 'videos_and_votes': list(zip(word_videos, user_votes)),
                   'user': request.user})


def vote(request, video_id):
    video = get_object_or_404(TranslationVideo, pk=video_id)
    new_delta_vote = int(request.POST['vote'])

    try:
        old_user_vote = UserVote.objects.get(user=request.user, video=video)
        old_vote_value = old_user_vote.vote
    except UserVote.DoesNotExist:
        old_vote_value = 0

    user_vote, created = UserVote.objects.update_or_create(
        user=request.user, video=video,
        defaults={'vote': new_delta_vote},
    )
    video.votes += new_delta_vote - old_vote_value
    video.save()
    return render(request, 'translations/vote_results.html', {'video': video,
                                                              'delta_vote': new_delta_vote})


def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
