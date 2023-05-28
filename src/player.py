import vlc
from fetcher import *
from utils import AudioDetails, AudioState
from vlc_callbacks import on_track_change, on_position_change
from typing import List

class PlaybackController:
    songQ: List[AudioDetails] = []
    mediaList = None
    player = None
    audio_state: AudioState = None
    check_index = 0

    def __init__(self) -> None:
        print("Init musicPlay Object")
        self.mediaList = vlc.MediaList(self.songQ)
        self.player = vlc.MediaListPlayer()
        self.player.get_instance().log_unset()
        self.player.set_media_list(self.mediaList)
        self.audio_state = AudioState()

        # attach event managers
        self.__attach_events()

        

    # Info functions
    
    def check_player_state(self) -> vlc.State:
        #print(self.player.get_state())
        return self.player.get_state()

    def is_playing(self) -> bool:
        if(self.player.is_playing() == 1):
            return True
        return False
    
    def get_now_playing(self) -> AudioState:
        return self.audio_state
    
    # Playback control functions

    def start_playback(self) -> None:
        self.player.play()

    def stop_playback(self) -> None:
        self.audio_state.track_index = -1
        self.player.stop()

    def pause_resume(self) -> None:
        self.player.pause()

    def set_vol(self, volume_level: int) -> int:
        if(volume_level<0 or volume_level>100):
            return -1
        
        mediaPlayer: vlc.MediaPlayer = self.player.get_media_player()
        previous_vol = mediaPlayer.audio_get_volume()
        resp = mediaPlayer.audio_set_volume(volume_level)

        if(resp == 0):
            return previous_vol
        else:
            return -1
        
    def end_player(self):
        self.player.stop()
        self.player.release()
    
    # Music control functions - High Level

    def append_song(self, audio: AudioDetails) -> None:

        if(self.check_player_state() == vlc.State.Ended):
            self.__reset_mediaList()    
            self.__add_song_to_queue(audio)
            self.start_playback()
        else:
            self.__add_song_to_queue(audio)

    def skip_song(self) -> bool:
        if(self.audio_state.track_index == len(self.songQ)-1):
            print("No next song")
            return False
        else :
            self.player.next()
            return True
    
    def remove_index(self, index: int) -> bool:
        if(index > self.audio_state.track_index and index < len(self.songQ)):
            self.__remove_song_from_queue(index)
            return True
        else:
            return False
        
    def remove_last(self)->bool:
        index = len(self.songQ)-1
        return self.remove_index(index)
    
    # Music control functions - Low Level

    def __add_song_to_mediaList(self, songUrl: str) -> None:
        self.mediaList.lock()
        self.mediaList.add_media(songUrl)
        self.mediaList.unlock()

    def __add_song_to_queue(self, audio: AudioDetails) -> None:
        self.__add_song_to_mediaList(audio.audio_stream)
        self.songQ.append(audio)

    def __remove_song_from_queue(self, index: int) -> None:
        self.__remove_song_from_mediaList(index)
        self.songQ.pop(index)

    def __remove_song_from_mediaList(self, index: int) -> None:
        self.mediaList.lock()
        self.mediaList.remove_index(index)
        self.mediaList.unlock()

    def __reset_mediaList(self):
        self.mediaList.release()
        self.mediaList = vlc.MediaList([])
        self.player.set_media_list(self.mediaList)
        self.songQ.clear()
        self.audio_state.track_index = -1

    def __attach_events(self):
        
        mediaPlayer: vlc.MediaPlayer = self.player.get_media_player()
        eventManager = mediaPlayer.event_manager()
        # MediaPlayerPositionChanged
        # MediaPlayerMediaChanged
        eventManager.event_attach(vlc.EventType.MediaPlayerMediaChanged, on_track_change, self)
        eventManager.event_attach(vlc.EventType.MediaPlayerPositionChanged, on_position_change, self)

        # medialListEvents = self.player.event_manager()
        # medialListEvents.event_attach(vlc.EventType.MediaListEndReached, check_event, "Media list ended", self)

    # not in use
    def __update_audio_state(self):
        total_time_ms = self.player.get_media_player().get_length()
        curr_time_ms = self.player.get_media_player().get_time()

        track_index = self.audio_state.track_index

        if(track_index<0 or track_index >= len(self.songQ)):
            raise InvalidTrackIndexException(track_index, len(self.songQ))

        curr_audio_details: AudioDetails = self.songQ[track_index]

        self.audio_state.update_audio_details(curr_audio_details)
        self.audio_state.current_position = curr_time_ms / 1000
        self.audio_state.total_duration = total_time_ms / 1000

    def get_player_debug(self):
        return self.player