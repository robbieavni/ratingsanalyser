from django.test import TestCase
from imdb import ImdbPoller, ImdbResponse
from films.models import Film

class ImdbPollerTestCase(TestCase):
    def setUp(self):
        self.poller = ImdbPoller('BCYhEodibuPWtshDLs5tNtAHZj_5KgqyLqJaafVk9OZVRH_eWuAGYrQnTb4PN-92iRraBublbOH7rCOCo_QZ9IlvTx9fZCtf3-pq33iDj2RUNwH2LLg6XdD9HRFLv-TItPkv6sD-le1J3hpZlOlDp78UVxuDTdj6guHwwYOB1FR3T8yDch9OnidQVxE-4fvgQf6Y')
        self.user_id = 'ur9663707'
        self.response = self.poller.requestRatingsResponse(self.user_id)

    def test_response(self):
        """Able to get a CSV response from IMDB"""
        self.assertEqual(self.response.status_code,200)
        self.assertEqual(self.response.headers._store['content-type'][1],'text/csv; charset=utf-8')

    def test_parse_csv_adding_films_and_ratings(self):
        """Successfully adds films and ratings to database"""
        self.imdb_response = ImdbResponse(self.response)
        self.imdb_response.addFilmsAndRatingsFromCSV(self.user_id)
        films = Film.objects.all()
        self.assertGreater(len(films),100)
        cabin = Film.objects.get(imdb_id='tt1259521')
        self.assertEqual(cabin.title, 'The Cabin in the Woods')
        self.assertEqual(cabin.runtime, 95)
        self.assertEqual(cabin.year, 2012)
