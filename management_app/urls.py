from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'rounds', views.RoundViewSet)
router.register(r'matches', views.MatchViewSet)
router.register(r'teams', views.TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('best-players/', views.BestPlayersView.as_view(), name='best_players'),
    path('team-details/', views.TeamDetailView.as_view(), name='team details'),
    path('players/', views.PlayerView.as_view(), name='players'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
]
