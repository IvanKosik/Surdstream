from .models import Word, TranslationVideo, UserVote

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


@ensure_csrf_cookie
def index(request):
    word_list = Word.objects.all()

    auth_form = AuthenticationForm()
    auth_form.fields['username'].widget.attrs['placeholder'] = "Email"
    auth_form.fields['password'].widget.attrs['placeholder'] = "Password"

    context = {'words': word_list, 'new_videos': TranslationVideo.new_videos(),
               'auth_form': auth_form}
    return render(request, 'translations/index.html', context)


def login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
        response_data = {'user_id': request.user.id,
                         'field_errors': login_form.errors.as_json()}
        return JsonResponse(response_data)
    raise Http404("Only accepts AJAX, method POST")


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({'user_id': request.user.id})


@ensure_csrf_cookie
def detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    word_videos = word.videos.all()
    user_votes = [video.user_vote_value(request.user.id) for video in word_videos]
    return render(request, 'translations/detail.html',
                  {'word': word, 'videos_and_votes': list(zip(word_videos, user_votes))})


def vote(request, video_id):
    new_delta_vote = int(request.POST['vote'])
    user_vote, created = UserVote.objects.update_or_create(
        user=request.user, video_id=video_id,
        defaults={'vote': new_delta_vote},
    )
    data = {'new_total_votes': user_vote.video.votes,
            'user_vote': new_delta_vote}
    return JsonResponse(data)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {})


@login_required
def add_translation(request):
    if request.method == 'POST':
        words = [w.strip() for w in request.POST['words'].split(',') if w.strip()]
        file = request.FILES['file']
        if file.size < 5242880 and words:  # 5 MB
            video_record = TranslationVideo(author=request.user, video_file=file)
            video_record.save()
            for word_text in words:
                word, created = Word.objects.get_or_create(word_text=word_text)
                video_record.words.add(word)
            return redirect(profile)
        else:
            return HttpResponse(status=413)
    return render(request, 'translations/new.html', {})
