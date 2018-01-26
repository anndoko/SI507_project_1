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

# use iTunes API
# data request & caching
itunes_cache_file = "SI507_proj1_cache.json" # set up a file for caching
try:
    cache_file = open(itunes_cache_file, 'r')
    cache_content = cache_file.read()
    CACHE_DICTION = json.loads(cache_content)
    cache_file.close()
except:
    CACHE_DICTION = {}

# to generate a unique id of a request
def unique_id_generator(base_url, params_diction):
    alphabetized_keys = sorted(params_diction.keys())
    lst = []
    for key in alphabetized_keys:
        lst.append("{}-{}".format(key, params_diction[key]))

    # combine the baseurl and the formatted pairs of keys and values
    unique_id = base_url + "_".join(lst)

    # return a unique id of the request
    return unique_id

# get data from the iTunes API
def request_itunes_data(search_string, search_type = "song"):
    # set up the base URL
    base_url = "https://itunes.apple.com/search"

    # set up a dictionary of parameters
    params_diction = {}
    params_diction["format"] = "json"
    params_diction["term"] = search_string
    params_diction["entity"] = search_type

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

# # test the code
# # use sample_json.json
# data = json.load(open('sample_json.json'))
# m1 = Movie(json_dic = data[0])
# s1 = Song(json_dic = data[1])
# o1 = Media(json_dic = data[2])
# print(m1)
# print(s1)
# print(o1)
# print(m1.__str__())
# print(s1.__str__())
# print(o1.__str__())
# print(m1.__len__())
# print(s1.__len__())
# print(o1.__len__())

if __name__ == "__main__":
	# your control code for Part 4 (interactive search) should go here
	pass
