from django.db import models


class ImdbUser(models.Model):
    imdb_id = models.CharField(max_length=12)
