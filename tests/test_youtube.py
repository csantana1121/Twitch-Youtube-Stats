import unittest
from youtube import *

class YoutubeTest(unittest.TestCase):
    
    def test_get_stats(self):
        api_key = "AIzaSyCdon2Ht4qsO50eVJpu9nJO5iJx7TSIOhM"
        channel_id = "UCJ5v_MCY6GNUBTO8-D3XoAg"
        stats = get_stats(channel_id, api_key)
        self.assertEqual(type(stats), type({}))
        self.assertNotEqual(stats, {})
        self.assertNotEqual(stats, None)
    
    def test_get_channel_id(self):
        api_key = "AIzaSyCdon2Ht4qsO50eVJpu9nJO5iJx7TSIOhM"
        channel_name = "wwe"
        id = get_channel_id(api_key, channel_name)
        self.assertEqual(type(id), type(""))
        self.assertNotEqual(id, None)
        self.assertNotEqual(id, "")
    
    def test_playlist_id(self):
        channel_id = "UCJ5v_MCY6GNUBTO8-D3XoAg"
        api_key = "AIzaSyCdon2Ht4qsO50eVJpu9nJO5iJx7TSIOhM"
        playlist_id = get_playlists_id(channel_id, api_key)
        self.assertEqual(type(playlist_id), type(""))
        self.assertNotEqual(playlist_id, "")
        self.assertNotEqual(playlist_id, None)
    
    def test_extract_info_json(self):
        channel_id = "UCJ5v_MCY6GNUBTO8-D3XoAg"
        api_key = "AIzaSyCdon2Ht4qsO50eVJpu9nJO5iJx7TSIOhM"
        stats = get_stats(channel_id, api_key)
        values = extract_info_json(stats)
        self.assertEqual(type(values), type(()))
        self.assertNotEqual(values, None)
        self.assertNotEqual(values, ())
        self.assertEqual(len(values), 8)
    
    def test_video_id(self):
        channel_id = "UCJ5v_MCY6GNUBTO8-D3XoAg"
        api_key = "AIzaSyCdon2Ht4qsO50eVJpu9nJO5iJx7TSIOhM"
        playlist_id = get_playlists_id(channel_id, api_key)
        video_id = get_playlists_items(playlist_id, api_key)
        self.assertNotEqual(video_id, None)
        self.assertEqual(type(video_id), type(""))
        self.assertNotEqual(video_id, "")
        
    def test_video_url(self):
        channel_id = "UCJ5v_MCY6GNUBTO8-D3XoAg"
        api_key = "AIzaSyCdon2Ht4qsO50eVJpu9nJO5iJx7TSIOhM"
        playlist_id = get_playlists_id(channel_id, api_key)
        video_id = get_playlists_items(playlist_id, api_key)
        vid_url = video_url(video_id)
        self.assertEqual(vid_url[0:30], "https://www.youtube.com/embed/")

if __name__ == "__main__":
        unittest.main()
    
   