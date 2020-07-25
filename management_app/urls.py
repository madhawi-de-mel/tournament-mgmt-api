from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'coaches', views.CoachViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'players', views.PlayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('best-players/', views.BestPlayersView.as_view(), name='best_players'),
    path('rounds/', views.RoundView.as_view(), name='rounds'),
    path('matches/', views.MatchView.as_view(), name='matches'),
    path('summary/', views.SummaryView.as_view(), name='summary'),
    path('login/', views.LoginView.as_view(), name='login'),
]
