from django.db import models
from django.core.urlresolvers import reverse


class ImdbUser(models.Model):
    imdb_id = models.CharField(max_length=12)

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'id': self.imdb_id})

    def __unicode__(self):
        return self.imdb_id
