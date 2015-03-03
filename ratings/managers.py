from django.db import models


class RatingManager(models.Manager):
    def average_for_user(self, user_id):
        return self.filter(user_id=user_id).aggregate(models.Avg('rating'))['rating__avg']

    def imdb_average_for_users_films(self, user_id):
        return self.filter(user_id=user_id).aggregate(models.Avg('film__imdb_rating'))['film__imdb_rating__avg']

    def average_runtime_for_user(self, user_id):
        return self.filter(user_id=user_id).aggregate(models.Avg('film__runtime'))['film__runtime__avg']
