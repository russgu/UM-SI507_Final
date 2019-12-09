from Final_Project import *
import unittest


class TestGetData(unittest.TestCase):

	def test_tracks(self):

		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		sql = 'SELECT name FROM Tracks'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertIn(('Breathe',), result_list)
		self.assertEqual(len(result_list), 100)

		sql = 'SELECT * FROM Tracks WHERE name like "sh%"'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 3)
		self.assertEqual(result_list[0][4], 219.0)

		conn.close()


	def test_artists(self):

		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		sql = 'SELECT name FROM Artists'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertIn(('ZEDD',), result_list)
		self.assertEqual(len(result_list), 78)

		sql = 'SELECT * FROM Artists WHERE radio = 1'

		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 65)
		self.assertEqual(result_list[0][2], 51)
		conn.close()


	def test_album(self):

		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		sql = 'SELECT name FROM Albums'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertIn(('Easy',), result_list)
		self.assertEqual(len(result_list), 95)

		sql = 'SELECT * FROM Albums WHERE genres = "Alternative"'
		results = cur.execute(sql)
		result_list = results.fetchall()
		self.assertEqual(len(result_list), 3)
		self.assertEqual(result_list[0][2], 1234.0)
		conn.close()


class TestProcessData(unittest.TestCase):

	def test_followers(self):
		results = artist_followers()
		self.assertEqual(results[0][1], 'David Guetta')

		results = artist_followers(20)
		self.assertEqual(results[13][1],'Dua Lipa')

	def test_album(self):

		results = artist_album()
		self.assertEqual(results[1][1], 'R3HAB')

		results = artist_album(20)
		self.assertEqual(results[13][1],'Ed Sheeran')

	def test_track(self):

		results = track_popularity()
		self.assertEqual(results[0][1], 'Shape of You')

		results = track_popularity(20)
		self.assertEqual(results[13][1],'Higher Love')

	def test_genre(self):

		results = albums_genre()
		self.assertEqual(results[0][0], 'Pop')
		self.assertEqual(results[0][1], 40)

unittest.main()

