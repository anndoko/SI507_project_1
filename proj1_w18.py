import math # for length calculation
import requests
import json

# Media
class Media:

	def __init__(self, title = "No Title", author = "No Author", year = "No Year", json_dic = None):
		if json_dic is None:
			self.title = title
			self.author = author
			self.release_year = year
		elif json_dic["wrapperType"] != "track":
			self.title = json_dic["collectionName"]
			self.author = json_dic["artistName"]
			self.release_year = json_dic["releaseDate"][0:4]
		else:
			self.title = json_dic["trackName"]
			self.author = json_dic["artistName"]
			self.release_year = json_dic["releaseDate"][0:4]

	def __str__(self):
		return "{} by {} ({})".format(self.title, self.author, self.release_year)

	def __len__(self):
		return "N/A"

## Other classes, functions, etc. should go here
# Song (subclass of Media)
class Song(Media):

	def __init__(self, title = "No Title", author = "No Author", year = "No Year", album = "No Album", genre = "No Genre", track_len = "N/A", json_dic = None):
		super().__init__(title, author, year, json_dic)
		if json_dic is None:
			self.album = album
			self.genre = genre
			self.len = track_len
		else:
			self.album = json_dic["collectionName"]
			self.genre = json_dic["primaryGenreName"]
			self.len = json_dic["trackTimeMillis"]

	def __str__(self):
		return super().__str__() + " [{}]".format(self.genre)

	def __len__(self):
		len_in_secs = int(self.len / 1000)
		return len_in_secs

# Movie (subclass of Media)
class Movie(Media):

	def __init__(self, title = "No Title", author = "No Author", year = "No Year", rating = "No Rating", movie_len = "N/A", json_dic = None):
		super().__init__(title, author, year, json_dic)
		if json_dic is None:
			self.rating = rating
			self.len = movie_len
		else:
			self.rating = json_dic["contentAdvisoryRating"]
			self.len = json_dic["trackTimeMillis"]

	def __str__(self):
		return super().__str__() + " [{}]".format(self.rating)

	def __len__(self):
		len_in_mins = math.ceil(self.len / 1000 / 60) # round time to the nearest minute
		return len_in_mins

# test the code
# use sample_json.json
data = json.load(open('sample_json.json'))
m1 = Movie(json_dic = data[0])
s1 = Song(json_dic = data[1])
o1 = Media(json_dic = data[2])
print(m1)
print(s1)
print(o1)
print(m1.__str__())
print(s1.__str__())
print(o1.__str__())
print(m1.__len__())
print(s1.__len__())
print(o1.__len__())

if __name__ == "__main__":
	# your control code for Part 4 (interactive search) should go here
	pass
