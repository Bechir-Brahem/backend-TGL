from django.urls import path

from .views import liveActivity, \
    leagueActivity, teamsPerDivision, leaguesView, playersView, \
    commentsPerGame, gamesPerTeam, gamePerId, arbitreView, startGame,\
    finishFirstHalf, startSecondHalf, finishGame, addComment

urlpatterns = [
    path('live', liveActivity, name='live'),
    path('league', leagueActivity, name='league'),
    path('teams', teamsPerDivision, name='teamsPerDivision'),
    path('leagues', leaguesView, name='leagues'),
    path('players', playersView, name='players'),
    path('comments', commentsPerGame, name='comments'),
    path('games', gamesPerTeam, name='gamesPerTeam'),
    path('game', gamePerId, name='gamesPerId'),
    path('arbitre/<int:game_id>', arbitreView, name='arbitre'),
    path('arbitre/<int:game_id>/startGame', startGame, name="arbitreStartGame"),
    path('arbitre/<int:game_id>/finishFirstHalf', finishFirstHalf, name="arbitreFinishFirstHalf"),
    path('arbitre/<int:game_id>/startSecondHalf', startSecondHalf, name="arbitreStartSecondHalf"),
    path('arbitre/<int:game_id>/finishGame', finishGame, name="arbitreFinishGame"),
    path('arbitre/<int:game_id>/addComment', addComment, name="arbitreAddComment")
]
