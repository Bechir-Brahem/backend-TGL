from django.http import JsonResponse
from django.shortcuts import render

from .service import *


def homeView(request):
    return render(request, 'home.html', {'title': 'a'})


def mainActivity(request):
    return JsonResponse(games_for_all_leagues())


def leagueActivity(request):
    league = request.GET.get('league')
    return JsonResponse(games_per_league(league), safe=False)


def liveActivity(request):
    return JsonResponse(live_games(), safe=False)

def teamsPerDivision(request):
    league=request.GET.get('league')
    return JsonResponse(teams_per_league(league),safe=False)


# Create your views here.
