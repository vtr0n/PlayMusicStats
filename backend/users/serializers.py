from rest_framework import serializers
from backend.users.models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['code', 'credential_is_valid']
        read_only_fields = ['credential_is_valid']

# TODO add mobile app choose
