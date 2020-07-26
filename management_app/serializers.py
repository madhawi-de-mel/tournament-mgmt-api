from rest_framework import serializers

from management_app.models import Team, Player, Coach, Round, Match


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


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['age', 'name', 'height', 'height_unit', 'average_score']
