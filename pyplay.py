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
"""
# commands


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

def welcome_msg():
	print("--------------- PYPLAY ----------------------")
	print()
	print("Welcome to Pyplay.\nEnter HELP for list of commands")
	print("\nplay song_name \n")
	print("to start playing a song")
	print("---------------------------------------------")

class pyplay(object):
	
	def __init__(self, sng_name=None, quality = 'h'):
		
		try:
			self.player.stop()
		except:
			pass
		
		if sng_name != None:
			search = crawl.get_relevant_url(sng_name)
			music, yt = get_audio_url(search['url'], quality)
			q = [music.url]
			qname = [yt]
			
			mediaList = vlc.MediaList(q)
			player = vlc.MediaListPlayer()
			player.set_media_list(mediaList)
			
			play_state = 1
			player.play()
		else:
			q, qname, mediaList = None, None, None
			player = vlc.MediaListPlayer()
			play_state = 0
		
		instance = player.get_instance()                           #getting instance
		instance.log_unset()                                       #unsetting log
		
		self.q = q
		self.qname = qname
		self.mediaList = mediaList
		self.quality = quality
		self.player = player
		self.exit_state = False
		self.play_state = play_state
		
		#pass
	
	
	def play(self, sng_name = None, quality = None, url = False):
		
		
		
		player = self.player
		if quality == None:
			self.quality = quality
		
		if sng_name != None and len(sng_name) !=0:
			try:
				self.player.release()
			except:
				pass
			try:
				self.MediaList.release()
			except:
				pass
			
			if url == False:
				search = crawl.get_relevant_url(sng_name)
				music, yt = get_audio_url(search['url'], self.quality)
			else:
				music, yt = get_audio_url(sng_name, self.quality)
			
			q = [music.url]
			qname = [yt]
			mediaList = vlc.MediaList(q)
			player = vlc.MediaListPlayer()
			player.set_media_list(mediaList)
			
			self.q = q
			self.qname = qname
			self.mediaList = mediaList
			self.player = player
			self.play_state = 1
		
		player.play()
		
		mediaList = self.mediaList
		if mediaList == None:
			print("No song in playlist")
		
		#pass
	
	
	def pause(self):
		player = self.player
		player.pause()
		
		#pass
	
	
	def skip(self):
		player = self.player
		player.next()
		
		#pass
	
	
	def add(self, sng_name, quality = None):
		# to add a song to queue
		player = self.player
		q = self.q
		qname = self.qname
		mediaList = self.mediaList
		
		if sng_name != None:
			search = crawl.get_relevant_url(sng_name)
			music, yt = get_audio_url(search['url'], self.quality)
			q.append(music.url)
			qname.append(yt)
			mediaList.add_media(music.url)
			
			self.q = q
			self.qname = qname
			self.mediaList = mediaList
		
		#pass
	
	
	def show_q(self):
		player = self.player
		q = self.q
		qname = self.qname
		mediaList = self.mediaList
		
		mediaList.lock()
		
		count = mediaList.count()
		if count == len(q):
			
			for vid in qname:
				print(vid.title, " || ", vid.duration)
		mediaList.unlock()
		
		#pass
	
	
	def remove_last(self):
		player = self.player
		mediaList = self.mediaList
		
		mediaList.lock()
		count = mediaList.count()			
		mediaList.unlock()
		
		self.remove(count-1)
		
		self.player = player
		self.mediaList = mediaList
		#pass
	
	
	def search_sng(self, sng_name):
		search_urls, results = crawl.get_search(sng_name)
		i = 1
		for result in results:
			print(i, ' -- ', result['duration'], ' -- ', result['title'][:20])
			i += 1
		print("\nEnter number to select or 0 to go back")
		
		try:
			search_ind = int(input(">> "))
			if search_ind == 0:
				pass
			else:
				i = search_ind-1
				try:
					sng_url = search_urls[i]
					if self.play_state == 1:
						self.add_url(sng_url)
					else:
						self.play(sng_url, url=True)
				except:
					print("<not valid!>")
		except:
			print("<not valid!>")
		
	
	# insider methods
	
	def player(self):
		# debug feature
		return self.player
		
	def stop(self):
		player = self.player
		player.stop()
		
		#pass
	def set_vol(self, vol):
		try:
			vol = int(vol)
			listPlayer = self.player
			player = listPlayer.get_media_player()
			current_vol = player.audio_get_volume()
			ret = player.audio_set_volume(vol)
			if ret == 0:
				print("[vol set: ", current_vol, "-->", vol, "]")
			else:
				print("<not valid!>")
		except:
			print("<not valid!>")
	
	def end(self):
		player = self.player
		inst = player.get_instance()
		inst.release()
		
		self.exit_state = True
		#pass
	
	def add_url(self, sng_url, quality = None):
		# to add a song to queue
		player = self.player
		q = self.q
		qname = self.qname
		mediaList = self.mediaList
		
		if sng_url != None:
			music, yt = get_audio_url(sng_url, self.quality)
			q.append(music.url)
			qname.append(yt)
			mediaList.add_media(music.url)
			
			self.q = q
			self.qname = qname
			self.mediaList = mediaList
	
	
	def remove(self, i):
		player = self.player
		q = self.q
		qname = self.qname
		mediaList = self.mediaList
		
		mediaList.lock()
		mediaList.remove_index(i)
		q.pop(i)
		qname.pop(i)
		
		mediaList.unlock()
		self.player = player
		self.q = q
		self.qname = qname
		self.mediaList = mediaList
	
	def help(self):
		print("play <song_name>")
		print("add <song_name> - to add song to queue")
		print("search <song_name>")
		print("showq   - to show all songs in the playlist")
		print("pause")
		print("stop")
		print("rmlast  - remove last added song")
		print("skip")
		print("setvol <0-100> - enter value between 0 and 100 to set volume")
		print("end     - to end pyplay")
		#pass
	
	
	def get_command(self):
		
		inp = input("-- ")
		
		inp = inp.split(' ')
		command = (inp.pop(0)).lower()
		inp = ' '.join(inp)
		
		if command == 'play': # and len(inp) != 0:
			self.play(inp)
		elif command == 'add':
			self.add(search)
		elif command == 'pause' or command == 'resume': # or (command == 'play' and len(inp)==0):
			self.pause()
		elif command == 'skip':
			self.skip()
		elif command == 'showq':
			self.show_q()
		elif command == 'rmlast':
			self.remove_last()
		elif command == 'search':
			self.search_sng(inp)
		elif command == 'setvol':
			self.set_vol(inp)
		
		elif command == 'stop':
			self.stop()
		elif command == 'end':
			self.end()
		elif command == 'help':
			self.help()
		else:
			print("Enter a valid command. Type HELP for list of available commands")



# readymade pyplay object
p = pyplay() 

if __name__ == '__main__':
	
	welcome_msg()
	while True:
		p.get_command()
		if p.exit_state:
			break

