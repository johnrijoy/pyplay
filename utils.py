class AudioDetails:
    id: str
    title: str
    uploader: str
    duration: int
    audio_stream: str

    def __repr__(self) -> str:
        tot_time = "{}m{}s".format(self.duration//60, (self.duration)%60)
        return "< song: '{}' duration: {} >".format(self.title, tot_time)

class AudioState(AudioDetails):
    track_index: int = -1
    current_position: int
    total_duration: int

    def update_audio_details(self, audio: AudioDetails):
        self.id = audio.id
        self.title = audio.title
        self.uploader = audio.uploader
        self.duration = audio.duration
        self.audio_stream = audio.audio_stream

    def get_current_details(self):
        print("song: {}".format(self.title))
        print("uploader: {}".format(self.uploader))
        print("current: {}".format(self.current_position))
        print("total: {}".format(self.total_duration))

    def __repr__(self) -> str:
        curr_time = "{}m{}s".format(self.current_position//60, (self.current_position)%60)
        tot_time = "{}m{}s".format(self.total_duration//60, (self.total_duration)%60)
        return "< song: '{}' playing: 0m0s--{}--{} >".format(self.title, curr_time, tot_time)