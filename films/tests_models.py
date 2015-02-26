from django.test import TestCase
from films.models import Film

# Create your tests here.

class FilmTestCase(TestCase):
    def setUp(self):
        Film.objects.create(imdb_id="tt0111161", title="The Shawshank Redemption", type="FF")
        Film.objects.create(imdb_id="tt0923752", title="The King of Kong", type="D")
        Film.objects.create(imdb_id="tt0944947", title="Game of Thrones", type="T")

    def test_actual_movie_type(self):
        """Movies correctly identified as such and TV shows etc. not"""
        shawshank = Film.objects.get(imdb_id="tt0111161")
        kong = Film.objects.get(imdb_id="tt0923752")
        got = Film.objects.get(imdb_id="tt0944947")
        self.assertTrue(shawshank.is_actual_film())
        self.assertTrue(kong.is_actual_film())
        self.assertFalse(got.is_actual_film())
