# # import unittest
# from django.test import TestCase
#
# from management_app.utils.player_detail_service import PlayerDetailsService
#
#
# class PlayerDetailsTest(TestCase):
#
#     def test_get_all_player_details(self):
#         players = PlayerDetailsService.get_all_player_details()
#         self.assertIsNotNone(players)
#         self.assertEqual(len(players), 2)
#
#     def test_get_player_details(self):
#         player = PlayerDetailsService.get_player_details()
#         self.assertIsNotNone(player)
#         self.assertEqual(player.name, "Andrew John")
#
#
# if __name__ == '__main__':
#     unittest.main()
