import sys, random
from class_api import youtube_api
from word_analysis import word_analysis

class location_object:
	location = ""
	radius = ""

	def __init__(self, location, radius):
		# location is a tuple (latitude, longitude)
		latitude, longitude = location
		self.location = "%.6f,%.6f" % (latitude, longitude)
		# radius defines a circular geo area around location (max is 1 000 000 meters)
		self.radius = "%.0fm" % radius

class client_api:
	ya = None
	wa = None

	def __init__(self, youtube_key):
		self.ya = youtube_api(youtube_key)
		self.wa = word_analysis()

	def save_network(self, filename_net, vid, list_related_vid, depth):
		with open(filename_net + ".net", 'a') as file_net:		
			for related_vid in list_related_vid:
				row = "%s %s %i\n" % (vid, related_vid, depth) 
				file_net.write(row)

	def retrieve_comments(self, list_vid):
		i = 1
		size = len(list_vid)

		for vid in list_vid:
			# printing progression
			sys.stdout.write("%i / %i - %s\r" % (i, size, vid))
			sys.stdout.flush()

			self.ya.request_video_comments(vid)

			i += 1

	def explore_youtube(self, filename_net, list_vid, depth, number_videos, order_criteria = "relevance", location_settings = None):
		list_explored_vid_new = set()
		list_explored_vid_all = set()

		i = 1
		while list_vid:
			list_explored_vid_all.update(list_vid)
			list_explored_vid_new = list_explored_vid_all.copy()

			for vid in list_vid:
				self.ya.request_video_information(vid)
				
				if i < depth:
					list_related_vid = self.ya.request_related_videos(vid, order_criteria, number_videos, location_settings)
					
					self.save_network(filename_net, vid, list_related_vid, i)					
					list_explored_vid_new.update(list_related_vid)

			list_vid = list_explored_vid_new - list_explored_vid_all
			i += 1

		return list_explored_vid_all

	# explore len(list_vid) * power(nb_best_matching, depth)
	# for example a list of 4 video with depth = 2 and nb_best_matching = 5 then explore : 4 * 5^2 = 100 videos
	def explore_youtube_by_wordlist(self, filename_net, list_vid, depth, wordlist, number_videos, nb_best_matching, order_criteria = "relevance", location_settings = None):
		list_explored_vid_new = set()
		list_explored_vid_all = set()

		i = 1
		while list_vid:
			list_explored_vid_all.update(list_vid)
			list_explored_vid_new = list_explored_vid_all.copy()

			for vid in list_vid:
				self.ya.request_video_information(vid)

				if i < depth:
					list_related_vid = self.ya.request_related_videos(vid, order_criteria, number_videos, location_settings)
					
					list_matching_vid = []
					for related_vid in list_related_vid:
						comments = self.ya.request_video_comments(related_vid)
						matching_score = self.wa.get_comments_matching(comments, wordlist)
						
						if matching_score > 0.0:
							list_matching_vid.append((matching_score, related_vid))

					if list_matching_vid:
						list_vid_best_matching = zip(*sorted(list_matching_vid, reverse=True))[1][:nb_best_matching]
						list_score = zip(*sorted(list_matching_vid, reverse=True))[0][:nb_best_matching]
					
						self.save_network(filename_net, vid, list_vid_best_matching, i)
						list_explored_vid_new.update(list_vid_best_matching)

			list_vid = list_explored_vid_new - list_explored_vid_all
			i += 1

		return list_explored_vid_all

	def explore_youtube_randomly(self, number_hits):
		list_vid = []
		nb_sample = 15

		wa.build_corpus()

		for i in range(number_hits):
			# printing progression
			sys.stdout.write("%i / %i\r" % (i+1, number_hits))
			sys.stdout.flush()

			random_term = self.wa.get_random_word()
			list_related_vid = self.get_list_video_by_termlist([random_term], nb_sample)
			if list_related_vid:
				list_vid.append(list_related_vid[random.randint(0, len(list_related_vid)-1)])

		return list_vid


	def get_list_video_by_termlist(self, termlist, number_videos, order_criteria = "relevance", location_settings = None):
		list_related_vid = self.ya.request_termed_videos(order_criteria, termlist, number_videos, location_settings)

		for related_vid in list_related_vid:
			self.ya.request_video_information(related_vid)

		return list_related_vid
