import json, pprint, sys
from client_api import client_api, location_object
from class_api import yandex


########### '''''''''''''''''' PARAMS '''''''''' [[[[[[[[]]]]]]]]
#"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""#


#print json.dumps(resp_js,indent=4, sort_keys=True)

# list_chills = ["chills", "tremors", "temperature", "shivers", "goosebumps", "piloerection", "frisson", 
# "feeling of cold", "cutis anserina", "gooseflesh", "horripilation", "thrills"]

# list_chills_v2 = ['shivers', 'quiver', 'shivering', 'charge up', 'agitate', 'energise', 'hasten', 
# 'tickle pink', 'tremble', 'shudder', 'turn on', 'goose bump', 'tickle', 'horripilation', 'vibrate', 
# 'inebriate', 'exalt', 'exhilarate', 'goose skin', 'beatify', 'throb', 'excite', 'induce', 'commove', 
# 'tingle', 'goose pimple', 'goosebump', 'shiver', 'pilomotor reflex', 'rouse', 'chill', 'frisson', 
# 'thrill', 'energize', 'gooseflesh', 'stimulate', 'chills', 'gelidity', 'hair', 'standing on end', 
# 'cold', 'spine']

# list_chills_v3 = ['shivers', 'quiver', 'shivering', 'agitate', 'hasten', 'tickle pink', 'tremble', 
# 'shudder', 'goose bump', 'tickle', 'horripilation', 'inebriate', 'exalt', 'exhilarate', 'goose skin', 
# 'throb', 'excite', 'induce', 'commove', 'tingle', 'goose pimple', 'goosebump', 'shiver', 'pilomotor reflex',
# 'rouse', 'chill', 'frisson', 'thrill', 'energize', 'gooseflesh', 'stimulate', 'chills', 'hair rising', 
# 'hairs standing on end', 'standing on end', 'cold', 'spine']

## Can be used to search for videos having high occurencies of these words in their comments
base_wordlist_en = ["chills", "chill", "shivers", "shiver", "shivering", "goosebump", "goosebumps", "goose bump", "goose bumps",
	"piloerection", "frisson", "frissons", "gooseflesh", "horripilation", 
	"thrills", "shivering", "gooseflesh", "goose flesh", "goose bump", "goose pimple",
	"feeling of cold", "cold in spine", "down spine", "cold in back", 
	"hairs rising", "hairs standing", "hairs tickling",
	"hairs rising", "hairs standing", "hairs tickling"]
