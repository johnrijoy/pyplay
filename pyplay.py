'''
to extract audio from links, stream/download and channel it through speaker  
'''
import pafy
import vlc
import webcrawler as crawl
#import os
#os.environ["VLC_VERBOSE"] = "-2"
"""
for playing music from a given youtube link.
A webcrawler will be designed to crawl the youtube for a given string to 
search for songs and return the most relevant link.

test url - https://www.youtube.com/watch?v=GeV4j6lo7Yw - Runaway: AURORA

crawl.get_search(song_name)
"--verbose=-1"
"""

def get_audio_url(yt_url, quality ):
	"""
	yt_url - corresponds to the url of the music video
	quality - set the quality of stream.... h - high
	                                        m - medium
	                                        l - low
	output:
	music - object containing the url of the music stream
	yt_vid - object containing the details of the vid
	"""
	yt_vid = pafy.new(yt_url)
	song_name = yt_vid.title
	
	if quality == 'h':
		q = -1
	elif quality == 'l':
		q = 0
	else:
		q = len(yt_vid.audiostreams)//2
	
	music = yt_vid.audiostreams[q]
	
	return music, yt_vid



class pyplay(object):
	
	def __init__(self, sng_name=None, quality = 'h'):
		
		try:
			self.player.stop()
		except:
			pass
		if sng_name != None:
			search = crawl.get_relevant_url(sng_name)
			music, yt = get_audio_url(search['url'], quality)
			player = vlc.MediaPlayer(music.url)
			player.play()
		else:
			music, yt = None, None
			player = vlc.MediaPlayer()
			
		instance = player.get_instance()                           #getting instance
		instance.log_unset()                                       #unsetting log

		self.music = music
		self.yt = yt
		self.quality = quality
		self.player = player
		
	def play(self, sng_name, quality = None):
		
		player = self.player
		if quality == None:
			self.quality = quality
			
		if sng_name != None:
			search = crawl.get_relevant_url(sng_name)
			music, yt = get_audio_url(search['url'], self.quality)
			player.set_mrl(music.url)
			
			self.music = music
			self.yt = yt
			
		player.play()
	
	def pause(self):
		player = self.player
		player.pause()
	
	def stop(self):
		player = self.player
		player.stop()
	
	def end(self):
		player = self.player
		inst = player.get_instance()
		inst.release()



# readymade pyplay object
p = pyplay() 

if __name__ == "main":
	p.play("Runaway")
	r = input()
	p.stop()
