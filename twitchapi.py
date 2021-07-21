#import twitch
#from twitch import TwitchClient
import requests, json, sys

BASE_URL = 'https://api.twitch.tv/helix/'
Client_ID = 'eedwgqusvmegsz5mwo0bm7qofps313'
Client_Secret = 'haxnb9q65oi0efb9mh2bvrjnd4ac4d'
INDENT = 2
AUTH_URL = 'https://id.twitch.tv/oauth2/token'

test = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={Client_ID}&client_secret={Client_Secret}&grant_type=client_credentials').json()['access_token']
bearer_token = test
if bearer_token.lower().startswith('bearer'):
            bearer_token = bearer_token[6:0]
print(bearer_token)
token = 'Bearer ' + bearer_token.lower().strip()
print(token)
HEADERS = {'Authorization' : token, 'client-id': Client_ID}
print(HEADERS)

# client = twitch.TwitchHelix(client_id=Client_ID, client_secret=Client_Secret, scopes=[twitch.constants.OAUTH_SCOPE_ANALYTICS_READ_EXTENSIONS])
# client.get_oauth()
# client.get_streams()
# helix = twitch.Helix(Client_ID, Client_Secret)

# for user in helix.users(['sodapoppin', 'reckful', 24250859]):
#     print(user.display_name)
#     # print(user.created_at)
#     print(user.view_count)

def get_response(query):
    url = BASE_URL + query
    response = requests.get(url, headers=HEADERS)
    return response

def print_response(response):
    response_json = response.json()
    print_response = json.dumps(response_json, indent = INDENT)
    print(print_response)

def get_user_streams_query(user_login):
    return 'streams?user_login={0}'.format(user_login)

# This gets live streamers stream data
def get_user_query(user_login):
    return 'users?login={0}'.format(user_login)

def get_user_videos_query(user_id):
    return f'streams?login={0}&first=50'.format(user_id)

user_login = 'gorgc'

query = get_user_query(user_login)
response = get_response(query)

print_response(response)