# this wordlist contains all words f rom base_wordlist_en translated into these langs : "fr", "es", "ru", "it", "de", "zh", "vi", "ja", "pt"
base_wordlist = ['hairs rising', u'\u9e45\u8089', u'les poils debout', u'piloerektion', 'shivering', u'\u4e0b\u810a\u690e', u'freddo in colonna', u's\u1ee3i l\xf4ng c\xf9', u'haare stehen', u'\u9e45\u649e', u'sensa\xe7\xe3o de frio', u'ganso colis\xe3o', u'\u6bdb\u7acb', u"pelle d'oca", u'temblando', u'\u4e0d\u5bd2\u800c\u6817', u'r\xf9ng m\xecnh', u'arrepios', u'\u043f\u0438\u043b\u043e\u044d\u0440\u0435\u043a\u0446\u0438\u044f', u'run r\u1ea9y', u'\u1edbn l\u1ea1nh', 'hairs tickling', u'piel de gallina', u'xu\u1ed1ng c\u1ed9t s\u1ed1ng', u'\u51b7\u9759', 'goose pimple', u'\u30b0\u30fc\u30b9\u30d0\u30f3\u30d7', 'goosebumps', u'ganso de espinilla', u'\u0433\u0443\u0441\u0438\u043d\u0430\u044f \u043a\u043e\u0436\u0430', 'feeling of cold', 'frissons', u'capelli in piedi', u'pelos parados', u'\u6218\u6817', u'el aumento de los pelos', u'frisson', u"d'oca brufolo", u's\u1ee3i l\xf4ng \u0111\u1ee9ng', 'cold in spine', u'haare steigende', 'gooseflesh', u'\u6bdbtickling', u'c\u1ea3m gi\xe1c m\u1ea1nh', u'l\u1ea1nh \u1edf x\u01b0\u01a1ng s\u1ed1ng', u'gi\xf9 per la colonna vertebrale', u'\u98a4\u6296', u'\u6bdb\u4e0a\u5347', u'les poils de la hausse des', u'escalofr\xedos', u'\u0432\u043e\u043b\u043e\u0441\u044b \u0432\u0441\u0442\u0430\u044e\u0442', u'carne de ganso', u'des frissons', u'\u9aea\u306e\u4e0a\u6607', u'\u0434\u0440\u043e\u0436\u044c', u'\u6bdb\u7ad9', u'l\u1ea1nh \u1edf l\u1ea1i', u'goose bosse', u'cabelos crescente', u'gans-pickel', u'k\xe4lte im r\xfccken', 'shivers', u'\u60aa\u5bd2', u'\u0433\u0443\u0441\u0438\u043d\u044b\u0445 \u043f\u0443\u043f\u044b\u0440\u044b\u0448\u0435\u043a', u'tremendo', u'sensaci\xf3n de fr\xedo', u'\u30e0\u30ba\u30e0\u30ba', u'schauder', u'\u0432\u043e\u043b\u043e\u0441\u044b \u0440\u0430\u0441\u0442\u0443\u0442', u'brividi', u'brivido', u"d'oca bump", u'la piel de gallina', u'freddo nella schiena', u'temblar', 'goose flesh', u'\u7acb\u6bdb', u'\u043e\u0449\u0443\u0449\u0435\u043d\u0438\u0435 \u0445\u043e\u043b\u043e\u0434\u0430', u'\u9e21\u76ae\u7599\u7629', u'\u0445\u043e\u043b\u043e\u0434\u043e\u043a', u'ganso carne', u'tiembla', u'arrepio', u'\u9e45\u7599\u7629', u'froid dans le dos', u'\u5bd2\u6218', u'\u0434\u0440\u043e\u0436\u0430', 'goose bumps', u'emociona', u'goose m\u1ee5n', u'\u51b7\u5728\u56de', 'chills', u'gef\xfchl von k\xe4lte', 'piloerection', u'\u0433\u0443\u0441\u0438\u043d\u0430\u044f \u043f\u043b\u043e\u0442\u044c', u'fr\xedo en la espina', 'hairs standing', u'\u043c\u0443\u0440\u0430\u0448\u043a\u0438 \u043f\u043e \u043a\u043e\u0436\u0435', u'\u30f4\u30cb\u30ad\u30d3', u'\u043e\u0437\u043d\u043e\u0431', u'cabelos c\xf3cegas', u'\u611f\u51b7', u'\u0432\u043d\u0438\u0437 \u043f\u043e\u0437\u0432\u043e\u043d\u043e\u0447\u043d\u0438\u043a\u0430', 'horripilation', u'nervenkitzel', u'\u51b7\u5728\u810a\u67f1', 'shiver', u'\u5bd2\u3044\u810a\u690e', u's\u1ee3i l\xf4ng rising', u'\u30b0\u30fc\u30b9\u8089', u'capelli solletico', u'goose chair', u'ansa.it', u'\u043e \u043c\u043d\u043e\u0433\u043e\u043c \u0433\u043e\u0432\u043e\u0440\u0438\u0442', u'\u611f\u89c9\u51b7', u'\u9ce5\u808c\u304c\u7acb\u3064', u'cabelos em p\xe9', u'schauer', u'la chair de poule', 'goosebump', u'piloerezione', 'chill', u'piloerecci\xf3n', u'freddo', u'peli in aumento', u'frio na parte de tr\xe1s', u'\u4e0b\u690e', 'goose bump', u'emozioni', u'\u3076', u'ganso de golpe', u'th\u1ecbt ng\u1ed7ng', u'\u51b7\u306b\u623b\u308b', u'fr\xedo en la espalda', u'wirbels\xe4ule hinunter', u'en bas de la colonne vert\xe9brale', u'les poils de chatouilles', u'ganso espinha', 'cold in back', 'thrills', u'k\xe4lte in der wirbels\xe4ule', u'enfriar', u'\u53d1\u6296', u'sch\xfcttelfrost', u'\u30b9\u30ea\u30eb', u'goose bourgeon', u'los pelos de las cosquillas', u'n\u1ed5i da g\xe0', u'\u0445\u043e\u043b\u043e\u0434\u0430 \u0432 \u043f\u043e\u0437\u0432\u043e\u043d\u043e\u0447\u043d\u0438\u043a\u0435', u"l'horripilation", u'le froid de la colonne vert\xe9brale', u'\u0432\u043e\u043b\u043d\u0435\u043d\u0438\u0435', u'\u043c\u0443\u0440\u0430\u0448\u043a\u0438 ', u'sensazione di freddo', u'\u5934\u53d1\u75d2\u75d2', u'abajo de la columna vertebral', u'\u0445\u043e\u043b\u043e\u0434 \u0432 \u0441\u043f\u0438\u043d\u0435', u'\u614c', u'frio', u'sensation de froid', u'c\u1ea3m gi\xe1c l\u1ea1nh', u'\u0433\u0443\u0441\u0438\u043d\u0430\u044f \u0443\u0434\u0430\u0440', u'zittern', 'down spine', u'haare kitzeln', u'g\xe4nsehaut', u'\u523a\u6fc0', u"la pelle d'oca", u'para baixo da espinha', u'\u0432\u043e\u043b\u043e\u0441\u0438\u043a\u0438 \u0449\u0435\u043a\u043e\u0447\u0443\u0442', u'frio na espinha']


