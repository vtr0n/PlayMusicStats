import json
import os
from unittest import TestCase
import backend.stats.views as stats_view


class ViewTestCase(TestCase):

    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        json_data = open(current_dir + '/static/previos_stats.json')
        self.previous_json = json.load(json_data)

        json_data = open(current_dir + '/static/current_stats.json')
        self.current_json = json.load(json_data)

    def test_get_total_time_in_sec(self):
        self.assertEqual(stats_view.get_total_time_in_sec(self.previous_json), 9042570.0)
        self.assertEqual(stats_view.get_total_time_in_sec(self.current_json), 9048243.0)

    def test_get_time_diff_in_sec(self):
        self.assertEqual(stats_view.get_time_diff_in_sec(self.current_json, self.current_json), 0.0)
        self.assertEqual(stats_view.get_time_diff_in_sec(self.previous_json, self.previous_json), 0.0)
        self.assertEqual(stats_view.get_time_diff_in_sec(self.previous_json, self.current_json), 5673.0)
        self.assertEqual(stats_view.get_time_diff_in_sec(self.current_json, self.previous_json), -5673.0)

    def test_top_tracks_for_all_time(self):
        valid_result_current = [{
            'album_art_ref': 'http://lh3.googleusercontent.com/jgnTiOqdXTs-L4LeYEfkBLA71RD3EwzrZWJcdeOFi7aRdFtIujGGB_5XlcxpHRJbSfNINvBq7Q',
            'artist': 'Daughter', 'title': 'Witches', 'play_count': 178}, {
            'album_art_ref': 'http://lh3.ggpht.com/hnnnfagq0l98Nx0YG5EazotoYh9702gAMZ9yXtw9mh4QnIEQpf99DDv72V4pB8fBu9fOt5_stCo',
            'artist': 'Foo Fighters', 'title': 'Everlong', 'play_count': 167}, {
            'album_art_ref': 'http://lh4.ggpht.com/NhZ_tLt7AUlIZsiM5bxsvmzaTeoNb88YWdQHVl69xyU2M2wFApCD1KJxZ_9Mx07hUBTt-WXQSro',
            'artist': 'Madrugada', 'title': 'Salt (2010 Remastered Version)', 'play_count': 165}, {
            'album_art_ref': 'http://lh3.googleusercontent.com/jgnTiOqdXTs-L4LeYEfkBLA71RD3EwzrZWJcdeOFi7aRdFtIujGGB_5XlcxpHRJbSfNINvBq7Q',
            'artist': 'Daughter', 'title': 'The Right Way Around', 'play_count': 161}, {
            'album_art_ref': 'http://lh4.ggpht.com/NhZ_tLt7AUlIZsiM5bxsvmzaTeoNb88YWdQHVl69xyU2M2wFApCD1KJxZ_9Mx07hUBTt-WXQSro',
            'artist': 'Madrugada', 'title': 'Belladonna (2010 Remastered Version)', 'play_count': 159}]

        valid_result_previous = [{
            'album_art_ref': 'http://lh3.googleusercontent.com/jgnTiOqdXTs-L4LeYEfkBLA71RD3EwzrZWJcdeOFi7aRdFtIujGGB_5XlcxpHRJbSfNINvBq7Q',
            'artist': 'Daughter', 'title': 'Witches', 'play_count': 178}, {
            'album_art_ref': 'http://lh3.ggpht.com/hnnnfagq0l98Nx0YG5EazotoYh9702gAMZ9yXtw9mh4QnIEQpf99DDv72V4pB8fBu9fOt5_stCo',
            'artist': 'Foo Fighters', 'title': 'Everlong', 'play_count': 167}, {
            'album_art_ref': 'http://lh4.ggpht.com/NhZ_tLt7AUlIZsiM5bxsvmzaTeoNb88YWdQHVl69xyU2M2wFApCD1KJxZ_9Mx07hUBTt-WXQSro',
            'artist': 'Madrugada', 'title': 'Salt (2010 Remastered Version)',
            'play_count': 165}, {
            'album_art_ref': 'http://lh3.googleusercontent.com/jgnTiOqdXTs-L4LeYEfkBLA71RD3EwzrZWJcdeOFi7aRdFtIujGGB_5XlcxpHRJbSfNINvBq7Q',
            'artist': 'Daughter', 'title': 'The Right Way Around', 'play_count': 161}, {
            'album_art_ref': 'http://lh4.ggpht.com/NhZ_tLt7AUlIZsiM5bxsvmzaTeoNb88YWdQHVl69xyU2M2wFApCD1KJxZ_9Mx07hUBTt-WXQSro',
            'artist': 'Madrugada', 'title': 'Belladonna (2010 Remastered Version)',
            'play_count': 159}]

        self.assertEqual(stats_view.get_top_tracks_for_all_time(self.current_json), valid_result_current)
        self.assertEqual(stats_view.get_top_tracks_for_all_time(self.previous_json), valid_result_previous)

    def test_get_top_artists_for_all_time(self):
        valid_result_current = [
            {'artist': 'Земфира', 'play_count': 1941,
             'artist_art_ref': 'http://lh3.googleusercontent.com/Qqdi45BhpVMKk7tOEhFZZspYfu9YZto8ZU6PEJkkDC6fIPkbfDgbuMPKR4CKF3EOWGM5S2_c0A'},
            {'artist': 'Madrugada', 'play_count': 1799,
             'artist_art_ref': 'http://lh3.googleusercontent.com/yQhyqtFI_s2fYP8Ag6Q9pr8NyYCePMqQYMM1ZWu3k_jmc20DGfRJyXBNBjgkBXzqds-NKvff'},
            {'artist': 'Daughter', 'play_count': 1761,
             'artist_art_ref': 'http://lh3.googleusercontent.com/u7HQ5YXSE7Y0Dle3G8pJI1ty4CC5Qsvtp6XCG-LVLidwxobSCVf4R1_e3Jlp5hiKpdab1nAx4A'},
            {'artist': 'Foo Fighters', 'play_count': 1733,
             'artist_art_ref': 'http://lh3.googleusercontent.com/mSxoNIcA5cq-oa1ddzErr5e5W-zk2VH47wXuShQAmBA44Edg5UZXeoGQdSBydL_BzRtcjB4Z'},
            {'artist': 'Pink Floyd', 'play_count': 1562,
             'artist_art_ref': 'http://lh3.googleusercontent.com/nJdWW6_WT0G8OSc8vWBOdIAtai_DLuyGm4dqDcaV_LkmuNQd_XCl4AWZYPchzvp9FPQLYhwK'}]

        valid_result_previous = [
            {'artist': 'Земфира', 'play_count': 1936,
             'artist_art_ref': 'http://lh3.googleusercontent.com/Qqdi45BhpVMKk7tOEhFZZspYfu9YZto8ZU6PEJkkDC6fIPkbfDgbuMPKR4CKF3EOWGM5S2_c0A'},
            {'artist': 'Madrugada', 'play_count': 1798,
             'artist_art_ref': 'http://lh3.googleusercontent.com/yQhyqtFI_s2fYP8Ag6Q9pr8NyYCePMqQYMM1ZWu3k_jmc20DGfRJyXBNBjgkBXzqds-NKvff'},
            {'artist': 'Daughter', 'play_count': 1761,
             'artist_art_ref': 'http://lh3.googleusercontent.com/u7HQ5YXSE7Y0Dle3G8pJI1ty4CC5Qsvtp6XCG-LVLidwxobSCVf4R1_e3Jlp5hiKpdab1nAx4A'},
            {'artist': 'Foo Fighters', 'play_count': 1732,
             'artist_art_ref': 'http://lh3.googleusercontent.com/mSxoNIcA5cq-oa1ddzErr5e5W-zk2VH47wXuShQAmBA44Edg5UZXeoGQdSBydL_BzRtcjB4Z'},
            {'artist': 'Pink Floyd', 'play_count': 1562,
             'artist_art_ref': 'http://lh3.googleusercontent.com/nJdWW6_WT0G8OSc8vWBOdIAtai_DLuyGm4dqDcaV_LkmuNQd_XCl4AWZYPchzvp9FPQLYhwK'}]

        self.assertEqual(stats_view.get_top_artists_for_all_time(self.current_json), valid_result_current)
        self.assertEqual(stats_view.get_top_artists_for_all_time(self.previous_json), valid_result_previous)

    def test_get_top_artists_by_month(self):
        valid_result = [
            {'artist': 'Земфира', 'play_count': 5,
             'artist_art_ref': 'http://lh3.googleusercontent.com/Qqdi45BhpVMKk7tOEhFZZspYfu9YZto8ZU6PEJkkDC6fIPkbfDgbuMPKR4CKF3EOWGM5S2_c0A'},
            {'artist': 'Борис Гребенщиков', 'play_count': 4,
             'artist_art_ref': 'http://lh3.googleusercontent.com/DMHa6WmlXGNC8KLjtUK8t5Rdcg0qgXYwrlzjOjswhpaqPFuOpf6w1NivnR7VdyJcX9O3e61o'},
            {'artist': 'Radiohead', 'play_count': 2,
             'artist_art_ref': 'http://lh3.googleusercontent.com/53cYhGcuBl6tJh4NAsrkxHW2dYReUv27bwrA1nb_KNCrgIKeGjhfl-NmUzsu6mJGoyg1UBuvpDM'},
            {'artist': 'Nirvana', 'play_count': 2,
             'artist_art_ref': 'http://lh3.googleusercontent.com/6rZYI7T2BlQvPP3vM2kAsPa-usqhHzaN5pexOJ5DJLSf5OEKs7FN0qbl5bSF7ROozvieX-tAcwI'},
            {'artist': 'The Flaming Lips', 'play_count': 1,
             'artist_art_ref': 'http://lh3.googleusercontent.com/HbfA4TR_zQbF4RJnwDLadKRbiUPqyWhUhKecd-ZJwDipeyeksVntI1PnH6rAkZCL6Tyrh8bK'}]

        self.assertEqual(stats_view.get_diff_top_artists(self.previous_json, self.current_json), valid_result)

    def test_get_diff_top_tracks(self):
        valid_result = [{
            'album_art_ref': 'http://lh3.googleusercontent.com/qGvujhCXQ4xweLa-tAyVbF9aqQ47nJvBSmdHTMbo7QBqlepN0Jhf9OM4MyoSESiZ0TtiDqUw8Q',
            'artist': 'Земфира', 'title': 'во мне (Live)', 'play_count': 2}, {
            'album_art_ref': 'http://lh3.googleusercontent.com/qGvujhCXQ4xweLa-tAyVbF9aqQ47nJvBSmdHTMbo7QBqlepN0Jhf9OM4MyoSESiZ0TtiDqUw8Q',
            'artist': 'Земфира', 'title': 'брызги (Live)', 'play_count': 1}, {
            'album_art_ref': 'http://lh6.ggpht.com/fht0eFPoqngBEOozoqv_QXxLa67ywVwE9_KHuVkzqhZIU04Jz_SLwEK7fowq8G-CVTHpk3nCXA',
            'artist': 'Борис Гребенщиков', 'title': 'Бурлак', 'play_count': 1}, {
            'album_art_ref': 'http://lh3.googleusercontent.com/ez_Oa6zSuoUVKRoM9MnQwsKQUjNCMioH4qgmLSRMpmkf2pN3AXOtR2vpwwMQSy6LKBmcf_4s',
            'artist': '5’Nizza', 'title': 'Весна (правильная версия)', 'play_count': 1}, {
            'album_art_ref': 'http://lh4.ggpht.com/o285k5kh2wjTWZ8HDltOdKE2GTLQ0J4Yko5UrokN-RNZWoE7pRsObMN4EKDwEJC1Keq_kKaZiA',
            'artist': 'Борис Гребенщиков', 'title': 'Ветка', 'play_count': 1}]

        self.assertEqual(stats_view.get_diff_top_tracks(self.previous_json, self.current_json), valid_result)

    def test_get_graph(self):
        # TODO write this test
        pass
