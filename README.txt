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
3. execute the python file
   --python3 pyplay.py
   OR
   open python REPL and
   >>>from pyplay import p
   >>>p.play("song_name")

COMMANDS:
play <song_name> - can be used to start playing a song and to change to a different song
add <song_name> - cad be used to add a song to the queue
search <song_name> - to search for a particular song and add to the queue
pause -  to pause and resume an already playing song.
rmlast - remove last added song
skip - skip the current song
showq - to list all songs in playlist
stop - to stop playing.
end - to end the program
help - to show list of commands

COMMENTS:
more functionality will be added later on
