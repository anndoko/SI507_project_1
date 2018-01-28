# modules
import math # for length calculation
import requests
import json
import webbrowser # for launching the url

# ==================== Define Class & Subclasses ====================
## Media
class Media:
	def __init__(self, title = "No Title", author = "No Author", year = "No Year", url = "No URL", json_dic = None):
		if json_dic is None: # if there's no json dic, the default values are assigned
			self.title = title
			self.author = author
			self.release_year = year
			self.info = url
		else:
			self.author = json_dic["artistName"]
			self.release_year = json_dic["releaseDate"][0:4] # get year only
			if "trackViewUrl" in json_dic: # if trackViewUrl is available, assign it to self.info
				self.info = json_dic["trackViewUrl"]
			else:
				self.info = url

		# for results that are not tracks, assign the value of collectionName
		if json_dic["wrapperType"] != "track":
			self.title = json_dic["collectionName"]
		else:
			self.title = json_dic["trackName"]

	def __str__(self):
		return "{} by {} ({})".format(self.title, self.author, self.release_year)

	def __len__(self):
		return "N/A"

## Other classes, functions, etc. should go here
### Song (subclass of Media)
class Song(Media):
	def __init__(self, title = "No Title", author = "No Author", year = "No Year", url = "No URL", album = "No Album", genre = "No Genre", track_len = "N/A", json_dic = None):
		super().__init__(title, author, year, url, json_dic)
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

### Movie (subclass of Media)
class Movie(Media):
	def __init__(self, title = "No Title", author = "No Author", year = "No Year", url = "No URL", rating = "No Rating", movie_len = "N/A", json_dic = None):
		super().__init__(title, author, year, url, json_dic)
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

# ==================== iTunes API ====================
## data request & caching
itunes_cache_file = "SI507_proj1_cache.json" # set up a file for caching
try:
	cache_file = open(itunes_cache_file, 'r')
	cache_content = cache_file.read()
	CACHE_DICTION = json.loads(cache_content)
	cache_file.close()
except:
	CACHE_DICTION = {}

## to generate a unique id of a request
def unique_id_generator(base_url, params_diction):
	alphabetized_keys = sorted(params_diction.keys())
	lst = []
	for key in alphabetized_keys:
		lst.append("{}-{}".format(key, params_diction[key]))

	# combine the baseurl and the formatted pairs of keys and values
	unique_id = base_url + "_".join(lst)

	# return a unique id of the request
	return unique_id

## get data from the iTunes API
def request_itunes_data(search_string):
	# set up the base URL
	base_url = "https://itunes.apple.com/search"

	# set up a dictionary of parameters
	params_diction = {}
	params_diction["format"] = "json"
	params_diction["term"] = search_string

	# generate a unique id of this search
	unique_id = unique_id_generator(base_url, params_diction)

	# request/cache data
	if unique_id in CACHE_DICTION:
		print("Getting data from the cache file...")
		return(CACHE_DICTION[unique_id])
	else:
		print("Making new data request...")
		results = requests.get(url = base_url, params = params_diction)
		itunes_data_py = json.loads(results.text)
		CACHE_DICTION[unique_id] = itunes_data_py

		cache_file = open(itunes_cache_file,"w")
		cache_string = json.dumps(CACHE_DICTION)
		cache_file.write(cache_string)
		cache_file.close()

		return CACHE_DICTION[unique_id]

# ==================== Other Function  ====================
## check if user input is an integer
def check_if_num(user_input):
	try:
		int(user_input)
		return True
	except:
		return False

if __name__ == "__main__":
	# your control code for Part 4 (interactive search) should go here
	# prompt user for input
	user_input = ""
	user_input = input("Enter a search term, or 'exit' to quit: ")

	while user_input != "exit": # end the program if user enters "exist"

		# if user input is num, launch the link
		# otherwise, make data using the string
		if check_if_num(user_input):
			info_request = instance_lst[int(user_input)]
			try:
				webbrowser.open_new(info_request.info) # open URL
				print("Launching")
				print(info_request.info)
				print("in web browser...")
			except:
				print("No URL is available.")
		else:
			data = request_itunes_data(user_input) # request data
			user_search_results = data["results"] # get the dics

			# create 3 lists for instances of Song, Movie, and Other Media
			song_lst = []
			movie_lst = []
			other_lst = []

			for result in user_search_results:
				# if result is song/movie, create an instance of Song/Movie
				# and add the instance to the song_lst/movie_lst
				if "kind" in result:
					if result["kind"] == "song":
						song_lst.append(Song(json_dic = result))
					if result["kind"] == "feature-movie":
						movie_lst.append(Movie(json_dic = result))

				# other types of results go to the other_lst
				if "kind" not in result:
					other_lst.append(Media(json_dic = result))

			# set an integer variable for indexing
			index_num = 1

			# SONG:
			print("\nSONG")
			for song in song_lst:
				print(index_num, song)
				index_num += 1

			# MOVIE:
			print("\nMOVIE")
			for movie in movie_lst:
				print(index_num, movie)
				index_num += 1

			# OTHER MEDIA:
			print("\nOTHER MEDIA")
			for media in other_lst:
				print(index_num, media)
				index_num += 1

		# prompt user for input again
		user_input = input("Enter a number for more info, or another search term, or exit: ")

	# end the program
	print("Bye!")
