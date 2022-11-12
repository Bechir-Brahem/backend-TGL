from django.urls import path

from .views import homeView,  liveActivity, leagueActivity,teamsPerDivision,leaguesView

urlpatterns = [
    path('', homeView, name='home'),
    # path('main', mainActivity, name='main'),
    path('live', liveActivity, name='live'),
    path('league', leagueActivity, name='league'),
    path('teams', teamsPerDivision, name='teamsPerDivision'),
    path('leagues', leaguesView, name='leagues')
]
