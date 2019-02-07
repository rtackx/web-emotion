import csv, sqlite3, sys, time

csv.field_size_limit(sys.maxsize)

conn_db = sqlite3.connect("./yt_database.db")
# enable UTF-8 8-bytes representation
conn_db.text_factory = str
c = conn_db.cursor()
c.execute("PRAGMA temp_store = MEMORY")
print "READING DB"
# with open("test/youtube_test_comments.csv", "rb") as file:
#       reader = csv.reader(file)

#       for row in reader:
#               c.execute("INSERT INTO comments VALUES (?,?,?,?,?)", [row[0], row[1], row[2], row[3], row[4]])

#       conn_db.commit()

c.execute("SELECT * FROM videos WHERE vid = 'lKZjgBAZrXA'")
print c.fetchall()
t = time.time()
c.execute("SELECT * FROM comments WHERE vid = 'lKZjgBAZrXA'")
t2 = time.time()
print t2 - t
#print "nb comments :", len(c.fetchall())

