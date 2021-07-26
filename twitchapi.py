# import twitch
# from twitch import TwitchClient
import requests
import json
import sys

BASE_URL = 'https://api.twitch.tv/helix/'
Client_ID = 'eedwgqusvmegsz5mwo0bm7qofps313'
Client_Secret = 'haxnb9q65oi0efb9mh2bvrjnd4ac4d'
INDENT = 2
AUTH_URL = 'https://id.twitch.tv/oauth2/token'

test = requests.post(
    f'https://id.twitch.tv/oauth2/token?client_id={Client_ID}&client_secret=' +
    f'{Client_Secret}&grant_type=client_credentials').json()['access_token']
bearer_token = test
if bearer_token.lower().startswith('bearer'):
    bearer_token = bearer_token[6:0]
# print(bearer_token)
token = 'Bearer ' + bearer_token.lower().strip()
# print(token)
HEADERS = {'Authorization': token, 'client-id': Client_ID}
# print(HEADERS)


def get_response(query):
    url = BASE_URL + query
    response = requests.get(url, headers=HEADERS)
    return response


def print_response(response):
    response_json = response.json()
    print_response = json.dumps(response_json, indent=INDENT)
    print(print_response)


def get_user_streams_query(user_login):
    return 'streams?user_login={0}'.format(user_login)

# This gets live streamers stream data


def get_user_query(user_login):
    return 'users?login={0}'.format(user_login)


def get_user_videos_query(user_id):
    return 'videos?user_id={0}&first=50'.format(user_id)


def test_method():
    user_login = 'gorgc'

    query = get_user_query(user_login)
    response = get_response(query)
    user_info = response.json()
    user_id = user_info['data'][0]['id']
    img_url = user_info['data'][0]['profile_image_url']
    print(user_id)
    print(img_url)
    user_videos_query = get_user_videos_query(user_id)
    videos_info = get_response(user_videos_query)
    print(videos_info.status_code)
    videos_info_json = videos_info.json()
    print(videos_info_json)

    # print_response(response)
