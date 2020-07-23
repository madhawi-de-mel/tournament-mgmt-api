import math

from django.db.models import Q

from management_app.models import Player, Team, Match


def get_all_teams():
    """Return all teams"""
    teams = Team.objects.all()
    return teams


def get_team(team_id: int):
    """Return selected team"""
    team = Team.objects.get(pk=team_id)
    matches = Match.objects.filter(Q(team_one=team_id) | Q(team_two=team_id))
    score_sum = 0
    team.average_score = 0

    # filter teams who played at least one match
    if matches is not None and len(matches) > 0:

        # calculate team average score
        for match in matches:
            if match.team_one_id == team_id:
                score_sum = score_sum + match.team_one_score
            else:
                score_sum = score_sum + match.team_two_score
        team_average = score_sum / len(matches)
        team.average_score = team_average

    return team


def get_player_details(player_id: int):
    """Return details of the given player such as name, height, average score, number of matches"""
    player: Player = Player.objects.get(pk=player_id)
    return set_average_score(player)


def get_best_players(team_id: int):
    """Return the players of the team who has average score in the 90 percentile across the team"""
    team = Team.objects.get(pk=team_id)
    players = team.player_set.all()
    players_with_scores = []
    best_players = []

    for player in players:
        # Players who haven't played a single match are not considered for calculation
        if player.playerplayedmatch_set is not None and len(player.playerplayedmatch_set.all()) > 0:
            players_with_scores.append(set_average_score(player))

    # sort players in ascending order
    players_with_scores.sort(key=lambda p: p.average_score)

    # calculate 90th percentile position (rounding up), 1 is deducted for compatibility with array index
    percentile_position = math.ceil(len(players_with_scores) * 0.1) - 1
    for player_position in range(percentile_position, len(players_with_scores) - 1):
        best_players.append(players_with_scores[player_position])

    # sorting in the reverse order so that player with highest score comes to top
    best_players.sort(key=lambda p: p.average_score, reverse=True)

    return best_players


def set_average_score(player: Player):
    """Calculate average score of the player in the matches he played"""
    score_details = player.playerplayedmatch_set.all()
    score_sum = 0
    # default score and match count set to 0
    player.number_of_matches_played = 0
    player.average_score = 0

    # calculate average score for player
    if score_details is not None:
        player.number_of_matches_played = len(score_details)
        if player.number_of_matches_played > 0:
            for match in score_details:
                score_sum = score_sum + match.personal_score
            player.average_score = score_sum / len(score_details)
    return player
