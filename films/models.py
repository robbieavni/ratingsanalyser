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
    imdb_id = models.CharField(max_length=12)
    title = models.TextField()
    type = models.CharField(max_length=3, choices=FILM_TYPE_CHOICES)
    year = models.PositiveSmallIntegerField()
    runtime = models.PositiveSmallIntegerField()
    released = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    number_of_votes = models.PositiveIntegerField()


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


