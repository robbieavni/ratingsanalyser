from django.db import models
from films.models import Film
from managers import RatingManager


class Rating(models.Model):
    user_id = models.CharField(max_length=12)
    rating = models.SmallIntegerField(blank=True, null=True)
    date_rated = models.DateField()
    film = models.ForeignKey(Film)
    objects = RatingManager()

    def __unicode__(self):
        return "%s rating on \"%s\"" % (self.user_id, self.film.title)

    class Meta:
        unique_together = ('user_id', 'film')