import json

from django.db.models import F
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .helper import get_now
from .models import GameComment
from .service import *


def process_game(game):
    tmp = model_to_dict(game)
    tmp['league'] = game.league.name
    tmp['startDate'] = tmp['firstHalfStartDate']
    homeTeam = model_to_dict(game.homeTeam)
    homeTeam['image'] = game.homeTeam.image.url
    homeTeam['league'] = game.league.name
    tmp['homeTeam'] = homeTeam

    awayTeam = model_to_dict(game.awayTeam)
    awayTeam['image'] = game.awayTeam.image.url
    awayTeam['league'] = game.league.name
    tmp['awayTeam'] = awayTeam
    del tmp['updateTeamPoints']
    return tmp


def leaguesView(request):
    return JsonResponse(list(leagues().values()), safe=False)


def leagueActivity(request):
    league = request.GET.get('league')
    games = games_per_league(league)
    ret = []
    for game in games:
        ret.append(process_game(game))
    return JsonResponse(ret, safe=False)


def liveActivity(request):
    games = live_games()
    ret = []
    for game in games:
        ret.append(process_game(game))
    return JsonResponse(ret, safe=False)


def teamsPerDivision(request):
    league = request.GET.get('league')
    return JsonResponse(list(teams_per_league(league).values()), safe=False)


def playersView(request):
    team = request.GET.get('team')
    league = request.GET.get('league')
    if team:
        print(team)
        try:
            return JsonResponse(list(players_per_team(team).values()), safe=False)
        except Team.DoesNotExist:
            raise Http404('team n\'existe pas')
    elif league:
        try:
            players = players_per_league(league)
            ret = []
            for player in players:
                tmp = model_to_dict(player)
                del tmp['team_id']
                tmp['team_name=']=player.team.name
                tmp['team_image']=player.team.image.url
                ret.append(tmp)
            return JsonResponse(ret)
        except League.DoesNotExist:
            raise Http404('league n\'existe pas')
    raise Http404()


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
        homeGames.append(process_game(game))
    for game in ret[1]:
        awayGames.append(process_game(game))

    return JsonResponse({
        'homeGames': homeGames,
        'awayGames': awayGames
    }, safe=True)


def gamePerId(request):
    game = request.GET.get('game')
    game = game_per_id(game)
    return JsonResponse(process_game(game), safe=False)


def startGame(request, game_id):
    game = Game.objects.get(id=game_id)

    if not game.live and not game.finished and not game.firstHalfFinished and not game.secondHalfStarted:
        print('game is now live')
        game.firstHalfStartDate = get_now()
        game.live = True
        game.save()
    return HttpResponse()


def finishFirstHalf(request, game_id):
    game = Game.objects.get(id=game_id)
    if game.live and not game.finished and not game.firstHalfFinished and not game.secondHalfStarted:
        game.firstHalfFinished = True
        game.firstHalfEndDate = get_now()
        game.save()
    return HttpResponse()


def startSecondHalf(request, game_id):
    game = Game.objects.get(id=game_id)
    if game.live and not game.finished and game.firstHalfFinished and not game.secondHalfStarted:
        game.secondHalfStarted = True
        game.secondHalfStartDate = get_now()
        game.save()
    return HttpResponse()


def finishGame(request, game_id):
    game = Game.objects.get(id=game_id)
    if game.live and not game.finished and game.firstHalfFinished and game.secondHalfStarted:
        game.secondHalfEndDate = get_now()
        game.finished = True
        game.live = False
        game.save()
    return HttpResponse()


def addComment(request, game_id):
    game = Game.objects.get(id=game_id)
    firstHalf = game.live and not game.finished and not game.firstHalfFinished and not game.secondHalfStarted
    secondHalf = game.live and not game.finished and game.firstHalfFinished and game.secondHalfStarted
    if firstHalf or secondHalf:
        data = json.loads(request.body)
        print(data)
        comment = GameComment(type=data['type'], time=game.counter(),
                              player_id=data['player'], game_id=game_id
                              )
        comment.save()
        team_id = comment.player.team_id
        if comment.type == 'but':
            if team_id == game.homeTeam_id:
                game.homeTeamScore += 1
            elif team_id == game.awayTeam_id:
                game.awayTeamScore += 1
            game.save()
    return HttpResponse()


def arbitreView(request, game_id):
    print('in view')
    print(game_id)
    game = Game.objects.get(id=game_id)
    homeTeamPlayers = Team.objects.get(id=game.homeTeam.id).players.all()
    awayTeamPlayers = Team.objects.get(id=game.awayTeam.id).players.all()
    comments = game.comments.all()

    context = {
        "game": game,
        "comments": comments,
        "players": homeTeamPlayers.union(awayTeamPlayers),
        "url": request.build_absolute_uri('/'),
        "choices": GameComment.choices,
        "counter": int(game.counter())
    }
    return render(request, 'championnat/arbitre.html', context)

# Create your views here.
