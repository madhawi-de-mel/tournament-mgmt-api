from django.core.exceptions import MiddlewareNotUsed

from management_app.services.player_detail_service import set_player_average_score, set_team_average


class StartupMiddleware(object):
    def __init__(self, param):
        print("Startup Running")
        set_team_average()
        set_player_average_score()
        print("Startup complete")
        raise MiddlewareNotUsed('Startup complete')
