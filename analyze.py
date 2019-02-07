# -*- coding: utf-8 -*-
import csv, time
from word_analysis import word_analysis
from class_api import youtube_api, yandex

# base_wordlist_en_old = ["chills", "chill", "shivers", "shiver", "shivering", "goosebump", "goosebumps", "goose bump", "goose bumps",
# 	"piloerection", "frisson", "frissons", "gooseflesh", "horripilation", 
# 	"thrills", "shivering", "gooseflesh", "goose flesh", "goose bump", "goose pimple",
# 	"feeling of cold", "cold in spine", "down spine", "cold in back", 
# 	"hairs rising", "hairs standing", "hairs tickling",
# 	"hairs rising", "hairs standing", "hairs tickling"]

base_wordlist_en = ["chill", "shiver", "goosebump",	"piloerection", "frisson", "horripilation", 
	"thrills", "feeling of cold", "cold spine",	"hairs rising"]
# "fr", "es", "ru", "it", "de", "zh", "vi", "ja", "pt"
base_wordlist = ['piloerection', '\xe6\xaf\x9b\xe4\xb8\x8a\xe5\x8d\x87', 'sensaci\xc3\xb3n de fr\xc3\xado', 'hairs rising', 'piloerektion', '\xd1\x85\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb4\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbf\xd0\xbe\xd0\xb7\xd0\xb2\xd0\xbe\xd0\xbd\xd0\xbe\xd1\x87\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0', 'sensation de froid', 'l\xe1\xba\xa1nh x\xc6\xb0\xc6\xa1ng s\xe1\xbb\x91ng', 'il freddo della colonna vertebrale', 'sensa\xc3\xa7\xc3\xa3o de frio', 'haare steigende', 'r\xc3\xb9ng m\xc3\xacnh', 'nervenkitzel', '\xd0\xb2\xd0\xbe\xd0\xbb\xd0\xbe\xd1\x81\xd1\x8b \xd1\x80\xd0\xb0\xd1\x81\xd1\x82\xd1\x83\xd1\x82', 'thrills', '\xe3\x82\xb9\xe3\x83\xaa\xe3\x83\xab', '\xe6\x84\x9f\xe5\x86\xb7', '\xd1\x85\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb4\xd0\xbe\xd0\xba', 'enfriar', '\xd0\xbf\xd0\xb8\xd0\xbb\xd0\xbe\xd1\x8d\xd1\x80\xd0\xb5\xd0\xba\xd1\x86\xd0\xb8\xd1\x8f', '\xe6\x84\x9f\xe8\xa7\x89\xe5\x86\xb7', 'horripilation', 'arrepios', 'shiver', 'cabelos crescente', '\xe5\x86\xb7\xe8\x84\x8a\xe6\xa4\x8e', 'piel de gallina', 'chill', "l'horripilation", 'c\xe1\xba\xa3m gi\xc3\xa1c m\xe1\xba\xa1nh', 'brivido', 'schauder', 'cold spine', '\xd0\xbe\xd1\x89\xd1\x83\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x85\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb4\xd0\xb0', 'sensazione di freddo', 'el fr\xc3\xado de la columna vertebral', 'temblar', 'piloerecci\xc3\xb3n', 's\xe1\xbb\xa3i l\xc3\xb4ng', 'frio', 'feeling of cold', '\xe6\x88\x98\xe6\xa0\x97', 'frissons', 'goosebump', '\xe5\x86\xb7\xe9\x9d\x99', '\xe5\x88\xba\xe6\xbf\x80', 'piloerezione', 'zittern', 'frio coluna vertebral', 'frisson', 'arrepio', 'freddo', 'peli in aumento', 'le froid de la colonne vert\xc3\xa9brale', 'c\xe1\xba\xa3m gi\xc3\xa1c l\xe1\xba\xa1nh', 'el aumento de los pelos', 'kalt wirbels\xc3\xa4ule', '\xe7\xab\x8b\xe6\xaf\x9b', '\xe9\xa2\xa4\xe6\x8a\x96', '\xd0\xb4\xd1\x80\xd0\xbe\xd0\xb6\xd1\x8c', '\xe9\xab\xaa\xe3\x81\xae\xe4\xb8\x8a\xe6\x98\x87', 'emozioni', 'emociona', 'gef\xc3\xbchl von k\xc3\xa4lte', '\xd0\xb2\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5']

api_key = "AIzaSyCxjD8L9yI6yRcFPNZ7brKMFzQhOWN0zIs"
ya = youtube_api(api_key)
wa = word_analysis()

# video_namefile = "vid_random500.txt"
# info_videos_csv = "vid_random500.csv"
# count_videos_file = "vid_random500.count"

video_namefile = "vid_terms1.txt"
info_videos_csv = "vid_terms1.csv"
count_videos_file = "vid_terms1.count"

list_vid = set()
with open(video_namefile, 'r') as file:
	for line in file:
		field = line.split()
		list_vid.add(field[0])
		# list_vid.add(field[1])

all_data_wordlist = {}

with open(info_videos_csv, 'w') as filecsv:
	writer = csv.writer(filecsv)
	writer.writerow(["vid", "title", "channel_title", "tags", "category", "published_date", "view_count", "like_count", "dislike_count", "comment_count", "list_topics", "audio_lang", "ratio_matching", "nb_matching", "simpson_index", "herfindahl_index", "entropy"])

	for vid in list_vid:
		infos = ya.request_video_information(vid)
		if infos:
			comments = ya.request_video_comments(vid)

			nb_comments = 0
			for thread_id in comments:
				nb_comments += len(comments[thread_id])
			infos[9] = nb_comments

			data_wordlist, nb_matching, matching_score = wa.get_comments_nb_matching(comments, base_wordlist)
			simpson_index = wa.calc_simpson_index(data_wordlist, nb_matching)
			herfindahl_index = wa.calc_herfindahl_index(data_wordlist, nb_matching)
			entropy = wa.calc_entropy(data_wordlist)

			for word in data_wordlist:
				all_data_wordlist.setdefault(word, 0)
				all_data_wordlist[word] += data_wordlist[word]

			#print nb_matching, matching_score, simpson_index, herfindahl_index

			infos.append(matching_score)
			infos.append(nb_matching)
			infos.append(simpson_index)
			infos.append(herfindahl_index)
			infos.append(entropy)
			print infos

	 		writer.writerow(infos)

with open(count_videos_file, 'w') as file:
	for word in all_data_wordlist:
		file.write(word + ' ' + str(all_data_wordlist[word]) + '\n')
