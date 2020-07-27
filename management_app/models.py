from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    year = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="rounds")
    name = models.CharField(max_length=200)
    number_of_matches = models.PositiveIntegerField(default=0)
    round_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Coach(models.Model):
    name = models.CharField(max_length=200)
    experience = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200)
    average_score = models.FloatField(default=0)
    coach = models.OneToOneField(Coach, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='matches')
    court_name = models.CharField(max_length=200)
    date = models.DateTimeField('date published', null=True)
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_one')
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_two')
    team_one_score = models.PositiveIntegerField(default=0)
    team_two_score = models.PositiveIntegerField(default=0)
    won_by = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='won_by', null=True)


class Player(models.Model):
    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField(default=0)
    height = models.FloatField(default=0)
    height_unit = models.CharField(max_length=200)
    average_score = models.FloatField(default=0)
    number_of_matches_played = models.PositiveIntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class PlayerPlayedMatch(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    personal_score = models.PositiveIntegerField(default=0)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    login_count = models.PositiveIntegerField(default=0)
    time_spent = models.FloatField(default=0)  # in minutes
    login_status = models.BooleanField(default=False)

    def login_user(sender, request, user, **kwargs):
        user.userprofile.login_count = user.userprofile.login_count + 1
        user.userprofile.login_status = True
        user.userprofile.save()

    def logout_user(sender, request, user, **kwargs):
        user.userprofile.login_status = False
        # time difference between logout time and last login is added to time spent in minutes
        user.userprofile.time_spent = (timezone.now() - user.last_login).seconds / 60
        user.userprofile.save()

    user_logged_in.connect(login_user)
    user_logged_out.connect(logout_user)
