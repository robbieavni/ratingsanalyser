from django.db import models
from ratings.imdb import ImdbResponse, ImdbPoller


class ImdbUser(models.Model):
    imdb_id = models.CharField(max_length=12, primary_key=True)


    def __unicode__(self):
        return self.imdb_id

    def process_ratings(self):
        poller = ImdbPoller()
        try:
            response = poller.requestRatingsResponse(self.imdb_id)
        except ConnectionError as e:
            return False
        if response.status_code != 200:
            return False
        imdb_response = ImdbResponse(response)
        imdb_response.addFilmsAndRatingsFromCSV(self)
        return True