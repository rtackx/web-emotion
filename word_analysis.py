import sqlite3, random, nltk
from scipy.stats import entropy

# Materials for text analysis
#from bs4 import BeautifulSoup
#import warnings
#warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
#nltk.download("stopwords")
#nltk.download("brown")
#nltk.download("punkt")
from nltk.corpus import stopwords
from nltk.corpus import brown

# 'fuzzywuzzy' doesn't work well with UTF-8 strings
#pip install fuzzywuzzy
#pip install python-levenshtein
#from fuzzywuzzy import process, fuzz

# import re, logging
# logging.getLogger("re").setLevel(logging.WARNING)
# logging.disable(logging.CRITICAL)
# logging.disable(logging.root)
# pattern_user = re.compile("@+\S+")

# import string
# replace_punctuation = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

class word_analysis:
	stop_words = None
	words = list()

	def __init__(self):
		self.stop_words = set(stopwords.words("english"))

	def encode_list(self, list_words):
		list_words_encoded = []
		for w in list_words:
			list_words_encoded.append(w.decode("utf-8"))

		return list_words_encoded

	def build_corpus(self):
		# getting all words from "brown" corpus 
		set_words = []
		for w in brown.words():
			if w not in self.stop_words:
				set_words.append(w.lower())
		self.words = list(set(set_words))
		random.shuffle(self.words)

	def get_random_word(self):
		return self.words[random.randint(0, len(self.words))]

	def get_decomposed_text(self, text, nb_words, mininum_size):
		text = text.split()
		
		dict_words = {}
		for i in range(0, len(text)):
			for n in range(i+1, i+1+nb_words):
				dict_words.setdefault(n-i, set())
				word = " ".join(text[i:n])

				if len(word) >= mininum_size:
					dict_words[n-i].add(word)

		return dict_words

	def is_ascii(self, word):
		is_ascii = True
		try:
			word.decode("ascii")
		except:
			is_ascii = False

		return is_ascii

	def filter_comment(self, comment):
		# soup = BeautifulSoup(comment, features="lxml")
		#text = soup.get_text().lower()
		text = comment.lower()
		# remove user reference, ex : @user2345
		#text = re.sub(pattern_user, "", text)

		return text

	def get_text_nb_matching(self, text, base_wordlist, data_wordlist):
		nb_matching = 0

		max_length_terms = max([len(term.split()) for term in base_wordlist])
		min_length_terms = min([len(term) for term in base_wordlist])
		decomposed_text = self.get_decomposed_text(text, max_length_terms, min_length_terms)
		
		if not decomposed_text:
			return 0

		for term in base_wordlist:
			length_term = len(term.split())
			#term_ascii = self.is_ascii(term)

			for words in decomposed_text[length_term]:
				if len(term) != len(words):
					pass

				if term in words:
					data_wordlist[term] += 1
					nb_matching += 1

				#words_ascii = self.is_ascii(words)

				'''if not term_ascii or not words_ascii:
					if fuzz.partial_ratio(words, term) > 85:						
						#print words, "[" + term + "]", fuzz.partial_ratio(words, term)
						data_wordlist[term] += 1
						nb_matching += 1
				else:
					if fuzz.token_sort_ratio(words, term) > 85:
						#print words, "[" + term + "]", fuzz.token_sort_ratio(words, term)
						data_wordlist[term] += 1
						nb_matching += 1'''

		return nb_matching

	def get_comments_nb_matching(self, comments, base_wordlist):
		data_wordlist = dict(zip(base_wordlist, [0]*len(base_wordlist)))
		nb_matching = 0
		matching_score = 0
		nb_comments = 0

		for thread_id in comments:
			nb_comments += len(comments[thread_id])

			for comment, published_date, like_count, cid, etag in comments[thread_id]:
				text = self.filter_comment(comment)
				
				nb = self.get_text_nb_matching(text, base_wordlist, data_wordlist)
				if nb > 0:
					matching_score += 1
				nb_matching += nb

		if matching_score > 0:
			matching_score = 1.0 * matching_score / nb_comments

		return data_wordlist, nb_matching, matching_score

	# def get_comments_matching(self, comments, wordlist):
	# 	matching_score = 0.0
	# 	nb_matching = 0
	# 	nb_comments = 0

	# 	wordlist_encoded = self.encode_list(wordlist)

	# 	for thread_id in comments:
	# 		nb_comments += len(comments[thread_id])

	# 		for comment, published_date, like_count, cid, etag in comments[thread_id]:
	# 			text = self.filter_comment(comment)

	# 			results_matching = process.extractBests(text, wordlist_encoded, scorer=fuzz.partial_ratio, score_cutoff=100)
	# 			if len(results_matching) > 0:
	# 				nb_matching += 1
		
	# 	if nb_matching > 0:
	# 	 	matching_score = 1.0 * nb_matching / nb_comments
		
	# 	return matching_score

	# With this index 1 represents infinite diversity and 0 no diversity.
	def calc_simpson_index(self, data_wordlist, nb_matching):
		simpson_index = 0.0
		
		for word in data_wordlist:
			if data_wordlist[word] > 0:
				simpson_index += data_wordlist[word] * (data_wordlist[word] - 1)
		
		if nb_matching > 1:
			simpson_index = 1.0 * simpson_index / (nb_matching * (nb_matching - 1))
		
		return 1 - simpson_index

	# With this index 1 represents total concentration and ~>0 homogenous distribution (loyal concurrency)	
	def calc_herfindahl_index(self, data_wordlist, nb_matching):
		herfindahl_index = 0.0
		
		for word in data_wordlist:
			if data_wordlist[word] > 0:
				herfindahl_index += pow(1.0 * data_wordlist[word] / nb_matching, 2)
		
		return herfindahl_index

	def calc_entropy(self, data_wordlist):
		if sum(data_wordlist.values()) > 0:
			return entropy(data_wordlist.values())
		else: 
			return 0