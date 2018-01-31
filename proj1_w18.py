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
            # for tracks, assign the value of trackName and trackViewUrl
            if json_dic["wrapperType"] == "track":
                self.title = json_dic["trackName"]
                self.info = json_dic["trackViewUrl"]
            # for non tracks, assign the value of collectionName and collectionViewUrl
            else:
                self.title = json_dic["collectionName"]
                self.info = json_dic["collectionViewUrl"]

            # assign values to author, and release_year
            self.author = json_dic["artistName"]
            self.release_year = json_dic["releaseDate"][0:4] # get year only

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
        if self.len != "N/A":
            len_in_secs = int(self.len / 1000)
            return len_in_secs
        else:
            return "N/A"

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
        if self.len != "N/A":
            len_in_mins = math.ceil(self.len / 1000 / 60) # round time to the nearest minute
            return len_in_mins
        else:
            return "N/A"

# ==================== iTunes API ====================
## data request & caching
itunes_cache_file = "proj1_cache.json" # set up a file for caching
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

    unique_id = base_url + "_".join(lst) # combine the baseurl and the formatted pairs of keys and values

    return unique_id # return a unique id of the request

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

# ==================== Other Functions  ====================
## ask user for input
def prompt():
    user_input = input("Enter a search term, or 'exit' to quit: ")
    return user_input

## check if user input is an integer
def check_if_num(user_input):
    try:
        int(user_input)
        return True
    except:
        return False

## check if url is available and launch it in user's default browser
def launch_url(url):
    if url != "No URL":
        webbrowser.open_new(url) # open URL
        print("Launching")
        print(url)
        print("in web browser...")
    else:
        print("No URL is available.")

## check what type (song/movie/other_media) the result is and create an instance accordingly
def create_instance(result_lst):
    # # create 3 lists for instances of Song, Movie, and Other Media
    song_lst = []
    movie_lst = []
    other_lst = []

    for result in result_lst:
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

    # return a dictionary of lists
    return {"SONG:": song_lst, "MOVIE:": movie_lst, "OTHER MEDIA:": other_lst}


# ==================== Main  ====================
if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    user_input = prompt() # prompt user for input
    user_search_results = {} # create an empty list to store the results

    # end the program if user enters "exist"
    while user_input != "exit":

        # if user enter a search term (str), make data using the string
        if check_if_num(user_input) == False:
            data = request_itunes_data(user_input) # request data
            user_search_results = data["results"] # get the dic & assign it to user_search_results
            instance_lst_dic = create_instance(user_search_results) # create instances

            # set an integer variable for indexing
            index_num = 1

            # display the instances
            for category in instance_lst_dic:
                print(category) # show type: Song/Movie/Other Media
                for instance in instance_lst_dic[category]: # iterate through each list
                    print(index_num, instance) # print both the index and the instance
                    index_num += 1

        # if user enters a num
        else:
            # if user hasn't done any search yet, ask for input again
            if user_search_results == {}:
                user_input = input("You haven't done any search yet.\nEnter a search term, or 'exit' to quit: ")
                continue
            # if user has done a search before
            else:
                # if user's input exceeds the range, print an error message and ask for input again
                if int(user_input) not in range(1, (len(instance_lst_dic["SONG:"]) + len(instance_lst_dic["MOVIE:"]) + len(instance_lst_dic["OTHER MEDIA:"]) + 1)):
                    print("Please enter a valid index number.")
                else:
                    # convert str to int and get the real index
                    index = int(user_input) - 1
                    # locate the data by checking the real index
                    if index < len(instance_lst_dic["SONG:"]):
                        info_request = instance_lst_dic["SONG:"][index]
                    elif index < (len(instance_lst_dic["SONG:"]) + len(instance_lst_dic["MOVIE:"])):
                        index -= (len(instance_lst_dic["SONG:"]) + len(instance_lst_dic["MOVIE:"]))
                        info_request = instance_lst_dic["MOVIE:"][index]
                    else:
                        index -= (len(instance_lst_dic["SONG:"]) + len(instance_lst_dic["MOVIE:"]) + len(instance_lst_dic["OTHER MEDIA:"]))
                        info_request = instance_lst_dic["OTHER MEDIA:"][index]

                    # try use the url and open it in user's default web browser
                    launch_url(info_request.info)

        # prompt user for input again
        user_input = input("Enter a number for more info, or another search term, or exit: ")

    # end the program
    print("Bye!")
