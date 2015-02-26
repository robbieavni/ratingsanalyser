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

    def __unicode__(self):
        return self.title

    def is_actual_film(self):
        actual_film_types = {'FF','D','V','TVM'}
        if self.type in actual_film_types:
            return True
        else:
            return False

class Additional(models.Model):
    year = models.PositiveSmallIntegerField()
    runtime = models.PositiveSmallIntegerField()
    released = models.DateField()
    film = models.OneToOneField(Film, primary_key=True)

    def __unicode__(self):
        return "Additional Info for \"%s\"" % self.film.title

class OverallRating(models.Model):
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    number_of_votes = models.PositiveIntegerField()
    film = models.OneToOneField(Film, primary_key=True)

    def __unicode__(self):
        return "Rating for \"%s\"" % self.film.title

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


