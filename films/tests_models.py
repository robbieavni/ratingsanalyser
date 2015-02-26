from django.test import TestCase
from films.models import Film

# Create your tests here.

class FilmTestCase(TestCase):
    def setUp(self):
        Film.objects.create(imdb_id="tt0111161", title="The Shawshank Redemption", type="FF", year=1994)
        Film.objects.create(imdb_id="tt0923752", title="The King of Kong", type="D", year=2007)
        Film.objects.create(imdb_id="tt0944947", title="Game of Thrones", type="T")
        self.shawshank = Film.objects.get(imdb_id="tt0111161")
        self.kong = Film.objects.get(imdb_id="tt0923752")
        self.got = Film.objects.get(imdb_id="tt0944947")

    def test_actual_movie_type(self):
        """Movies correctly identified as such and TV shows etc. not"""
        self.assertTrue(self.shawshank.is_actual_film())
        self.assertTrue(self.kong.is_actual_film())
        self.assertFalse(self.got.is_actual_film())

    def test_decade(self):
        """Decades correctly identified"""
        self.assertEqual(self.shawshank.decade(),1990)
        self.assertEqual(self.kong.decade(), 2000)


