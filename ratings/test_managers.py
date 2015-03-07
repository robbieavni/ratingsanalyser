from django.test import TransactionTestCase
from imdb import ImdbPoller, ImdbResponse
from films.models import Film
from ratings.models import Rating

class RatingManagerTestCase(TransactionTestCase):
    fixtures = ['me.json']

    def test_user_aggregate_rating(self):
        """Successfully calculates aggregates for a user's ratings"""
        self.assertEqual(Rating.objects.average_for_user('ur9663707'), 7.0036)

    def test_imdb_aggregate_for_user(self):
        """Successfully calculates aggregate of the IMDB ratings for a user's films"""
        self.assertEqual(Rating.objects.imdb_average_for_users_films('ur9663707'), 7.26966)

    def test_runtime_aggregate_for_user(self):
        self.assertEqual(Rating.objects.average_runtime_for_user('ur9663707'),109.9587)