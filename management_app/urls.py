from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register(r'rounds', views.RoundViewSet)
# router.register(r'matches', views.MatchViewSet)
# router.register(r'players', views.PlayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('best-players/', views.BestPlayersView.as_view(), name='best_players'),
    path('rounds/', views.RoundView.as_view(), name='rounds'),
    path('matches/', views.MatchView.as_view(), name='matches'),
    path('summary/', views.SummaryView.as_view(), name='summary'),
    path('teams/', views.TeamView.as_view(), name='teams'),
    path('players/', views.PlayerView.as_view(), name='players'),
]
