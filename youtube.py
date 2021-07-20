import requests
import pandas as pd


def get_input():
     channel = input("Enter channel name: ")

def get_channel_id(api_key, channel):
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&maxResults=1&q=" + channel + "&key=" + api_key

    response = requests.get(url)
    data = response.json()
    return (data['items'][0]['id']['channelId'])


def get_stats(channel_id, api_key):
    url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet&part=statistics&id=' + channel_id + "&key=" + api_key
    response = requests.get(url)
    data = response.json()
    return data


def extract_info_json(data):
    channel_name = data['items'][0]['snippet']['title']
    
    description = data['items'][0]['snippet']['description']
    
    key = 'country'
    country = ""
    if key in data['items'][0]['snippet']:
        country = data['items'][0]['snippet']['country']
        
    num_views = data['items'][0]['statistics']['viewCount']
    
    num_subscribers = ""
    if data['items'][0]['statistics']['hiddenSubscriberCount'] is False:
        num_subscribers = data['items'][0]['statistics']['subscriberCount']
    
    num_videos = data['items'][0]['statistics']['videoCount']
    
    date_creation = data['items'][0]['snippet']['publishedAt']
    
    photo_url = data['items'][0]['snippet']['thumbnails']['default']['url']
    
    return channel_name, description, country, num_views, num_subscribers, num_videos, date_creation, photo_url
    
    
def construct_dtfr():
    column_names = ['Channel name', 'Description', 'Country', 'Views', 'Subscribers', 'Number of Videos', 'Creation date', 'Photo url']
    dtfr = pd.DataFrame(columns=column_names)
    return dtfr
    
    
def insert_values_dtfr(dtfr, values):
    dtfr.loc[len(dtfr.index)] = values
    return dtfr


def print_dataframe():
    api_key = "AIzaSyCdon2Ht4qsO50eVJpu9nJO5iJx7TSIOhM"
    channel_id = get_channel_id(api_key)
    stats = get_stats(channel_id, api_key)
    values = extract_info_json(stats)
    dtfr_without_vals = construct_dtfr()
    dtfr_with_vals = insert_values_dtfr(dtfr_without_vals, values)
    
    print(dtfr_with_vals)
    

