from rest_framework import serializers

from management_app.models import Team, Player, Coach


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'coach', 'average_score']


class CoachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coach
        fields = ['experience', 'name']


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['age', 'name', 'height', 'height_unit', 'average_score']
