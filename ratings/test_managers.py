from django.test import TransactionTestCase
from ratings.models import Rating
from website.models import ImdbUser

class RatingManagerTestCase(TransactionTestCase):
    fixtures = ['me.json']

    def setUp(self):
        self.user = ImdbUser.objects.get(imdb_id='ur9663707')

    def test_user_aggregate_rating(self):
        self.assertEqual(Rating.objects.average_for_user(self.user), 7.0385)

    def test_imdb_aggregate_for_user(self):
        self.assertEqual(Rating.objects.imdb_average_for_users_films(self.user), 7.63846)

    def test_runtime_aggregate_for_user(self):
        self.assertEqual(Rating.objects.average_runtime_for_user(self.user), 114.0385)

    def test_total_for_user(self):
        self.assertEqual(Rating.objects.total_for_user(self.user), 26)

    def test_actual_films_rated(self):
        self.assertEqual(Rating.objects.actual_films_rated(self.user), 25)

    def test_decade_breakdown(self):
        dictionary = Rating.objects.decade_breakdown(self.user)
        self.assertEqual(len(dictionary),14)
        self.assertEqual(dictionary[1990][0], 3)
        self.assertEqual(dictionary[1990][1], 7.3333)
        self.assertEqual(dictionary[2010][0], 21)
        self.assertEqual(dictionary[2010][1], 7.0)

    def test_hipster_list(self):
        hipster_list = Rating.objects.hipster_films(self.user)
        self.assertEqual(len(hipster_list),6)
        self.assertEqual(hipster_list[0]['votes'], 5005)
        in_order = True
        for i in range(0,3,1):
            if (hipster_list[i]['votes'] > hipster_list[i+1]['votes']):
                in_order = False
        for i in range(3,5,1):
            if (hipster_list[i]['votes'] < hipster_list[i+1]['votes']):
                in_order = False
        self.assertTrue(in_order)

    def test_runtime_list(self):
        runtime_list = Rating.objects.high_low_runtime_list(self.user)
        self.assertEqual(len(runtime_list),6)
        self.assertEqual(runtime_list[0]['runtime'], 60)
        in_order = True
        for i in range(0,3,1):
            if (runtime_list[i]['runtime'] > runtime_list[i+1]['runtime']):
                in_order = False
        for i in range(3,5,1):
            if (runtime_list[i]['runtime'] < runtime_list[i+1]['runtime']):
                in_order = False
        self.assertTrue(in_order)
