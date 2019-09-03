from django.db import models
from django.contrib.auth.models import User
from djongo import models as MongoModels
from datetime import datetime


class PlayMusicStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = MongoModels.DateTimeField(default=datetime.now, blank=True)
    stats = MongoModels.ListField(default=[])
