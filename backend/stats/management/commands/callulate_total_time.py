from django.core.management.base import BaseCommand
from backend.stats.models import PlayMusicStats
from backend.stats.tasks import get_total_time_in_sec


class Command(BaseCommand):
    help = 'Calculate and save total time for all stats'

    def handle(self, *args, **options):
        all_stats = PlayMusicStats.objects.all()
        for stats in all_stats:
            total_time = get_total_time_in_sec(stats.stats)
            print("id: %s, time: %s" % (stats.pk, total_time))
            stats.total_time = total_time
            stats.save()
