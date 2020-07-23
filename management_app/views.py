
from django.http import HttpResponse

from management_app.services.player_detail_service import get_player_details, get_best_players


def index(request):
    get_player_details(1)
    get_player_details(2)
    get_best_players(1)
    return HttpResponse("Hello, world. You're at the management_app. ")
