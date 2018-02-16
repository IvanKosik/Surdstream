from django.conf import settings

import requests


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
def upload_video_metadata(access_token: str, file_size: int) -> str:
    upload_url = "https://www.googleapis.com/upload/youtube/v3/videos"
    upload_params = {'uploadType': 'resumable',
                     'part': 'snippet,status,contentDetails'}
    upload_headers = {'Host': 'www.googleapis.com',
                      'Authorization': 'Bearer ' + access_token,
                      'Content-type': 'application/json',  # ; charset=UTF-8',
                      'X-Upload-Content-Length': str(file_size),
                      'X-Upload-Content-Type': 'video/*'}
    upload_data = {
        "snippet": {
            "title": "My video title",
            "description": "This is a description of my video",
            "tags": ["cool", "video", "more keywords"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "private",
            "license": "youtube"
        }
    }

    '''
    body = dict(
        snippet=dict(
            title="TestSurdVideo",
            description="My test description",
            tags=["TestO","Surd"],
            categoryId="22"
    ),
        status=dict(
            privacyStatus="private"
        )
    )
    '''

    upload_r = requests.post(upload_url, params=upload_params, headers=upload_headers,
                             json=upload_data)
    return upload_r.headers['Location']


# Upload video to the |upload_url}
def upload_video_to_url(upload_url: str, access_token: str, file_size: int, file_data) -> requests.Response:
    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-type': 'video/*',
               'Content-Length': str(file_size)}
    return requests.put(upload_url, headers=headers, data=file_data)


# Returns video id string
def upload_video() -> str:
    current_access_token = refresh_access_token(settings.YOUTUBE_AUTH_REFRESH_TOKEN)
    print("access_token:  ", current_access_token)

    file_name = 'Video3.webm'
    #    if not os.path.exists(file_name):
    #        print("NO SUCH FILE")
    upload_data_file = open(file_name, 'rb').read()
    file_size = len(upload_data_file)

    location_url = upload_video_metadata(current_access_token, file_size)
    print("---LOCATION: ", location_url)
    resp = upload_video_to_url(location_url, current_access_token, file_size, upload_data_file)
    print("UPLOAD RESULT: ", resp.status_code)
    print(print_response(resp))
    video_id = resp.json()['id']
    print("Video ID: ", video_id)
    return video_id
