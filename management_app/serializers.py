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
    def get_dump_object(self, obj):
        user_list = []
        mapped_object = {
            'user_name': obj.user_name,
            'first_name': obj.first_name,
            'last_name': obj.last_name
        }
        return user_list
