import sqlite3

class youtube_database:
	conn_db = None
	cursor = None

	def open_database(self):
		self.conn_db = sqlite3.connect("./yt_database.db")
		# enable UTF-8 8-bytes representation
		self.conn_db.text_factory = str
		self.c = self.conn_db.cursor()		

		sql = """CREATE TABLE IF NOT EXISTS videos (
		vid TEXT NOT NULL,
		title TEXT NOT NULL,
		channel_title TEXT, tags TEXT, category TEXT,
		published_date INTEGER, view_count INTEGER, like_count INTEGER, dislike_count INTEGER,
		comment_count INTEGER, list_topics TEXT, audio_lang TEXT,
		PRIMARY KEY (vid),
		UNIQUE(vid));"""
		self.c.execute(sql)
		
		sql = """CREATE TABLE IF NOT EXISTS comments (
		cid TEXT NOT NULL,
		vid TEXT NOT NULL,
		thread_id TEXT NOT NULL,
		comment TEXT NOT NULL,
		published_date INTEGER,
		etag TEXT NOT NULL,
		like_count INTEGER,		
		PRIMARY KEY (cid),
		FOREIGN KEY (vid) REFERENCES videos(vid));"""		
		self.c.execute(sql)
		
		self.c.execute("PRAGMA temp_store = MEMORY")
		self.conn_db.commit()

	def get_comments(self, vid):
		comments = {}

		self.c.execute("SELECT cid, thread_id, comment, published_date, like_count, etag FROM comments WHERE vid = ?", (vid, ))
		rows = self.c.fetchall()

		for row in rows:
			comments.setdefault(row[1], [])
			comments[row[1]].append([row[2], row[3], row[4], row[0], row[5]])

		return comments

	def get_video_infos(self, vid):
		self.c.execute("SELECT vid, title, channel_title, tags, category, published_date, view_count, like_count, dislike_count,	comment_count, list_topics, audio_lang FROM videos WHERE vid = ?", (vid, ))
		video_infos = self.c.fetchone()
		
		list_infos = []
		if video_infos:
			for i in range(len(video_infos)):
				list_infos.append(video_infos[i])

		return list_infos

	def insert_video_db(self, list_infos):
		self.c.execute("INSERT OR IGNORE INTO videos VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", list_infos)
		self.conn_db.commit()
	
	def insert_comment_db(self, vid, comments):
		for thread_id in comments:
			for comment, published_date, like_count, cid, etag in comments[thread_id]:
				self.c.execute("INSERT OR IGNORE INTO comments VALUES (?,?,?,?,?,?,?)", [cid, vid, thread_id, comment, published_date, like_count, etag])
		self.conn_db.commit()