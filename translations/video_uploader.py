from django.conf import settings
import logging

import requests

from typing import Tuple, List


logger = logging.getLogger(__name__)


def print_request(req):
    print('HTTP/1.1 {method} {url}\n{headers}\n\n{body}'.format(
        method=req.method,
        url=req.url,
        headers='\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        body=req.body,
    ))


def print_response(res):
    print('HTTP/1.1 {status_code}\n{headers}\n\n{body}'.format(
        status_code=res.status_code,
        headers='\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
        body=res.content,
    ))


# Form the auth URL. Then we can go to this url in our browser, and after accepting get the auth code
def auth_url():
    return '{auth_uri}?client_id={client_id}&scope={scope}' \
           '&response_type=code&redirect_uri={redirect_uri}&access_type=offline'.format(
        auth_uri=settings.GOOGLE_AUTH_URI,
        client_id=settings.YOUTUBE_AUTH_CLIENT_ID,
        scope=settings.YOUTUBE_UPLOAD_SCOPE,
        redirect_uri=settings.YOUTUBE_AUTH_WEB_REDIRECT_URI,
    )


# Swap authorization code for access and refresh tokens
# When run locally it returns error: invalid_grant.
# Maybe it because of we have to send this command from domain of this URL: settings.YOUTUBE_AUTH_WEB_REDIRECT_URI
def get_access_and_refresh_tokens_using_auth_code(auth_code: str) -> requests.Response:
    headers = {'Host': 'www.googleapis.com',
               'content-type': 'application/x-www-form-urlencoded'}
    data = {'code': auth_code,
            'client_id': settings.YOUTUBE_AUTH_CLIENT_ID,
            'client_secret': settings.YOUTUBE_AUTH_CLIENT_SECRET,
            'redirect_uri': settings.YOUTUBE_AUTH_WEB_REDIRECT_URI,
            'scope': '',
            'grant_type': 'authorization_code'}
    return requests.post(settings.GOOGLE_TOKEN_URI, headers=headers, data=data)


# Returns new access token using the refresh token
def refresh_access_token(refresh_token: str) -> str:
    headers = {'Host': 'www.googleapis.com',
               'content-type': 'application/x-www-form-urlencoded'}
    data = {'client_id': settings.YOUTUBE_AUTH_CLIENT_ID,
            'client_secret': settings.YOUTUBE_AUTH_CLIENT_SECRET,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'}
    response = requests.post(settings.GOOGLE_TOKEN_URI, headers=headers, data=data)
    return response.json()['access_token']


# Upload a video metadata
# Returns a location URI to upload the actual video file
def upload_video_metadata(access_token: str, file_size: int, words: List[str]) -> str:
    params = {'uploadType': 'resumable',
              'part': 'snippet,status,contentDetails'}
    headers = {'Host': 'www.googleapis.com',
               'Authorization': 'Bearer ' + access_token,
               'Content-type': 'application/json; charset=UTF-8',
               'X-Upload-Content-Length': str(file_size),
               'X-Upload-Content-Type': 'video/*'}

    words_str = ", ".join(words)
    data = dict(
        snippet=dict(
            title=words_str + " in sign language",
            description="Translation into sign language of the following synonyms: " + words_str,
            tags=words,
            categoryId=27
        ),
        status=dict(
            privacyStatus="unlisted",
            embeddable=True
        )
    )

    response = requests.post(settings.YOUTUBE_UPLOAD_URI, params=params, headers=headers, json=data)
    return response.headers['Location']


# Upload video to the |upload_url}
def upload_video_to_url(upload_url: str, access_token: str, file_data) -> requests.Response:
    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-type': 'video/*',
               'Content-Length': str(file_data.size)}
    return requests.put(upload_url, headers=headers, data=file_data)


# Returns (status, video id string)
def upload_video_to_youtube(file, words: List[str]) -> Tuple[int, str]:
    current_access_token = refresh_access_token(settings.YOUTUBE_AUTH_REFRESH_TOKEN)
    logger.debug("Youtube access token: ", current_access_token)

    location_url = upload_video_metadata(current_access_token, file.size, words)
    logger.debug("Youtube file location URL: ", location_url)

    response = upload_video_to_url(location_url, current_access_token, file)
    logger.debug("Youtube upload status code: ", response.status_code)

    video_id = response.json()['id']
    logger.debug("Youtube uploaded video id: ", video_id)
    return response.status_code, video_id
