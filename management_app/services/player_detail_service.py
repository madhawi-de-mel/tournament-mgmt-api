import logging

from management_app.models import Player, PlayerPlayedMatch


class PlayerDetailsService:

    @staticmethod
    def get_all_player_details():
        """Return details of all players such as name, height"""
        players = Player.objects.all()

        print(players[0].name)
        return players

    @staticmethod
    def get_player_details(player_id: int):
        """Return details of the given player such as name, height, average score, number of matches"""
        player = Player.objects.get(pk=player_id)
        score_details = PlayerPlayedMatch.objects.filter(player=player_id)
        score_sum = 0
        # default score and match count set to 0
        player.number_of_matches_played = 0
        player.average_score = 0

        # calculate average score for player
        if score_details is not None:
            player.number_of_matches_played = len(score_details)
            if len(score_details) > 0:
                for match in score_details:
                    score_sum = score_sum + match.personal_score
                player.average_score = score_sum / len(score_details)
        print(player.name)
        return player
