from .models import Word, TranslationVideo, UserVote

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


def index(request):
    word_list = Word.objects.all()
    context = {'words': word_list, 'new_videos': TranslationVideo.new_videos()}
    return render(request, 'translations/index.html', context)


@ensure_csrf_cookie
def detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    word_videos = word.videos.all()
    user_votes = [video.user_vote_value(request.user.id) for video in word_videos]
    return render(request, 'translations/detail.html',
                  {'word': word, 'videos_and_votes': list(zip(word_videos, user_votes)),
                   'user': request.user})


def vote(request, video_id):
    new_delta_vote = int(request.POST['vote'])
    user_vote, created = UserVote.objects.update_or_create(
        user=request.user, video_id=video_id,
        defaults={'vote': new_delta_vote},
    )
    data = {'new_total_votes': user_vote.video.votes,
            'user_vote': new_delta_vote}
    return JsonResponse(data)


def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
