from youtube_search import YoutubeSearch
"""
the YoutubeSearch returns list of dicts with following keys
'id' - video id
'thumbnails' - url to thumbnails, is list of urls
'title' - video title                              ******
'long_desc' - video description
'channel' - name of channel
'duration' - video duration in HH:MM:SS            *******
'views' - total views
'publish_time' - upload time
'url_suffix' - video url suffix                    *******
"""

def get_search(sng_name):
	
	search_list = []
	
	results = YoutubeSearch(sng_name, max_results=10).to_dict()

	for result in results:
		search_list.append("https://www.youtube.com"+result['url_suffix'])

	return search_list, results
	
def get_relevant_url(sng_name):
	
	music = {}
	
	search_list, results = get_search(sng_name)
	
	music['title'] = results[0]['title']
	music['duration'] = results[0]['duration']
	music['url'] = search_list[0]
	
	return music
	
#if __name__ == "main":	
#	print(get_search("Right Here Waiting"))
