from django.urls import path

from .views import homeView, mainActivity, liveActivity, leagueActivity

urlpatterns = [
    path('', homeView, name='home'),
    path('main', mainActivity, name='main'),
    path('live', liveActivity, name='live'),
    path('league', leagueActivity, name='league'),
]
