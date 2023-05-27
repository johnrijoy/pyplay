
# callback to be triggerred when player changes to next track
def on_track_change(event, playbackController):

    playbackController.audio_state.track_index += 1
    track_index = playbackController.audio_state.track_index

    if(track_index<0 or track_index >= len(playbackController.songQ)):
        return
    
    curr_audio_details = playbackController.songQ[track_index]
    playbackController.audio_state.update_audio_details(curr_audio_details)


def on_position_change(event, playbackController):

    total_time_ms = playbackController.player.get_media_player().get_length()
    curr_time_ms = playbackController.player.get_media_player().get_time()
    playbackController.audio_state.current_position = curr_time_ms // 1000
    playbackController.audio_state.total_duration = total_time_ms // 1000

def check_event(event, message, playbackController):
    playbackController.check_index += 1
    print("Hello, event called: " + message)
