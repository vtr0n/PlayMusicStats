from rest_framework.decorators import api_view
from django.http import JsonResponse
from backend.stats.models import PlayMusicStats
from datetime import datetime, timedelta
from collections import OrderedDict
import time


@api_view(['GET'])
def get_stats(request):
    user_id = request.user

    start_time = time.time()
    time_now = datetime.now()
    last_user_stats = PlayMusicStats.objects.filter(user_id=user_id).latest('id')

    # TODO refactor queries
    # day before stats
    stats = PlayMusicStats.objects.filter(user_id=user_id,
                                          date__range=[time_now.date(), time_now]).order_by(
        'id')
    day_before_stats = stats[0]
    # week before stats
    week_stats_range = PlayMusicStats.objects.filter(user_id=user_id,
                                                     date__range=[(time_now - timedelta(days=7)).date(),
                                                                  time_now]).order_by(
        'id')
    week_before_stats = week_stats_range[0]
    # month before stats
    stats = PlayMusicStats.objects.filter(user_id=user_id,
                                          date__range=[(time_now - timedelta(days=30)).date(), time_now]).order_by(
        'id')
    month_before_stats = stats[0]

    obj = {
        'all_duration_sec': get_total_time_in_sec(last_user_stats),
        'duration_by_day_sec': get_time_diff_in_sec(day_before_stats, last_user_stats),
        'duration_by_day_week': get_time_diff_in_sec(week_before_stats, last_user_stats),
        'duration_by_day_month': get_time_diff_in_sec(month_before_stats, last_user_stats),
        'top_tracks': get_top_tracks_for_all_time(last_user_stats.stats),
        'top_artists': get_top_artists_for_all_time(last_user_stats.stats),
        'top_artists_by_mouth': get_diff_top_artists(month_before_stats.stats, last_user_stats.stats),
        'top_tracks_by_mouth': get_diff_top_tracks(month_before_stats.stats, last_user_stats.stats),

        'chart': get_graph(week_stats_range, 7),
    }

    return JsonResponse(obj)


def get_total_time_in_sec(last_user_stats):
    """Calculates the total time you listen to music"""
    return last_user_stats.total_time


def get_time_diff_in_sec(first_stats, last_stats):
    """Return difference in music play time between stats"""
    return get_total_time_in_sec(last_stats) - get_total_time_in_sec(first_stats)


def get_top_tracks_for_all_time(last_user_stats):
    top_track_list = []
    last_user_stats.sort(key=lambda x: x['play_count'], reverse=True)
    for i in range(5):
        try:
            top_track_list.append({
                'album_art_ref': last_user_stats[i]['album_art_ref'],
                'artist': last_user_stats[i]['artist'],
                'title': last_user_stats[i]['title'],
                'play_count': last_user_stats[i]['play_count'],
            })
        except:
            pass
    return top_track_list


def get_top_artists_for_all_time(last_user_stats):
    top_artist_dict = {}
    for song in last_user_stats:
        try:
            top_artist_dict[str(song['artist'])]['play_count'] += int(song['play_count'])
        except:
            top_artist_dict[str(song['artist'])] = {
                'artist': song['artist'],
                'play_count': int(song['play_count']),
                'artist_art_ref': song['artist_art_ref']
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


def get_diff_top_artists(first_stats, last_stats):
    top_artists = {}
    for song in first_stats:
        try:
            top_artists[str(song['artist'])] += int(song['play_count'])
        except:
            top_artists[str(song['artist'])] = int(song['play_count'])

    top_artists2 = {}
    for song in last_stats:
        try:
            top_artists2[str(song['artist'])]['play_count'] += int(song['play_count'])
        except:
            top_artists2[str(song['artist'])] = {
                'artist': song['artist'],
                'play_count': int(song['play_count']),
                'artist_art_ref': song['artist_art_ref']
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


def get_diff_top_tracks(first_stats, last_stats):
    dict = {}
    for song in first_stats:
        dict[song['id']] = song['play_count']

    list = []
    for song in last_stats:
        try:
            diff = song['play_count'] - dict[song['id']]
        except:
            diff = song['play_count']
        if diff > 0:
            list.append({
                'album_art_ref': song['album_art_ref'],
                'artist': song['artist'],
                'title': song['title'],
                'play_count': diff,
            })
    list.sort(key=lambda x: x['play_count'], reverse=True)

    top_songs = []
    for i in range(5):
        try:
            top_songs.append(list[i])
        except:
            pass
    return top_songs


def get_graph(week_stats, days_delta):
    time_now = datetime.now()

    date_dict = OrderedDict()
    for i in range(days_delta, -1, -1):
        date_dict[(time_now - timedelta(days=i)).date()] = 0

    stats_dict = OrderedDict()
    for i in range(len(week_stats)):
        try:
            if stats_dict[week_stats[i].date.date()]['min'] is not None:
                stats_dict[week_stats[i].date.date()]['max'] = week_stats[i].total_time
        except:
            stats_dict[week_stats[i].date.date()] = {}
            stats_dict[week_stats[i].date.date()]['min'] = week_stats[i].total_time

    while stats_dict:
        key, value = stats_dict.popitem()
        try:
            date_dict[key] = value['max'] - value['min']
        except:
            date_dict[key] = 0

    final_list = []
    while date_dict:
        key, value = date_dict.popitem()
        final_list.append({
            'date': key,
            'minutes': value / 60,
            'hours': value / (60 * 60),
        })
    final_list.reverse()
    return {
        'columns': ['date', 'minutes', 'hours'],
        'rows': final_list
    }
