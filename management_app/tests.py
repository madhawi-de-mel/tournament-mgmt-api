from django.test import TestCase

from management_app.services.tournament_detail_service import get_best_players, set_team_average, set_player_average_score


class PlayerDetailsTest(TestCase):
    fixtures = ['tournament.json']

    def setUp(self):
        set_team_average()
        set_player_average_score()

    #     def test_get_all_player_details(self):
    #         players = get_all_player_details()
    #         self.assertIsNotNone(players)
    #         self.assertEqual(len(players), 2)
    #
    #     def test_get_player_details(self):
    #         player = PlayerDetailsService.get_player_details()
    #         self.assertIsNotNone(player)
    #         self.assertEqual(player.name, "Andrew John")
    #
    #
    #
    # if __name__ == '__main__':
    #     unittest.main()

    def test_get_best_player_ninetieth(self):
        best_players = get_best_players(1, 90)
        self.assertIsNotNone(best_players)
        self.assertEquals(len(best_players), 1)
        self.assertEquals(best_players[0].name, 'Riane James')
        assert True

    def test_get_best_player_tenth(self):
        best_players = get_best_players(1, 10)
        self.assertIsNotNone(best_players)
        self.assertEquals(len(best_players), 3)
        # check if sort is working
        self.assertTrue(best_players[0].average_score >= best_players[1].average_score)
        self.assertTrue(best_players[1].average_score >= best_players[2].average_score)
        assert True

    def test_get_best_player_invalid_team(self):
        best_players = get_best_players(78, 90)
        self.assertIsNotNone(best_players)
        self.assertEquals(len(best_players), 0)
        assert True

    # def test_resolution_for_best_players(self):
    #     resolver = resolve('/management_app/best-players')
    #     self.assertEqual(resolver.func.cls, BestPlayersView)

    # def test_get_tournament_summary(self):
    #     summery = get_tournament_summary()
    #     self.assertIsNotNone(summery)
