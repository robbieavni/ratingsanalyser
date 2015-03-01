from django.test import SimpleTestCase
from imdb import ImdbPoller

class ImdbPollerTestCase(SimpleTestCase):
    def setUp(self):
        self.poller = ImdbPoller('BCYhEodibuPWtshDLs5tNtAHZj_5KgqyLqJaafVk9OZVRH_eWuAGYrQnTb4PN-92iRraBublbOH7rCOCo_QZ9IlvTx9fZCtf3-pq33iDj2RUNwH2LLg6XdD9HRFLv-TItPkv6sD-le1J3hpZlOlDp78UVxuDTdj6guHwwYOB1FR3T8yDch9OnidQVxE-4fvgQf6Y')

    def test_response(self):
        """Able to get a response from IMDB"""
        response = self.poller.requestRatingsResponse('ur9663707')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.headers._store['content-type'][1],'text/csv; charset=utf-8')