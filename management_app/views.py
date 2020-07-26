import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from management_app.models import Coach, Team, Player, Round, Match
from management_app.reponse_models.UserGroup import UserGroup
from management_app.serializers import TeamSerializer, RoundSerializer, PlayerSerializer, MatchSerializer
from management_app.services.match_summary_service import get_rounds, get_matches, get_tournament_summary

from management_app.services.player_detail_service import get_best_players, get_team_of_coach, get_all_teams, get_team, \
    get_players


# class RoundViewSet(viewsets.ModelViewSet):
#     """
#        API endpoint that allows rounds to be viewed only, only authenticated users can access
#        """
#     permission_classes = [IsAuthenticated]
#     queryset = Round.objects.all()
#     serializer_class = RoundSerializer
#     http_method_names = ['get']


# class MatchViewSet(viewsets.ModelViewSet):
#     """
#        API endpoint that allows matches to be viewed only, only authenticated users can access
#        """
#     permission_classes = [IsAuthenticated]
#     queryset = Match.objects.all()
#     serializer_class = MatchSerializer
#     http_method_names = ['get']


# class TeamViewSet(viewsets.ModelViewSet):
#     """
#        API endpoint that allows all teams to be viewed.
#        """
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer
#     http_method_names = ['get']


# class PlayerViewSet(viewsets.ModelViewSet):
#     """
#        API endpoint that allows all players to be viewed.
#        """
#     queryset = Player.objects.all()
#     serializer_class = PlayerSerializer
#     http_method_names = ['get']


class BestPlayersView(APIView):
    @staticmethod
    @login_required
    def get(request):
        try:
            # if request is by an admin, team id must be sent
            if Group.objects.get(user=request.user).name == 'admin':
                if len(request.query_params) == 0 or request.query_params['team-id'] is None:
                    return HttpResponseBadRequest("team-id not specified")
                team_id = request.query_params['team-id']
                data = serializers.serialize('json', get_best_players(team_id))
                return HttpResponse(data, content_type="application/json", status=200)

            # if request is by a coach, results for his team is returned
            if Group.objects.get(user=request.user).name == 'coach':
                data = serializers.serialize('json', get_best_players(get_team_of_coach(request.user.pk)))
                return HttpResponse(data, content_type="application/json", status=200)

            # for players this method is not accessible
            return HttpResponse('Unauthorized', status=401)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)
        except MultiValueDictKeyError:
            return HttpResponseBadRequest("team-id not specified")


class RoundView(APIView):
    @staticmethod
    @login_required
    def get(request):
        try:
            return HttpResponse(serializers.serialize('json', get_rounds()), content_type="application/json",
                                status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)


class MatchView(APIView):
    @staticmethod
    @login_required
    def get(request):
        try:
            return HttpResponse(serializers.serialize('json', get_matches()), content_type="application/json",
                                status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)


class SummaryView(APIView):
    @staticmethod
    def get(request):
        try:

            return JsonResponse(json.dumps(model_to_dict(get_tournament_summary(1))), content_type="application/json",
                                status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)


class TeamView(APIView):

    @staticmethod
    @login_required()
    def get(request):
        # if request is by an admin, all teams are returned
        if Group.objects.get(user=request.user).name == UserGroup.ADMIN.value[0]:
            data = serializers.serialize('json', get_all_teams())
            return HttpResponse(data, content_type="application/json", status=200)

        # if request is by a coach, results for his team is returned
        if Group.objects.get(user=request.user).name == UserGroup.COACH.value[0]:
            data = serializers.serialize('json', get_team(get_team_of_coach(request.user.id)))
            return HttpResponse(data, content_type="application/json", status=200)

        # if request is by a player, results for his team is returned
        if Group.objects.get(user=request.user).name == UserGroup.PLAYER.value[0]:
            data = serializers.serialize('json', [get_team(request.user.player.team_id)])
            return HttpResponse(data, content_type="application/json", status=200)
        return HttpResponse('Unauthorized', status=401)


class PlayerView(APIView):

    @staticmethod
    @login_required()
    def get(request):
        # if request is by an admin, all players are returned
        if Group.objects.get(user=request.user).name == UserGroup.ADMIN.value[0]:
            data = serializers.serialize('json', get_players())
            return HttpResponse(data, content_type="application/json", status=200)

        # if request is by a coach, results for his team is returned
        if Group.objects.get(user=request.user).name == UserGroup.COACH.value[0]:
            data = serializers.serialize('json', get_players(get_team_of_coach(request.user.id)))
            return HttpResponse(data, content_type="application/json", status=200)

        # if request is by a player, results for his team is returned
        if Group.objects.get(user=request.user).name == UserGroup.PLAYER.value[0]:
            data = serializers.serialize('json', [get_players(request.user.player.team_id, request.user.player.id)])
            return HttpResponse(data, content_type="application/json", status=200)
        return HttpResponse('Unauthorized', status=401)
