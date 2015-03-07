from django.db import models
from website.models import ImdbUser


class RatingManager(models.Manager):
    def average_for_user(self, user_id):
        user = ImdbUser.objects.get(imdb_id=user_id)
        return self.filter(user=user).aggregate(models.Avg('rating'))['rating__avg']

    def imdb_average_for_users_films(self, user_id):
        user = ImdbUser.objects.get(imdb_id=user_id)
        return self.filter(user=user).aggregate(models.Avg('film__imdb_rating'))['film__imdb_rating__avg']

    def average_runtime_for_user(self, user_id):
        user = ImdbUser.objects.get(imdb_id=user_id)
        return self.filter(user=user).aggregate(models.Avg('film__runtime'))['film__runtime__avg']
