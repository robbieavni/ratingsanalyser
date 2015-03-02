from django.test import TransactionTestCase
from imdb import ImdbPoller, ImdbResponse
from films.models import Film
from ratings.models import Rating

class RatingManagerTestCase(TransactionTestCase):
    fixtures = ['me.json']

    def test_aggregates(self):
        """Successfully calculates aggregates for a user's ratings"""
        self.assertEqual(Rating.objects.average_for_user('ur9663707'), 7.0036)