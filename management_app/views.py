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
from rest_framework.views import APIView

from management_app.models import Coach, Team, Player
from management_app.serializers import TeamSerializer, CoachSerializer, PlayerSerializer
from management_app.services.match_summary_service import get_rounds, get_matches, get_tournament_summary

from management_app.services.player_detail_service import get_best_players, get_team_of_coach


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
    def get(request):
        try:
            return HttpResponse(serializers.serialize('json', get_rounds()), content_type="application/json",
                                status=200)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)


class MatchView(APIView):
    @staticmethod
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


class LoginView(APIView):

    @staticmethod
    def get(request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return tournament summary
            return HttpResponse("Successful login")
        else:
            return HttpResponse('Permission Denied', status=403)
