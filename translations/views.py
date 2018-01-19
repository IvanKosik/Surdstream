from .models import Word, TranslationVideo

from django.shortcuts import render, get_object_or_404


def index(request):
    word_list = Word.objects.all()
    context = {'words': word_list, 'new_videos': TranslationVideo.new_videos()}
    return render(request, 'translations/index.html', context)


def detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    word_videos = word.videos.all()
    return render(request, 'translations/detail.html',
                  {'word': word, 'videos': word_videos, 'user': request.user})


def vote(request, video_id):
    video = get_object_or_404(TranslationVideo, pk=video_id)
    delta_vote = int(request.POST['vote'])
    video.votes += delta_vote
    video.save()
    return render(request, 'translations/vote_results.html', {'video': video,
                                                              'delta_vote': delta_vote})


def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
