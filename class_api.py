import requests, datetime, sys, json
from database import youtube_database

def get_timestampd(str_date):
	# date : 2018-03-28T08:02:07.000Z
	return datetime.datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%s")

def check_videos_db(func):
	def wrapper(*args, **kwargs):
		ya = args[0]
		vid = args[1]

		list_infos = ya.db_youtube.get_video_infos(vid)

		if list_infos:
			return list_infos
		else:
			return func(*args, **kwargs)

	return wrapper

def check_comments_db(func):
	def wrapper(*args, **kwargs):
		ya = args[0]
		vid = args[1]

		comments = ya.db_youtube.get_comments(vid)

		if comments:
			return comments
		else:
			return func(*args, **kwargs)

	return wrapper

class youtube_api:
	http_header = {'accept-encoding':'gzip'}

	url_comments = "https://content.googleapis.com/youtube/v3/comments"
	url_comments_thread = "https://content.googleapis.com/youtube/v3/commentThreads"
	url_search = "https://www.googleapis.com/youtube/v3/search"
	url_videos = "https://content.googleapis.com/youtube/v3/videos"
	url_categories = "https://content.googleapis.com/youtube/v3/videoCategories"

	categories = {}
	api_key = ""
	db_youtube = None

	def __init__(self, api_key):
		self.db_youtube = youtube_database()
		self.db_youtube.open_database()
		self.api_key = api_key
		self.request_video_categories()

	def __valid_request(self, resp):
		if resp.status_code == requests.codes.ok:
			return True
		else:
			resp_js = resp.json()
			sys.stderr.write("Error : %s\n" % (resp_js["error"]["message"]))
			return False

	def request_video_categories(self):
		params = {"key" : self.api_key, "part": "snippet", "regionCode": "US"}
		resp = requests.get(self.url_categories, params, headers=self.http_header)

		if self.__valid_request(resp):
			resp_js = resp.json()

			for item in resp_js["items"]:
				self.categories[item["id"]] = item["snippet"]["title"]

	# ="relevance" / "date" / etc..
	def request_related_videos(self, vid, order, number_video, location_settings):
		list_related_vid = []
		token = ""

		nb_results = 0
		while nb_results < number_video:
			params = {"key" : self.api_key, "part": "id", "type": "video", "order": order, "relatedToVideoId": vid, "maxResults": 20, "pageToken": token}
			if location_settings:
				params["location"] = location_settings.location
				params["locationRadius"] = location_settings.radius

			resp = requests.get(self.url_search, params, headers=self.http_header)

			if self.__valid_request(resp):
				resp_js = resp.json()
				
				for item in resp_js["items"]:
					list_related_vid.append(item["id"]["videoId"])

				if "nextPageToken" in resp_js:
					token = resp_js["nextPageToken"]
				else:
					break

			nb_results += 20

		return list_related_vid[:number_video]

	def request_termed_videos(self, order, list_terms, number_video, location_settings):
		list_related_vid = []
		token = ""

		nb_results = 0
		while nb_results < number_video:
			params = {"key" : self.api_key, "part": "id", "type": "video", "order": order, "q": "|".join(list_terms), "maxResults": 20, "pageToken": token}
			if location_settings:
				params["location"] = location_settings.location
				params["locationRadius"] = location_settings.radius

			resp = requests.get(self.url_search, params, headers=self.http_header)

			if self.__valid_request(resp):
				resp_js = resp.json()

				for item in resp_js["items"]:
					list_related_vid.append(item["id"]["videoId"])

				if "nextPageToken" in resp_js:
					token = resp_js["nextPageToken"]
				else:
					break

			nb_results += 20

		return list_related_vid[:number_video]

	# retrieve from API information about given video "vid" and return a list containing it
	@check_videos_db
	def request_video_information(self, vid):
		params = {"key" : self.api_key, "part": "snippet,statistics,topicDetails", "id": vid}
		resp = requests.get(self.url_videos, params, headers=self.http_header)

		list_infos = []

		if self.__valid_request(resp):
			resp_js = resp.json()

			if "items" not in resp_js or len(resp_js["items"]) == 0 or "snippet" not in resp_js["items"][0]:
				sys.stderr.write("Error : can't retrieve information about %s\n" % vid)
				return list_infos
			
			list_infos.append(vid)

			if "title" in resp_js["items"][0]["snippet"]:
				list_infos.append(resp_js["items"][0]["snippet"]["title"].encode("utf-8"))
			else:
				list_infos.append("UNAMED_VIDEO")

			if "channelTitle" in resp_js["items"][0]["snippet"]:
				list_infos.append(resp_js["items"][0]["snippet"]["channelTitle"].encode("utf-8"))
			else:
				list_infos.append("UNAMED_CHANNEL")

			tags = []
			if "tags" in resp_js["items"][0]["snippet"]:
				for tag in resp_js["items"][0]["snippet"]["tags"]:
					tags.append(tag.encode("utf-8"))
			list_infos.append(", ".join(tags))

			if "categoryId" in resp_js["items"][0]["snippet"]:
				list_infos.append(self.categories[resp_js["items"][0]["snippet"]["categoryId"]])
			else:
				list_infos.append("None")

			if "publishedAt" in resp_js["items"][0]["snippet"]:
				list_infos.append(get_timestampd(resp_js["items"][0]["snippet"]["publishedAt"]))
			else:
				list_infos.append("-1")

			if "viewCount" in resp_js["items"][0]["statistics"]:
				list_infos.append(resp_js["items"][0]["statistics"]["viewCount"])
			else:
				list_infos.append("0")

			if "likeCount" in resp_js["items"][0]["statistics"]:
				list_infos.append(resp_js["items"][0]["statistics"]["likeCount"])
			else:
				list_infos.append("0")

			if "dislikeCount" in resp_js["items"][0]["statistics"]:
				list_infos.append(resp_js["items"][0]["statistics"]["dislikeCount"])
			else:
				list_infos.append("0")

			if "commentCount" in resp_js["items"][0]["statistics"]:
				list_infos.append(resp_js["items"][0]["statistics"]["commentCount"])
			else:
				list_infos.append("0")

			list_topic = []
			if "topicDetails" in resp_js["items"][0]:
				for topic in resp_js["items"][0]["topicDetails"]["topicCategories"]:
					list_topic.append(topic.replace("https://en.wikipedia.org/wiki/", "").encode("utf-8"))
			list_infos.append(", ".join(list_topic))
			
			if "defaultAudioLanguage" in resp_js["items"][0]["snippet"]:
				list_infos.append(resp_js["items"][0]["snippet"]["defaultAudioLanguage"])
			else:
				list_infos.append("NA")

		self.db_youtube.insert_video_db(list_infos[:])

		return list_infos

	@check_comments_db
	def request_video_comments(self, vid):
		comments = {}
		token = ""

		while True:
			params = {"key" : self.api_key, "part": "snippet, replies", "videoId": vid, "maxResults": 100, "pageToken": token}
			resp = requests.get(self.url_comments_thread, params, headers=self.http_header)
			
			if self.__valid_request(resp):
				resp_js = resp.json()

				for item in resp_js["items"]:
					list_comments = []

					if "replies" in item:
						for comment in item["replies"]["comments"]:
							list_comments.append([
								comment["snippet"]["textOriginal"].encode("utf-8"), 
								get_timestampd(comment["snippet"]["publishedAt"]), 
								comment["snippet"]["likeCount"], 
								comment["id"], 
								comment["etag"]
								])

					list_comments.append([
						item["snippet"]["topLevelComment"]["snippet"]["textDisplay"].encode("utf-8"), 
						get_timestampd(item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]), 
						item["snippet"]["topLevelComment"]["snippet"]["likeCount"], 
						item["snippet"]["topLevelComment"]["id"], 
						item["snippet"]["topLevelComment"]["etag"]
						])

					comments[item["id"]] = list_comments[::-1]

				if "nextPageToken" in resp_js:
					token = resp_js["nextPageToken"]
				else:
					break
			else:
				break

		if comments:
			self.db_youtube.insert_comment_db(vid, comments)

		return comments

