from django.urls import path

from .views import homeView, liveActivity, \
    leagueActivity, teamsPerDivision, leaguesView, playerPerTeam, commentsPerGame, gamesPerTeam

urlpatterns = [
    path('', homeView, name='home'),
    # path('main', mainActivity, name='main'),
    path('live', liveActivity, name='live'),
    path('league', leagueActivity, name='league'),
    path('teams', teamsPerDivision, name='teamsPerDivision'),
    path('leagues', leaguesView, name='leagues'),
    path('players',playerPerTeam,name='players'),
    path('comments',commentsPerGame,name='comments'),
    path('games', gamesPerTeam, name='gamesPerTeam')
]
