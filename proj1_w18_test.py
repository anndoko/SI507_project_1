import unittest
import proj1_w18 as proj1
import json


# PART 1.
# test the Media class
class TestMedia(unittest.TestCase):

    def testConstructor(self):
        m1 = proj1.Media()
        m2 = proj1.Media("1999", "Prince")

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")
        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")

        # test __str__ and __len__ methods
        self.assertEqual(m1.__str__(), "No Title by No Author (No Year)")
        self.assertEqual(m1.__len__(), "N/A")
        self.assertEqual(m2.__str__(), "1999 by Prince (No Year)")
        self.assertEqual(m2.__len__(), "N/A")

# test the subclass of Media: Song
class TestSong(unittest.TestCase):
    def testSongConstructor(self):
        s1 = proj1.Song()
        s2 = proj1.Song(title = "A Day In The Life", author =  "The Beatles", year = "1967", album = "Sgt. Pepper's Lonely Heart Club Band", genre = "Rock", track_len = 331000)

        # test the instances
        self.assertIsInstance(s1, proj1.Media) # check if it's a sub-instance of Media
        self.assertIsInstance(s1, proj1.Song) # check if it's a instance of Song
        self.assertIsInstance(s2, proj1.Media)
        self.assertIsInstance(s2, proj1.Song)

        # test the instance variables of s1 (the defaults)
        self.assertEqual(s1.title, "No Title")
        self.assertEqual(s1.author, "No Author")
        self.assertEqual(s1.release_year, "No Year")
        self.assertEqual(s1.album, "No Album")
        self.assertEqual(s1.genre, "No Genre")
        self.assertEqual(s1.len, "N/A")

        # test the instance variables of s2
        self.assertEqual(s2.title, "A Day In The Life")
        self.assertEqual(s2.author, "The Beatles")
        self.assertEqual(s2.release_year, "1967")
        self.assertEqual(s2.album, "Sgt. Pepper's Lonely Heart Club Band")
        self.assertEqual(s2.genre, "Rock")
        self.assertEqual(s2.len, 331000)

        # test __str__ and __len__ methods
        self.assertEqual(s1.__str__(), "No Title by No Author (No Year) [No Genre]")
        self.assertEqual(s1.__len__(), "N/A")
        self.assertEqual(s2.__str__(), "A Day In The Life by The Beatles (1967) [Rock]")
        self.assertEqual(s2.__len__(), 331)

# test the subclass of Media: Movie
class TestMovie(unittest.TestCase):
    def testMovieConstructor(self):
        mv1 = proj1.Movie()
        mv2 = proj1.Movie(title = "Battle of the Sexes", author = "Jonathan Dayton, Valerie Faris", year = "2017", rating = "PG-13", movie_len = 7259999)

        # test the instances
        self.assertIsInstance(mv1, proj1.Media) # check if it's a sub-instance of Media
        self.assertIsInstance(mv1, proj1.Movie) # check if it's a instance of Movie
        self.assertIsInstance(mv2, proj1.Media)
        self.assertIsInstance(mv2, proj1.Movie)

        # test the instance variables of mv1 (the defaults)
        self.assertEqual(mv1.title, "No Title")
        self.assertEqual(mv1.author, "No Author")
        self.assertEqual(mv1.release_year, "No Year")
        self.assertEqual(mv1.rating, "No Rating")
        self.assertEqual(mv1.len, "N/A")

        # test the instance variables of mv2
        self.assertEqual(mv2.title, "Battle of the Sexes")
        self.assertEqual(mv2.author, "Jonathan Dayton, Valerie Faris")
        self.assertEqual(mv2.release_year, "2017")
        self.assertEqual(mv2.rating, "PG-13")
        self.assertEqual(mv2.len, 7259999)

        # test __str__ and __len__ methods
        self.assertEqual(mv1.__str__(), "No Title by No Author (No Year) [No Rating]")
        self.assertEqual(mv1.__len__(), "N/A")
        self.assertEqual(mv2.__str__(), "Battle of the Sexes by Jonathan Dayton, Valerie Faris (2017) [PG-13]")
        self.assertEqual(mv2.__len__(), 121)

