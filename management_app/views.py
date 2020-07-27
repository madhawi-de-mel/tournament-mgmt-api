from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.views import APIView

from management_app.constants.user_group import UserGroup

from management_app.utils.tournament_detail_util import get_best_players, get_team_of_coach, get_all_teams, \
    get_team, \
    get_players, get_tournament_summary, get_coaches, get_coach_details
from management_app.utils.site_statistics_util import get_site_statistics


class BestPlayersView(APIView):
    """Endpoint to get players in 90th percentile of the team"""

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
    """Endpoint to get team details such as team average score"""

    @staticmethod
    @login_required()
    def get(request, **kwargs):

        team_id = kwargs.get('id')
        try:
            # if request is by an admin, any team details given by team id are returned with average scores
            if Group.objects.get(user=request.user).name == UserGroup.ADMIN.value:
                return HttpResponse(serializers.serialize('json', [get_team(kwargs.get('id'))]),
                                    content_type="application/json", status=200)

            # if request is by a coach for his team, results for his team is returned
            if Group.objects.get(user=request.user).name == UserGroup.COACH.value:
                coach_team_id = get_team_of_coach(request.user.id)
                if team_id == coach_team_id:
                    return HttpResponse(serializers.serialize('json', [get_team(coach_team_id)]),
                                        content_type="application/json", status=200)

            # if request is by a player for his team, results for his team is returned
            if Group.objects.get(user=request.user).name == UserGroup.PLAYER.value:
                if team_id == request.user.player.team_id:
                    data = serializers.serialize('json', [get_team(request.user.player.team_id)])
                    return HttpResponse(data, content_type="application/json", status=200)

        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)

        return HttpResponse('Unauthorized', status=401)


class PlayerView(APIView):
    """Endpoint to get player details"""

    @staticmethod
    @login_required()
    def get(request):

        try:
            # if request is by an admin, all players are returned
            if Group.objects.get(user=request.user).name == UserGroup.ADMIN.value:
                data = serializers.serialize('json', get_players())
                return HttpResponse(data, content_type="application/json", status=200)

            # if request is by a coach, results for his team is returned
            if Group.objects.get(user=request.user).name == UserGroup.COACH.value:
                data = serializers.serialize('json', get_players(get_team_of_coach(request.user.id)))
                return HttpResponse(data, content_type="application/json", status=200)

            # if request is by a player, results for him is returned
            if Group.objects.get(user=request.user).name == UserGroup.PLAYER.value:
                data = serializers.serialize('json', [get_players(request.user.player.team_id, request.user.player.id)])
                return HttpResponse(data, content_type="application/json", status=200)
            return HttpResponse('Unauthorized', status=401)

        except ObjectDoesNotExist:
            return HttpResponseNotFound()


class StatisticsView(APIView):
    """Endpoint to get site usage statistics"""

    @staticmethod
    @permission_required('management_app.view_stats')
    def get(request):
        try:
            # Only users/groups with permission can access site users
            return HttpResponse(get_site_statistics(), content_type="application/json", status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)


class RoundsView(APIView):
    """Endpoint to get tournament progress info: rounds, matches"""

    @staticmethod
    @login_required()
    def get(request):
        try:
            return HttpResponse(get_tournament_summary(), content_type="application/json", status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)


class TeamView(APIView):
    """Endpoint to get all teams with public details"""

    @staticmethod
    @login_required()
    def get(request):
        try:
            return HttpResponse(get_all_teams(), content_type="application/json", status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)


class CoachView(APIView):
    """Endpoint to get all coaches"""

    @staticmethod
    @permission_required('management_app.view_coaches')
    def get(request):
        try:
            return HttpResponse(serializers.serialize('json', get_coaches()), content_type="application/json",
                                status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)


class CoachDetailView(APIView):
    """Endpoint to get specific coach"""

    @staticmethod
    @permission_required('management_app.view_coaches')
    def get(request, **kwargs):
        try:
            return HttpResponse(serializers.serialize('json', [get_coach_details(kwargs.get('id'))]), content_type="application/json",status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)
