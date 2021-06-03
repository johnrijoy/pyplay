The project is still under development and incomplete.

packages required:
certifi==2021.5.30
chardet==4.0.0
idna==2.10
pafy==0.5.5
python-vlc==3.0.12118
requests==2.25.1
urllib3==1.26.5
youtube-dl==2021.5.16
youtube-search==2.1.0

USAGE:
1. have vlc installed on the device and following libraries
2. navigate to the folder conatining the python file
3. start an python REPR
    >>> from pyplay import p
    >>> p.play("song name")

COMMANDS:
p.play("song name") - can be used to start playing a song and to change to a different song
p.pause() -  to pause and resume an already playing song.
p.stop() - to stop playing.

COMMENTS:
more functionality will be added later on
