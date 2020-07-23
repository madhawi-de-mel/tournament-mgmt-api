from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    year = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    number_of_matches = models.IntegerField(default=0)
    round_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    court_name = models.CharField(max_length=200)
    date = models.DateTimeField('date published', null=True)


class Coach(models.Model):
    name = models.CharField(max_length=200)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PlayedMatch(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_one")
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_two")
    team_one_score = models.IntegerField(default=0)
    team_two_score = models.IntegerField(default=0)

    def won_by(self):
        if self.team_one_score > self.team_two_score:
            return self.team_one
        return self.team_two


class Player(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    height = models.FloatField(default=0)
    height_unit = models.CharField(max_length=200)


class PlayerPlayedMatch(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    personal_score = models.IntegerField(default=0)


