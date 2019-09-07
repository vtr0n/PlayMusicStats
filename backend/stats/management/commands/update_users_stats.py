import pickle, codecs
from django.core.management.base import BaseCommand
from backend.stats.models import PlayMusicStats
from backend.users.models import UserSettings
from gmusicapi import Mobileclient


class Command(BaseCommand):
    help = 'Get gm stats and save it to mongo'

    def handle(self, *args, **options):
        gm = Mobileclient()
        users = UserSettings.objects.all()

        for user in users:
            if user.credential_is_valid is False:
                continue

            try:
                user_credential_base64 = user.credential
                user_credential = codecs.decode(user_credential_base64.encode(), "base64")
                credential = pickle.loads(user_credential)

                # TODO think about google apis problem
                gm.oauth_login(user.current_device, credential)
                library = gm.get_all_songs()
                gm.logout()

                new_stats = PlayMusicStats()
                new_stats.user = user.user
                new_stats.stats = library
                new_stats.save()

                self.stdout.write(self.style.SUCCESS('Stats for ' + str(user.user) + ' saved'))
            except Exception as e:
                user.credential_is_valid = False
                user.save()
                self.stdout.write(self.style.ERROR('Credential for ' + str(user.user) + ' is invalid: ' + str(e)))