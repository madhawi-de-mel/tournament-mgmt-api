from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework.views import APIView

from management_app.models import Coach, Team, Player
from management_app.serializers import TeamSerializer, CoachSerializer, PlayerSerializer

from management_app.services.player_detail_service import get_best_players


class CoachViewSet(viewsets.ModelViewSet):
    """
       API endpoint that allows users to be viewed or edited.
       """
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """
       API endpoint that allows users to be viewed or edited.
       """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """
       API endpoint that allows users to be viewed or edited.
       """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class BestPlayersView(APIView):
    def get(self, request):
        try:
            if len(request.query_params) == 0 or request.query_params['team-id'] is None:
                return HttpResponseBadRequest("bank id not specified")
            team_id = request.query_params['team-id']
            data = serializers.serialize('json', get_best_players(team_id))
            return HttpResponse(data, content_type="application/json", status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)
        except MultiValueDictKeyError:
            return HttpResponseBadRequest("bank id not specified")
