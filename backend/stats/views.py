from rest_framework.decorators import api_view
from django.http import JsonResponse
from backend.stats.models import PlayMusicStats
from datetime import datetime, timedelta
from collections import OrderedDict


@api_view(['GET'])
def get_stats(request):
    user_id = request.user
    obj = {
        'all_duration_sec': all_duration(user_id),
        'duration_by_day_sec': get_time_range_in_sec(user_id, 1),
        'duration_by_day_week': get_time_range_in_sec(user_id, 7),
        'duration_by_day_month': get_time_range_in_sec(user_id, 30),
        'top_artists': top_artists(user_id),
        'top_artists_by_mouth': get_top_artists(user_id, 30),
        'top_tracks': top_tracks(user_id),
        'top_tracks_by_mouth': get_top_tracks(user_id, 30),
        'chart': get_graph(user_id, 7),
    }

    return JsonResponse(obj)


def top_tracks(user_id):
    last_user_stats = PlayMusicStats.objects.filter(user_id=user_id).latest('id').stats
    top_track_list = []
    last_user_stats.sort(key=lambda x: x['playCount'], reverse=True)
    for i in range(5):
        try:
            try:
                album_art_ref = last_user_stats[i]['albumArtRef'][0]['url']
            except:
                album_art_ref = ''
            top_track_list.append({
                'album_art_ref': album_art_ref,
                'artist': last_user_stats[i]['artist'],
                'title': last_user_stats[i]['title'],
                'play_count': last_user_stats[i]['playCount'],
            })
        except:
            pass
    return top_track_list


def top_artists(user_id):
    last_user_stats = PlayMusicStats.objects.filter(user_id=user_id).latest('id').stats
    top_artist_dict = {}
    for song in last_user_stats:
        try:
            top_artist_dict[str(song['artist'])]['play_count'] += int(song['playCount'])
        except:
            try:
                artist_art_ref = song['artistArtRef'][0]['url']
            except:
                artist_art_ref = ''
            top_artist_dict[str(song['artist'])] = {
                'artist': song['artist'],
                'play_count': int(song['playCount']),
                'artist_art_ref': artist_art_ref
            }
    top_artists_list = []
    while top_artist_dict:
        key, value = top_artist_dict.popitem()
        top_artists_list.append(value)

    top_artists_list.sort(key=lambda x: x['play_count'], reverse=True)

    top_artist_dict = []
    for i in range(5):
        try:
            top_artist_dict.append(top_artists_list[i])
        except:
            pass

    return top_artist_dict


def all_duration(user_id):
    last_user_stats = PlayMusicStats.objects.filter(user_id=user_id).latest('id').stats

    all_count_time = 0
    for song in last_user_stats:
        all_count_time += int(song['playCount']) * (int(song['durationMillis']) / 1000)

    return all_count_time


def get_time_range_in_sec(user_id, day_delta):
    now = datetime.now()
    minus_day = now - timedelta(days=day_delta)

    day_range = PlayMusicStats.objects.filter(user_id=user_id, date__range=[minus_day.date(), now]).order_by('id')

    def get_time_play(day):
        all_count_time = 0
        for song in day:
            all_count_time += int(song['playCount']) * (int(song['durationMillis']) / 1000)

        return all_count_time

    if len(day_range) > 0:
        first = day_range[0]
        last = day_range[len(day_range) - 1]
        return get_time_play(last.stats) - get_time_play(first.stats)

    return 0


def get_top_tracks(user_id, day_delta):
    now = datetime.now()
    minus_day = now - timedelta(days=day_delta)

    day_range = PlayMusicStats.objects.filter(user_id=user_id, date__range=[minus_day.date(), now]).order_by('id')

    first = day_range[0]
    last = day_range[len(day_range) - 1]

    dict = {}
    for song in first.stats:
        dict[song['id']] = song['playCount']

    list = []
    for song in last.stats:
        try:
            diff = song['playCount'] - dict[song['id']]
        except:
            diff = song['playCount']
        try:
            album_art_ref = song['albumArtRef'][0]['url']
        except:
            album_art_ref = ''
        if diff > 0:
            list.append({
                'album_art_ref': album_art_ref,
                'artist': song['artist'],
                'title': song['title'],
                'play_count': diff,
            })
    list.sort(key=lambda x: x['play_count'], reverse=True)

    top_songs = []
    # TODO refactor all this views

    for i in range(5):
        try:
            top_songs.append(list[i])
        except:
            pass
    return top_songs


def get_top_artists(user_id, day_delta):
    now = datetime.now()
    minus_day = now - timedelta(days=day_delta)

    day_range = PlayMusicStats.objects.filter(user_id=user_id, date__range=[minus_day.date(), now]).order_by('id')

    first = day_range[0]
    last = day_range[len(day_range) - 1]

    top_artists = {}
    for song in first.stats:
        try:
            top_artists[str(song['artist'])] += int(song['playCount'])
        except:
            top_artists[str(song['artist'])] = int(song['playCount'])

    top_artists2 = {}
    for song in last.stats:
        try:
            top_artists2[str(song['artist'])]['play_count'] += int(song['playCount'])
        except:
            try:
                artist_art_ref = song['artistArtRef'][0]['url']
            except:
                artist_art_ref = ''

            top_artists2[str(song['artist'])] = {
                'artist': song['artist'],
                'play_count': int(song['playCount']),
                'artist_art_ref': artist_art_ref
            }

    top_artists_list = []
    while top_artists2:
        key, value = top_artists2.popitem()
        try:
            play_count = value['play_count'] - top_artists[key]
        except:
            play_count = value['play_count']

        value['play_count'] = play_count
        if play_count > 0:
            top_artists_list.append(value)

    top_artists_list.sort(key=lambda x: x['play_count'], reverse=True)

    top_artists = []
    for i in range(5):
        try:
            top_artists.append(top_artists_list[i])
        except:
            pass
    return top_artists


def get_graph(user_id, day_delta):
    now = datetime.now()
    minus_day = now - timedelta(days=day_delta)

    day_range = PlayMusicStats.objects.filter(user_id=user_id, date__range=[minus_day.date(), now]).order_by(
        'id').order_by('id')

    dict = OrderedDict()
    for i in range(day_delta, -1, -1):
        dict[(now - timedelta(days=i)).date()] = float('inf')

    for song in day_range:
        music_time = 0
        for songs in song.stats:
            music_time += int(songs['playCount']) * (int(songs['durationMillis']) / 1000)

        dict[song.date.date()] = music_time

    minimum = min(dict.items(), key=lambda x: x[1])[1]

    list = []
    while dict:
        key, value = dict.popitem()
        if value == float('inf'):
            value = minimum
        list.append([key, value])

    for i in range(len(list)):
        if list[i][1] == 0:
            list[i][1] = minimum

    list.reverse()
    final_list = []
    for i in range(len(list) - 1):
        final_list.append({
            'date': (list[i + 1][0]),
            'minutes': (list[i + 1][1] - list[i][1]) / 60,
            'hours': (list[i + 1][1] - list[i][1]) / (60 * 60),
        })

    return {
        'columns': ['date', 'minutes', 'hours'],
        'rows': final_list
    }
