from django.db import models


class RatingManager(models.Manager):
    def total_for_user(self, user):
        return self.filter(user=user).count()

    def average_for_user(self, user):
        return self.filter(user=user).aggregate(models.Avg('rating'))['rating__avg']

    def imdb_average_for_users_films(self, user):
        return self.filter(user=user).aggregate(models.Avg('film__imdb_rating'))['film__imdb_rating__avg']

    def average_runtime_for_user(self, user):
        return self.filter(user=user).aggregate(models.Avg('film__runtime'))['film__runtime__avg']

    def actual_films_rated(self, user):
        return self.filter(user=user, film__type__in=['FF','D','V','TVM']).count()

    def decade_breakdown(self, user):
        decades = range(1880, 2020, 10)
        dictionary = dict((el, [0,0]) for el in decades)
        for decade, count in dictionary.iteritems():
            possible_years = range(decade, decade+10)
            decade_queryset = self.filter(user=user, film__year__in=possible_years)
            dictionary[decade][0] = decade_queryset.count()
            dictionary[decade][1] = decade_queryset.aggregate(models.Avg('rating'))['rating__avg']
        return dictionary

