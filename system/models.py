from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField('date published')
    city = models.DateTimeField('date started')


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    number_of_matches = models.IntegerField(default=0)
    round_number = models.IntegerField(default=0)