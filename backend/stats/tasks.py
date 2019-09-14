import pickle, codecs
from celery import shared_task
from backend.stats.models import PlayMusicStats
from backend.users.models import UserSettings
from gmusicapi import Mobileclient


# Добавить подсчет веремени
# Сократить
@shared_task
def update_stats(user_id):
    gm = Mobileclient()
    user = UserSettings.objects.get(pk=user_id)
    try:
        user_credential_base64 = user.credential
        user_credential = codecs.decode(user_credential_base64.encode(), "base64")
        credential = pickle.loads(user_credential)

        # TODO think about google apis problem
        gm.oauth_login(user.current_device, credential)

        try:
            library = gm.get_all_songs()
            gm.logout()
        except Exception as e:
            print("Exception: " + str(e))
            return

        new_library = prepare_library(library)

        new_stats = PlayMusicStats()
        new_stats.user = user.user
        new_stats.stats = new_library
        new_stats.total_time = get_total_time_in_sec(new_library)
        new_stats.save()

        print('Stats for ' + str(user.user) + ' saved')
    except Exception as e:
        user.credential_is_valid = False
        user.save()
        print('Credential for ' + str(user.user) + ' is invalid: ' + str(e))


def get_total_time_in_sec(last_user_stats):
    """Calculates the total time you listen to music"""
    total_time_sec = 0
    for song in last_user_stats:
        try:
            total_time_sec += int(song['play_count']) * (int(song['duration_millis']) / 1000)
        except:
            continue
    return total_time_sec


def prepare_library(library):
    """Change library structure"""
    new_library = []
    for songs in library:
        new_song = dict()
        new_song['title'] = songs['title']
        new_song['artist'] = songs['artist']
        new_song['id'] = songs['id']
        new_song['artist'] = songs['artist']
        new_song['duration_millis'] = songs['durationMillis']
        try:
            new_song['play_count'] = songs['playCount']
        except:
            new_song['play_count'] = 0
        try:
            new_song['artist_id'] = songs['artistId'][0]
        except:
            new_song['artist_id'] = ''
        try:
            new_song['artist_art_ref'] = songs['artistArtRef'][0]['url']
        except:
            new_song['artist_art_ref'] = ''
        try:
            new_song['album_art_ref'] = songs['albumArtRef'][0]['url']
        except:
            new_song['album_art_ref'] = ''

        new_library.append(new_song)
    return new_library
