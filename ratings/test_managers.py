from django.test import TransactionTestCase
from ratings.models import Rating
from website.models import ImdbUser

class RatingManagerTestCase(TransactionTestCase):
    fixtures = ['me.json']

    def setUp(self):
        self.user = ImdbUser.objects.get(imdb_id='ur9663707')

    def test_user_aggregate_rating(self):
        """Successfully calculates aggregates for a user's ratings"""
        self.assertEqual(Rating.objects.average_for_user(self.user), 7.0036)

    def test_imdb_aggregate_for_user(self):
        """Successfully calculates aggregate of the IMDB ratings for a user's films"""
        self.assertEqual(Rating.objects.imdb_average_for_users_films(self.user), 7.26966)

    def test_runtime_aggregate_for_user(self):
        self.assertEqual(Rating.objects.average_runtime_for_user(self.user),109.9587)

    def test_total_for_user(self):
        self.assertEqual(Rating.objects.total_for_user(self.user),557)

    def test_actual_films_rated(self):
        self.assertEqual(Rating.objects.actual_films_rated(self.user),537)

    def test_decade_breakdown(self):
        dictionary = Rating.objects.decade_breakdown(self.user)
        self.assertEqual(len(dictionary),14)
        self.assertEqual(dictionary[1930][0],3)
        self.assertEqual(dictionary[1930][1],6.6667)
        self.assertEqual(dictionary[2000][0],293)
        self.assertEqual(dictionary[2000][1],6.8089)
