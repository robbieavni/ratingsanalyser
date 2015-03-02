from django.db import models


class RatingManager(models.Manager):
    def average_for_user(self, user_id):
        return self.all().aggregate(models.Avg('rating'))['rating__avg']
