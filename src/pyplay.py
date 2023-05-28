'''
to extract audio from links, stream/download and channel it through speaker  
'''
from player import PlaybackController
from frontend_cli import start_pyplay_cli

player = PlaybackController() 

if __name__ == '__main__':
	start_pyplay_cli(player)

