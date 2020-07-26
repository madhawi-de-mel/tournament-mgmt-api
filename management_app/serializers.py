from django.core.serializers.json import Serializer
from rest_framework import serializers

from management_app.models import Team, Round, Match, UserProfile


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['name']


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


class IsActiveListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        # data = data.filter(is_active=1)
        return super().to_representation(data)


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
    def get_dump_object(rounds, **kwargs):
        round_array = []
        for round_instance in rounds:
            match_array = []
            for match in round_instance.matches.all():
                mapped_match = {
                    'court_name': match.court_name,
                    'team_one': match.team_one.name,
                    'team_two': match.team_two.name,
                    'team_one_score': match.team_one_score,
                    'team_two_score': match.team_two_score,
                    'won_by': match.won_by.name,
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
            'rounds': round_array
        }
        return data
