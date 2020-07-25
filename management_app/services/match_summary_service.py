from django.core import serializers

from management_app.models import Round, Match
from management_app.reponse_models.match_summary import TournamentRound, TournamentSummary


def get_rounds():
    return Round.objects.all()


def get_matches():
    return Match.objects.all()


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


def set_won_by():
    matches = Match.objects.all()
    for match in matches:
        if match.team_one_score > match.team_two_score:
            match.won_by = match.team_one
        else:
            match.won_by = match.team_two
        match.save()