class yandex:
	http_header = {'accept-encoding':'gzip'}
	url =  "https://translate.yandex.net/api/v1.5/tr.json/translate"
	lang = "en"
	api_key = ""

	def __init__(self, api_key):
		self.api_key = api_key

	def __valid_request(self, resp):
		if resp.status_code == requests.codes.ok:
			return True
		else:		
		 	resp_js = resp.json()
		 	sys.stderr.write("Error - %s\n" % (resp_js["message"]))
			return False
	
	def build_wordlist(self, base_wordlist_en, lang_support):
 		wordlist = list()

 		for word in base_wordlist_en:
 			# add english word
 			wordlist.append(word)

 			for lang in lang_support:
 				list_translation = self.translate(word, lang)

 				for trans in list_translation:
 					wordlist.append(trans.lower())

 		return list(set(wordlist))

	def translate(self, text, to_lang):
		lang_dir = self.lang + "-" + to_lang
		params = {"key": self.api_key, "text": text, "lang": lang_dir}
		
		resp = requests.get(self.url, params, headers=self.http_header)

		if self.__valid_request(resp):
			resp_js = resp.json()

			list_trans = resp_js["text"]
			new_list_trans = []

			for trans in list_trans:
				if trans != text:
					new_list_trans.append(trans.encode("utf-8"))
			
			return new_list_trans
		else:
			return []