# PART 2.
class TestJsonDic(unittest.TestCase):

    def testCreateInstance(self):
        # use the json file provided by the class to test Part 2.
        f = open("sample_json.json", "r")
        data_dic = json.load(f)
        f.close()
        # create instances using the create_instance function
        instance_dic = proj1.create_instance(data_dic)
        m1 = instance_dic["OTHER MEDIA:"][0]
        s1 = instance_dic["SONG:"][0]
        mv1 = instance_dic["MOVIE:"][0]

        # test the instances
        self.assertIsInstance(m1, proj1.Media)
        self.assertIsInstance(mv1, proj1.Movie)
        self.assertIsInstance(s1, proj1.Song)

        # test the instance variables of m1
        self.assertEqual(m1.title, "Bridget Jones's Diary (Unabridged)")
        self.assertEqual(m1.author, "Helen Fielding")
        self.assertEqual(m1.release_year, "2012")
        self.assertEqual(m1.info, "https://itunes.apple.com/us/audiobook/bridget-joness-diary-unabridged/id516799841?uo=4")

        # test the instance variables of s1
        self.assertEqual(s1.title, "Hey Jude")
        self.assertEqual(s1.author, "The Beatles")
        self.assertEqual(s1.release_year, "1968")
        self.assertEqual(s1.album, "TheBeatles 1967-1970 (The Blue Album)")
        self.assertEqual(s1.genre, "Rock")
        self.assertEqual(s1.len, 431333)
        self.assertEqual(s1.info, "https://itunes.apple.com/us/album/hey-jude/400835735?i=400835962&uo=4")

        # test the instance variables of mv1
        self.assertEqual(mv1.title, "Jaws")
        self.assertEqual(mv1.author, "Steven Spielberg")
        self.assertEqual(mv1.release_year, "1975")
        self.assertEqual(mv1.rating, "PG")
        self.assertEqual(mv1.len, 7451455)
        self.assertEqual(mv1.info, "https://itunes.apple.com/us/movie/jaws/id526768967?uo=4")

        # test __str__ and __len__ methods
        # m1
        self.assertEqual(m1.__str__(), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")
        self.assertEqual(m1.__len__(), "N/A")
        # s1
        self.assertEqual(s1.__str__(), "Hey Jude by The Beatles (1968) [Rock]")
        self.assertEqual(s1.__len__(), 431)
        # mv1
        self.assertEqual(mv1.__str__(), "Jaws by Steven Spielberg (1975) [PG]")
        self.assertEqual(mv1.__len__(), 125)

# PART 3.
class TestAPI(unittest.TestCase):

    def testQueries(self):
        # test common word: baby
        data1 = proj1.request_itunes_data("baby") # request data
        user_search_results1 = data1["results"] # get the dic
        results_dic1 = proj1.create_instance(user_search_results1) # use the dic to create instances

        # test if the number of results is within the range (50)
        num1 = 0
        for category in results_dic1:
            for instance in category:
                num1 += 1

        self.assertLess(num1, 50)

        # test less common words: helter skelter
        data2 = proj1.request_itunes_data("helter skelter") # request data
        user_search_results2 = data2["results"] # get the dic
        results_dic2 = proj1.create_instance(user_search_results2) # use the dic to create instances

        # test if the number of results is within the range (50)
        num2 = 0
        for category in results_dic2:
            for instance in category:
                num2 += 1

        self.assertLess(num2, 50)

        # test nonsense queries: &@#!$
        data3 = proj1.request_itunes_data("&@#!$") # request data
        user_search_results3 = data3["results"] # get the dic
        results_dic3 = proj1.create_instance(user_search_results3) # use the dic to create instances

        # test if the number of results is within the range (50)
        num3 = 0
        for category in results_dic3:
            for instance in category:
                num3 += 1

        self.assertLess(num3, 50)

        # test blank
        data4 = proj1.request_itunes_data(" ") # request data
        user_search_results4 = data4["results"] # get the dic
        results_dic4 = proj1.create_instance(user_search_results4) # use the dic to create instances

        # test if the number of results is within the range (50)
        num4 = 0
        for category in results_dic4:
            for instance in category:
                num4 += 1

        self.assertLess(num4, 50)

unittest.main()
