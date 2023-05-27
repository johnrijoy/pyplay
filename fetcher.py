from youtube_search import YoutubeSearch
import requests
from exceptions import *
from utils import AudioDetails
from typing import List

def search_song(song_name: str) -> list:

    audio_info_list = []

    song_id_list = fetch_all_song_id(song_name)
    for song_id in song_id_list:
        audio_info = get_audio_dict(song_id)
        audio_info_list.append(audio_info)

    return audio_info_list

def get_song(song_name: str) -> AudioDetails:
    song_yt_id = fetch_song_id(song_name)
    audio_info = get_audio_dict(song_yt_id)

    return audio_info

def fetch_song_id(search_string) -> str:
    search: dict = YoutubeSearch(search_string, max_results=1).to_dict().pop()
    video_id = search.get('id', None)

    if(video_id == None):
        raise YtSearchException("Could not fetch Id for the song '{}'".format(search_string))

    return video_id

def fetch_all_song_id(search_string) -> list:
    video_id_list = []
    searchList: dict = YoutubeSearch(search_string, max_results=10).to_dict()
    for search in searchList:
        video_id = search.get('id', None)
        if(video_id == None):
            continue
        video_id_list.append(video_id)

    return video_id_list

def get_audio_dict(video_id) -> AudioDetails:
    if(video_id==None):
        return None
    
    return get_piped_audio(video_id)

def get_piped_audio(video_id: str) -> AudioDetails:
    piped_url = "https://pipedapi.kavin.rocks/streams/" + video_id

    resp = requests.get(piped_url)
    if(resp.status_code != 200):
        raise InvalidPipedReponseException()
    
    json_resp: dict = resp.json()

    audio = AudioDetails()
    audio.title = json_resp.get('title', None)
    audio.id = video_id
    audio.duration = json_resp.get('duration', None)
    audio.uploader = json_resp.get('uploader', None)

    all_audio_stream: list[dict] = json_resp.get('audioStreams', None)
    audio_stream = all_audio_stream[0]
    audio.audio_stream = audio_stream.get('url', None)

    if(audio.audio_stream== None):
        raise NoAudioStreamFoundException()
    
    return audio