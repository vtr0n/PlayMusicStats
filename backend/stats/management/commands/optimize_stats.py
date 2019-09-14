from django.core.management.base import BaseCommand
from backend.stats.models import PlayMusicStats
from backend.stats.tasks import prepare_library


class Command(BaseCommand):
    help = 'Reorganize stats structure'

    def handle(self, *args, **options):
        all_stats = PlayMusicStats.objects.all()
        for library in all_stats:
            library.stats = prepare_library(library.stats)
            library.save()
            print('Done for ' + str(library.pk))