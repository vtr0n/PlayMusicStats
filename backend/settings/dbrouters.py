from backend.stats.models import PlayMusicStats


class DBRouter(object):

    def db_for_read(self, model, **hints):
        """ reading PlayMusicStats from mongo """
        if model == PlayMusicStats:
            return 'mongo'
        return None

    def db_for_write(self, model, **hints):
        """ writing PlayMusicStats to mongo """
        if model == PlayMusicStats:
            return 'mongo'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed
        """
        db_list = ('default', 'mongo')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrate for stats app only for mongo
        """
        if app_label == 'stats':
            return db == 'mongo'
        return None
