from django.db import models

class Film(models.Model):
    FILM_TYPE_CHOICES = (
        ('FF', 'Feature Film'),
        ('D', 'Documentary'),
        ('S', 'TV Series'),
        ('V', 'Video'),
        ('SF', 'Short Film'),
        ('MS', 'Mini-Series'),
        ('TVM', 'TV Movie'),
        ('TVE', 'TV Episode'),
        ('TVS', 'TV Special'),
        ('VG', 'Video Game'),
    )
    imdb_id = models.CharField(max_length=12, primary_key=True)
    title = models.TextField()
    type = models.CharField(max_length=3, choices=FILM_TYPE_CHOICES)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    runtime = models.PositiveSmallIntegerField(blank=True, null=True)
    released = models.DateField(blank=True, null=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    number_of_votes = models.PositiveIntegerField(blank=True, null=True)


    def __unicode__(self):
        return self.title

    def is_actual_film(self):
        actual_film_types = {'FF','D','V','TVM'}
        if self.type in actual_film_types:
            return True
        else:
            return False

    def decade(self):
        return self.year / 10 * 10

class Director(models.Model):
    name = models.TextField()
    films = models.ManyToManyField(Film)

    def __unicode__(self):
        return self.name

class Genre(models.Model):
    genre = models.CharField(max_length=128)
    films = models.ManyToManyField(Film)

    def __unicode__(self):
        return self.genre


