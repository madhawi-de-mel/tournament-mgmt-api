import logging

from django.http import HttpResponse

from management_app.services.player_detail_service import PlayerDetailsService


def index(request):
    PlayerDetailsService.get_player_details(1)
    PlayerDetailsService.get_player_details(2)
    return HttpResponse("Hello, world. You're at the management_app. ")
