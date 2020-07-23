from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from management_app.models import Coach, Team, Player
from management_app.serializers import TeamSerializer, CoachSerializer, PlayerSerializer


# def index(request):
#     a = get_player_details(1)
#     b = get_player_details(2)
#     c = get_best_players(1)
#     d = get_best_players(2)
#     e = get_team(1)
#     f = get_team(3)
#     return HttpResponse("Hello, world. You're at the management_app. ")


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
    # def list(self, request, *args, **kwargs):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    # return HttpResponse(get_all_teams())

    # @action(detail=True, methods=['get'])
    # def get_team(self, request):
    #     team = get_team(request)
    #     serializer_class = TeamSerializer
    #     return serializer_class.data


class PlayerViewSet(viewsets.ModelViewSet):
    """
       API endpoint that allows users to be viewed or edited.
       """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
