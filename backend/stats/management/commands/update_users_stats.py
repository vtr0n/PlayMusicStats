from django.core.management.base import BaseCommand
from backend.stats.tasks import update_stats
from backend.users.models import UserSettings


class Command(BaseCommand):
    help = 'Get gm stats and save it to mongo'

    def handle(self, *args, **options):
        users = UserSettings.objects.filter(credential_is_valid=True)
        for user in users:
            update_stats.delay(user.pk)
            print("Stats for user " + str(user.pk) + " send to que")