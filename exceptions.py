class PyPlayException(Exception):
    message = None
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class YtSearchException(PyPlayException):
    def __init__(self, message: str = "Error while fetching Song details" ) -> None:
        self.message = message
        super().__init__(message)

class NoSongFoundException(PyPlayException):
    def __init__(self, message: str = "No Song Found" ) -> None:
        self.message = message
        super().__init__(message)

class InvalidPipedReponseException(PyPlayException):
    def __init__(self, message: str = "No Good response from Piped Api" ) -> None:
        self.message = message
        super().__init__(message)

class NoAudioStreamFoundException(PyPlayException):
    def __init__(self, message: str = "No Audio Stream was found" ) -> None:
        self.message = message
        super().__init__(message)

class InvalidTrackIndexException(PyPlayException):
    def __init__(self, track_index: int, queue_length: int ) -> None:
        self.message = "Invalid Current Track Index < index:{} length:{}>".format(track_index, queue_length)
        super().__init__(self.message)