import math

from django.core import serializers
from django.db.models import Q

from management_app.models import Player, Team, Match, Coach, Round
from management_app.reponse_models.match_summary import TournamentRound, TournamentSummary


def get_all_teams():
    """Return all teams"""
    return Team.objects.all()


def get_team(team_id: int):
    """Return selected team with average score"""
    return Team.objects.get(pk=team_id)


def get_players(team_id: int = -1, player_id: int = -1):
    """Return players"""
    if player_id > -1:
        return Player.objects.get(pk=player_id)
    if team_id > -1:
        return Player.objects.filter(team_id=team_id)

    return Player.objects.all()


def get_player_details(player_id: int):
    """Return details of the given player such as name, height, average score, number of matches"""
    return Player.objects.get(pk=player_id)


def get_best_players(team_id: int, percentile: int = 90):
    """Return the players of the team who has average score in the 90 percentile across the team"""
    team = Team.objects.get(pk=team_id)
    players = team.player_set.all()
    players_with_scores = []
    best_players = []

    for player in players:
        # Players who haven't played a single match are not considered for calculation
        if player.playerplayedmatch_set is not None and len(player.playerplayedmatch_set.all()) > 0:
            players_with_scores.append(player)

    # sort players in ascending order
    players_with_scores.sort(key=lambda p: p.average_score)

    if len(players_with_scores) > 0:
        # calculate 90th percentile position (rounding up), 1 is deducted for compatibility with array index
        percentile_position = math.ceil(len(players_with_scores) * percentile / 100) - 1
        for player_position in range(percentile_position, len(players_with_scores)):
            best_players.append(players_with_scores[player_position])

        # sorting in the reverse order so that player with highest score comes to top
        best_players.sort(key=lambda p: p.average_score, reverse=True)

    return best_players


def set_team_average():
    """Calculate team average score and save to DB"""
    teams = Team.objects.all()

    for team in teams:
        matches = Match.objects.filter(Q(team_one=team.pk) | Q(team_two=team.pk))

        # team average is calculated if it's 0 and then saved, otherwise return the existing value
        # filter teams who played at least one match
        if team is not None and team.average_score == 0 and matches is not None and len(matches) > 0:
            score_sum = 0
            # calculate team average score
            for match in matches:
                if match.team_one_id == team.pk:
                    score_sum = score_sum + match.team_one_score
                else:
                    score_sum = score_sum + match.team_two_score
            team_average = score_sum / len(matches)
            team.average_score = team_average
            team.save()


def set_player_average_score():
    """Calculate average score of all players in the matches he played, and save in DB"""

    players = Player.objects.all()

    for player in players:
        score_details = player.playerplayedmatch_set.all()
        score_sum = 0
        # default score and match count set to 0
        player.number_of_matches_played = 0
        player.average_score = 0

        # calculate average score, played match count for player
        if score_details is not None:
            player.number_of_matches_played = len(score_details)
            if player.number_of_matches_played > 0:
                for match in score_details:
                    score_sum = score_sum + match.personal_score
                player.average_score = score_sum / len(score_details)
            player.save()


def get_team_of_coach(coach_user_id):
    """Returns the team-id of the team, coach in charge of"""
    coach = Coach.objects.get(user=coach_user_id)
    return coach.team.pk


def set_won_by():
    matches = Match.objects.all()
    for match in matches:
        if match.team_one_score > match.team_two_score:
            match.won_by = match.team_one
        else:
            match.won_by = match.team_two
        match.save()


def get_tournament_summary(tournament_id):
    rounds = Round.objects.filter(tournament=tournament_id)
    tournament_rounds = []
    for round_instance in rounds:
        tournament_round = TournamentRound(serializers.serialize('json', round_instance.match_set.all()))
        # for match in round_instance.match_set.all():
        #     pass
        #     tournament_round.matches.append[tournament_match]
        #     tournament_match = match
        tournament_rounds.append(tournament_round)

    return TournamentSummary(tournament_rounds)
