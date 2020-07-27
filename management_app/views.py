from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from management_app.models import Team, Round, Match
from management_app.constants.user_group import UserGroup
from management_app.serializers import TeamSerializer, RoundSerializer, TournamentDetailsSerializer

from management_app.utils.tournament_detail_util import get_best_players, get_team_of_coach, get_all_teams, \
    get_team, \
    get_players, get_tournament_summary
from management_app.utils.site_statistics_util import get_site_statistics


class RoundViewSet(viewsets.ModelViewSet):
    """
       API endpoint that allows rounds to be viewed only, only authenticated users can access"""
    permission_classes = [IsAuthenticated]
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    http_method_names = ['get']


class MatchViewSet(viewsets.ModelViewSet):
    """
       API endpoint that allows matches to be viewed only, only authenticated users can access"""
    permission_classes = [IsAuthenticated]
    queryset = Match.objects.all()
    serializer_class = TournamentDetailsSerializer
    http_method_names = ['get']


class TeamViewSet(viewsets.ModelViewSet):
    """
       API endpoint that allows all teams to be view only, only authenticated users can access"""
    permission_classes = [IsAuthenticated]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    http_method_names = ['get']


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


class TeamDetailView(APIView):

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


class StatisticsView(APIView):
    @staticmethod
    @permission_required('management_app.view_stats')
    def get(request):
        try:
            # Only users/groups with permission can access site users
            return HttpResponse(get_site_statistics(), content_type="application/json", status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)


class RoundsView(APIView):
    @staticmethod
    @login_required()
    def get(request):
        try:
            return HttpResponse(get_tournament_summary(), content_type="application/json", status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)
