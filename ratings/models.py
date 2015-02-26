from django.db import models
from films.models import Film

# Create your models here.

class Rating(models.Model):
    user_id = models.CharField(max_length=12)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    date_rated = models.DateField()
    film = models.ForeignKey(Film)

    def __unicode__(self):
        return "%s rating on \"%s\"" % (self.user_id, self.film.title)