list_term = ["chills", "goosebumps", "frisson", "gooseflesh", "horripilation", "thrills", "goosebumps live"]
#list_term = ["chills", "goosebumps", "frisson"]

video_batch = ["fRL447oDId4", "kP218E7Ekuc", "VtdbyugYO7A", "MeAskiCHdbE",
			   "xpzdB0G3TJU", "1koa2xAxCAw", "J6bGnSEwdKY", "RxabLA7UQ9k", "8waJ7W3QcJc",
 			   "8tz7UHGnjq4", "YDOENZediM8", "buA3tsGnp2s", "w8HdOHrc3OQ", "dncVUXs_OP8",
 			   "fQhj_aKQkBY", "AGRfJ6-qkr4", "vD-tWNJ5Orc"]
#video_batch = ["kP218E7Ekuc"]


########### '''''''''''''''''' EXEC '''''''''''' [[[[[[[[]]]]]]]]
#"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""#

## east europe 
# lo_eu = location_object((46.720,8.693), 900000)
## taiwan
# lo_tw = location_object((23.831,121.394), 279418)
## west USA
# lo_wus = location_object((36.769,-85.784), 1000)
# lo_rd = location_object((16.598998,20.088853),339294.38)

youtube_key = "AIzaSyCxjD8L9yI6yRcFPNZ7brKMFzQhOWN0zIs"
yandex_key = "trnsl.1.1.20190107T142924Z.19d76f10aaa3f91a.d71c13fe003a8f682eb122f346caf47691eec038"

ca = client_api(youtube_key)

#### EXPLORATION BASED ON CRITERIA (wordlist) 
# yx = yandex(yandex_key)
# wordlist = yx.build_wordlist(base_wordlist_en, lang_support)
# list_vid = ca.explore_youtube_by_wordlist("exploration_chills_wordlist1", video_batch, 4, wordlist, 15, 4)

# list_vid = ca.explore_youtube_by_wordlist("exploration_chills_wordlist2", video_batch, 4, base_wordlist, 15, 4)

#### BASIC EXPLORATION 
# list_vid = ca.explore_youtube("exploration_by_relevance", video_batch, 2, 5)

#### EXPLORATION USING A LIST OF TERMS
# list_vid = []
# for term in list_term:
# 	list_vid.extend(ca.get_list_video_by_termlist([term], 20))

# list_vid = set(list_vid)
list_vid = []
list_terms_v3 = [["chills"], ["frisson", "hairs rising", "horripilation"],["goosebumps", "goose bump", "goose pimple"]]
for list_terms in list_terms_v3:
 	list_vid.extend(ca.get_list_video_by_termlist(list_terms, 40))
list_vid = set(list_vid)

#### RANDOM EXPLORATION 
# list_vid = ca.explore_youtube_randomly(500)

print "Number of discovered videos :", len(list_vid)
with open("out_list_vid.txt", 'w') as file:
	for vid in list_vid:
		file.write("%s\n" % vid)

#with uft-8 = "e4dT8FJ2GE0"

# print "Retrieving comments from videos. This can take some times..."
# request from YT_API all comments and store them in the DB
#ca.retrieve_comments(list_vid)

