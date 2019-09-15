from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from backend.stats.models import PlayMusicStats


class Command(BaseCommand):
    help = 'Delete old stats'

    def handle(self, *args, **options):
        PlayMusicStats.objects.filter(date__lt=(datetime.now() - timedelta(days=30)).date()).delete()
