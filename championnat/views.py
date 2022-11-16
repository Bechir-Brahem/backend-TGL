from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render

from .service import *


def homeView(request):
    return render(request, 'home.html', {'title': 'a'})


# def mainActivity(request):
#     return JsonResponse(games_for_all_leagues())

def leaguesView(request):
    return JsonResponse(list(leagues().values()), safe=False)


def leagueActivity(request):
    league = request.GET.get('league')
    return JsonResponse(games_per_league(league), safe=False)


def liveActivity(request):
    return JsonResponse(live_games(), safe=False)


def teamsPerDivision(request):
    league = request.GET.get('league')
    return JsonResponse(teams_per_league(league), safe=False)


def playerPerTeam(request):
    team = request.GET.get('team')
    print(team)
    return JsonResponse(list(players_per_team(team).values()), safe=False)


def commentsPerGame(request):
    game = request.GET.get('game')
    return JsonResponse(list(comments_per_game(game).values('time', 'type', playerName=F('player__fullname'))),
                        safe=False)


def gamesPerTeam(request):
    team = request.GET.get('team')
    ret = games_per_team(team)
    homeGames = []
    awayGames = []
    for game in ret[0]:
        tmp = model_to_dict(game)
        tmp['league'] = game.league.name
        tmp['homeTeam'] = model_to_dict(game.homeTeam)
        tmp['homeTeam']['image'] = game.homeTeam.image.url
        tmp['awayTeam'] = model_to_dict(game.awayTeam)
        tmp['awayTeam']['image'] = game.awayTeam.image.url
        homeGames.append(tmp)
    for game in ret[1]:
        tmp = model_to_dict(game)
        tmp['league'] = game.league.name
        tmp['homeTeam'] = model_to_dict(game.homeTeam)
        tmp['awayTeam'] = model_to_dict(game.awayTeam)
        tmp['homeTeam']['image'] = game.homeTeam.image.url
        tmp['awayTeam']['image'] = game.awayTeam.image.url
        awayGames.append(tmp)

    return JsonResponse({
        'homeGames': homeGames,
        'awayGames': awayGames
    }, safe=True)


def gamePerId(request):
    game = request.GET.get('game')
    game = game_per_id(game)
    tmp = model_to_dict(game)
    tmp['league'] = game.league.name
    tmp['homeTeam'] = model_to_dict(game.homeTeam)
    tmp['homeTeam']['image'] = game.homeTeam.image.url
    tmp['awayTeam'] = model_to_dict(game.awayTeam)
    tmp['awayTeam']['image'] = game.awayTeam.image.url

    return JsonResponse(tmp, safe=False)

# Create your views here.
