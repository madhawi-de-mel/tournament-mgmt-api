from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('rounds/', views.RoundsView.as_view(), name='rounds'),
    path('best-players/', views.BestPlayersView.as_view(), name='best_players'),
    path('teams/', views.TeamView.as_view(), name='teams'),
    path('teams/<int:id>/', views.TeamDetailView.as_view(), name='team_details'),
    path('players/', views.PlayerView.as_view(), name='players'),
    path('coaches/', views.CoachView.as_view(), name='coaches'),
    path('coaches/<int:id>/', views.CoachDetailView.as_view(), name='coach_details'),

]
