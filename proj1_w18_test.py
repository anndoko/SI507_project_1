import unittest
import proj1_w18 as proj1

class TestMedia(unittest.TestCase):

    def testConstructor(self):
        m1 = proj1.Media()
        m2 = proj1.Media("1999", "Prince")

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")
        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")

class TestSong(unittest.TestCase):
    # test the subclass of Media: Song
    def testSongConstructor(self):
        s1 = proj1.Song()
        s2 = proj1.Song("A Day In The Life", "The Beatles", "1967", "Sgt. Pepper's Lonely Heart Club Band", "Rock", 331000)

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
        self.assertEqual(s1.len, 0)

        # test the instance variables of s2
        self.assertEqual(s2.title, "A Day In The Life")
        self.assertEqual(s2.author, "The Beatles")
        self.assertEqual(s2.release_year, "1967")
        self.assertEqual(s2.album, "Sgt. Pepper's Lonely Heart Club Band")
        self.assertEqual(s2.genre, "Rock")
        self.assertEqual(s2.len, 331000)

        # test __str__ and __len__ methods
        self.assertEqual(s1.__str__(), "No Title by No Author (No Year) [No Genre]")
        self.assertEqual(s1.__len__(), 0)
        self.assertEqual(s2.__str__(), "A Day In The Life by The Beatles (1967) [Rock]")
        self.assertEqual(s2.__len__(), 331)


class TestMovie(unittest.TestCase):
    # test the subclass of Media: Movie
    def testMovieConstructor(self):
        mv1 = proj1.Movie()
        mv2 = proj1.Movie("Battle of the Sexes", "Jonathan Dayton, Valerie Faris", "2017", "PG-13", 7259999)

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
        self.assertEqual(mv1.len, 0)

        # test the instance variables of mv2
        self.assertEqual(mv2.title, "Battle of the Sexes")
        self.assertEqual(mv2.author, "Jonathan Dayton, Valerie Faris")
        self.assertEqual(mv2.release_year, "2017")
        self.assertEqual(mv2.rating, "PG-13")
        self.assertEqual(mv2.len, 7259999)

        # test __str__ and __len__ methods
        self.assertEqual(mv1.__str__(), "No Title by No Author (No Year) [No Rating]")
        self.assertEqual(mv1.__len__(), 0)
        self.assertEqual(mv2.__str__(), "Battle of the Sexes by Jonathan Dayton, Valerie Faris (2017) [PG-13]")
        self.assertEqual(mv2.__len__(), 121)


	# OFFICE HOURS:
	# use the json file provided by the class to test Part 2.
	# for Part 3. test if the functions work and if the number of the results exceed the range
    # should be 50 or less

unittest.main()
