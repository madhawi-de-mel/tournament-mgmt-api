import json
import logging

from django.core.exceptions import MiddlewareNotUsed
from django.test import TestCase

from management_app.middleware.startup_middleware import StartupMiddleware
from management_app.utils.site_statistics_util import get_site_statistics
from management_app.utils.tournament_detail_util import get_best_players, \
    get_tournament_summary, get_players_of_team, get_all_players, get_player, get_all_teams, get_team, get_coaches, \
    get_coach_details, get_team_of_coach


class PlayerDetailsTest(TestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        try:
            StartupMiddleware(param='')
        except MiddlewareNotUsed as e:
            self.logger.info(e)

    def test_get_best_player_ninetieth(self):
        """test nineties percentile"""
        best_players = get_best_players(1, 90)
        self.assertIsNotNone(best_players)
        self.assertEquals(len(best_players), 1)
        self.assertEquals(best_players[0].name, 'Andrew John')
        assert True

    def test_get_best_player_tenth(self):
        """test tenth percentile"""
        best_players = get_best_players(1, 10)
        self.assertIsNotNone(best_players)
        self.assertEquals(len(best_players), 3)
        # check if sort is working
        self.assertTrue(best_players[0].average_score >= best_players[1].average_score)
        self.assertTrue(best_players[1].average_score >= best_players[2].average_score)
        assert True

    def test_get_team(self):
        team = get_team(1)
        self.assertIsNotNone(team)
        self.assertEqual(team.name, 'Golden Eagles')

    def test_get_all_teams(self):
        teams = get_all_teams()
        self.assertIsNotNone(teams)
        teams_obj = json.loads(teams)
        self.assertIsNotNone(teams_obj)
        self.assertEquals(len(teams_obj), 2)

    def test_get_players_of_team(self):
        players = get_players_of_team(1)
        self.assertIsNotNone(players)
        self.assertEqual(len(players), 5)

    def test_get_all_player_details(self):
        players = get_all_players()
        self.assertIsNotNone(players)
        self.assertEqual(len(players), 6)

    def test_get_player_details(self):
        player = get_player(1)
        self.assertIsNotNone(player)
        self.assertEqual(player.name, 'Riane James')

    def test_get_tournament_summary(self):
        tournament = get_tournament_summary()
        self.assertIsNotNone(tournament)
        tournament_obj = json.loads(tournament)
        self.assertIsNotNone(tournament_obj)
        self.assertEquals(tournament_obj.get('name'), 'Basketball Tournament')
        self.assertEquals(len(tournament_obj.get('rounds')), 4)
        self.assertEquals(len(tournament_obj.get('rounds')[0].get('matches')), 2)

    def test_get_coaches(self):
        coaches = get_coaches()
        self.assertIsNotNone(coaches)
        self.assertEquals(len(coaches), 2)

    def test_get_coach_details(self):
        coach = get_coach_details(1)
        self.assertIsNotNone(coach)
        self.assertEquals(coach.name, 'John Doily')

    def test_get_team_of_coach(self):
        team_id = get_team_of_coach(4)
        self.assertIsNotNone(team_id)
        self.assertEquals(team_id, 1)

    def test_get_site_statistics(self):
        stats = get_site_statistics()
        self.assertIsNotNone(stats)
        stats_obj = json.loads(stats)
        self.assertIsNotNone(stats_obj)
        self.assertEquals(len(json.loads(stats)), 4)
