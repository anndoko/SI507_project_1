import math # for length calculation

class Media:

	def __init__(self, title = "No Title", author = "No Author", year = "No Year"):
		self.title = title
		self.author = author
		self.release_year = year

	def __str__(self):
		return "{} by {} ({})".format(self.title, self.author, self.release_year)

	def __len__(self):
		return 0


## Other classes, functions, etc. should go here

# Song (subclass of Media)
class Song(Media):

	def __init__(self, album = "No Album", genre = "No Genre", track_len = 0):
		super().__init__()
		self.album = album
		self.genre = genre
		self.len = track_len

	def __str__(self):
		return super().__str__() + " [{}]".format(self.genre)

	def __len__(self):
		len_in_secs = self.len / 1000
		return len_in_secs

# Movie (subclass of Media)
class Movie(Media):

	def __init__(self, rating = "No Rating", movie_len = 0):
		super().__init__()
		self.rating = rating
		self.len = movie_len

	def __str__(self):
		return super().__str__() + " []".format(self.rating)

	def __len__(self):
		len_in_mins = math.ceil(self.len / 1000 / 60) # round time to the nearest minute
		return len_in_mins

if __name__ == "__main__":
	# your control code for Part 4 (interactive search) should go here
	pass
