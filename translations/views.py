from .models import Word, TranslationVideo, UserVote, User
from .forms import SignUpForm
from .tokens import account_activation_token

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    authenticate as auth
)
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text


@ensure_csrf_cookie
def remove_this(request):

    word_list = Word.objects.all()

    login_form = AuthenticationForm(auto_id='login_id_%s')
    login_form.fields['username'].widget.attrs['placeholder'] = "Username"
    login_form.fields['password'].widget.attrs['placeholder'] = "Password"

    signup_form = SignUpForm(auto_id='signup_id_%s')
    signup_form.fields['username'].widget.attrs['placeholder'] = "Username"
    signup_form.fields['email'].widget.attrs['placeholder'] = "Email"
    signup_form.fields['password1'].widget.attrs['placeholder'] = "Password"
    signup_form.fields['password2'].widget.attrs['placeholder'] = "Confirm"

    context = {'words': word_list, 'new_videos': TranslationVideo.new_videos(),
               'login_form': login_form, 'signup_form': signup_form}

    return render(request, 'translations/new-base.html', context)


@ensure_csrf_cookie
def index(request):
    word_list = Word.objects.all()

    login_form = AuthenticationForm(auto_id='login_id_%s')
    signup_form = SignUpForm(auto_id='signup_id_%s')

    context = {'words': word_list, 'new_videos': TranslationVideo.new_videos(),
               'login_form': login_form, 'signup_form': signup_form}
    return render(request, 'translations/index.html', context)


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your SurdStream Account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
        return JsonResponse({'user_id': request.user.id,
                             'field_errors': signup_form.errors.as_json()})
    raise Http404("Only accepts AJAX, method POST")

    #         signup_form.save()
    #         username = signup_form.cleaned_data.get('username')
    #         raw_password = signup_form.cleaned_data.get('password1')
    #         user = auth(username=username, password=raw_password)
    #         auth_login(request, user)
    #     return JsonResponse({'user_id': request.user.id,
    #                          'field_errors': signup_form.errors.as_json()})
    # raise Http404("Only accepts AJAX, method POST")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        auth_login(request, user)
    return JsonResponse({'user_id': request.user.id})


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


def upload_video(request):
    # TranslationVideo.upload_video()
    if request.method == 'POST':
        print("UPLOAD VIDEO, post: ", request.POST)
        print("files: ", request.FILES['file-input'])
        # words = [w.strip() for w in request.POST['words'].split(',') if w.strip()]
        # file = request.FILES['file']
        # if file.size < 5242880 and words:  # 5 MB
        #     video_record = TranslationVideo(author=request.user, video_file=file)
        #     video_record.save()
        #     for word_text in words:
        #         word, created = Word.objects.get_or_create(word_text=word_text)
        #         video_record.words.add(word)
        #     return redirect(profile)
        # else:
        #     return HttpResponse(status=413)
    raise Http404("Only accepts AJAX, method POST")


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
