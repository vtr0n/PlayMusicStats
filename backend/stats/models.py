from django.db import models
from django.contrib.auth.models import User
from djongo import models as MongoModels
from django.utils import timezone


class PlayMusicStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = MongoModels.DateTimeField(default=timezone.now, blank=True)
    stats = MongoModels.ListField(default=[])
    total_time = models.FloatField(default=0.0)