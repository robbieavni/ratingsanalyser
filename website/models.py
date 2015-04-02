from django.db import models
from ratings.imdb import ImdbResponse, ImdbPoller, addFilmsAndRatingsFromCSV


class ImdbUser(models.Model):
    imdb_id = models.CharField(max_length=18, primary_key=True)


    def __unicode__(self):
        return self.imdb_id

    def process_ratings_from_imdb(self):
        poller = ImdbPoller()
        try:
            response = poller.requestRatingsResponse(self.imdb_id)
        except ConnectionError as e:
            return False
        if response.status_code != 200:
            return False
        imdb_response = ImdbResponse(response)
        imdb_response.addFilmsAndRatingsFromResponse(self)
        return True

    def process_ratings_from_csv(self, reader):
        addFilmsAndRatingsFromCSV(self, reader)