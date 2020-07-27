from django.core.serializers.json import Serializer
from rest_framework import serializers

from management_app.models import Team, Round, Match, UserProfile


class RoundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Round
        fields = ['name', 'number_of_matches', 'round_number', 'matches']


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = ['round', 'court_name', 'team_one', 'team_two', 'team_one_score', 'team_two_score', 'won_by']


class StatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['login_count', 'time_spent', 'login_status']


class UserSerializer(Serializer):
    @staticmethod
    def get_dump_object(profile, **kwargs):
        mapped_user = {
            'user_name': profile.user.username,
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'user_id': profile.user.pk,
            'login_count': profile.login_count,
            'time_spent': profile.time_spent,
            'login_status': profile.login_status,
        }
        return mapped_user


class TournamentDetailsSerializer(Serializer):
    @staticmethod
    def get_dump_object(tournament, **kwargs):
        round_array = []
        for round_instance in tournament.rounds.all():
            match_array = []
            for match in round_instance.matches.all():
                mapped_match = {
                    'court_name': match.court_name,
                    'team_one': {
                        'team_id': match.team_one.pk,
                        'team_name': match.team_one.name
                    },
                    'team_two': {
                        'team_id': match.team_two.pk,
                        'team_name': match.team_two.name
                    },
                    'team_one_score': match.team_one_score,
                    'team_two_score': match.team_two_score,
                    'won_by': {
                        'team_id': match.won_by.pk,
                        'team_name': match.won_by.name
                    },
                    'match_id': match.pk
                }
                match_array.append(mapped_match)
            mapped_round = {
                'matches': match_array,
                'name': round_instance.name,
                'number_of_matches': round_instance.number_of_matches,
                'round_number': round_instance.round_number,
                'round_id': round_instance.pk
            }
            round_array.append(mapped_round)
        data = {
            'name': tournament.name,
            'year': tournament.year,
            'country': tournament.country,
            'rounds': round_array,
            'won_by': {
                'team_id': tournament.won_by.pk,
                'team_name': tournament.won_by.name
            }
        }
        return data


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    @staticmethod
    def get_dump_object(team, **kwargs):
        mapped_team = {
            'name': team.name,
            'team_id': team.pk,
            'coach': {
                'coach_id': team.coach.pk,
                'coach_name': team.coach.name
            }
        }
        return mapped_team
