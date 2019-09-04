import codecs
import pickle
from backend.users.models import UserSettings
from backend.users.serializers import UserSettingsSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404, JsonResponse
from gmusicapi import Mobileclient
from oauth2client.client import OAuth2WebServerFlow


# Create your views here.
class UserSettingsView(APIView):
    def get_object(self, user):
        try:
            return UserSettings.objects.get(user=user)
        except:
            raise Http404

    def get(self, request):
        user_settings = self.get_object(request.user)

        serializer = UserSettingsSerializer(user_settings)
        return Response(serializer.data)

    def put(self, request):

        user_settings = self.get_object(request.user)
        serializer = UserSettingsSerializer(user_settings, data=request.data)

        if serializer.is_valid():
            code = serializer.validated_data['code']
            try:
                flow = OAuth2WebServerFlow(**Mobileclient._session_class.oauth._asdict())
                credential = flow.step2_exchange(code)
                credential_picked = codecs.encode(pickle.dumps(credential), "base64").decode()

                gm = Mobileclient()
                current_device = gm.get_device_ids(credential)[0]
            except:
                # TODO change response and connect it to frontend
                return Response({'google play troubles'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user_settings.credential = credential_picked
            user_settings.current_device = current_device
            user_settings.credential_is_valid = True
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_auth_url(request):
    flow = OAuth2WebServerFlow(**Mobileclient._session_class.oauth._asdict())
    try:
        auth_uri = flow.step1_get_authorize_url()
    except:
        auth_uri = '/'
    return JsonResponse({'url': auth_uri})
