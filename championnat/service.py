from datetime import datetime

from django.forms.models import model_to_dict
from django.http import Http404

from .models import Game, League, Player, Team


def leagues():
    return League.objects.all()


# def games_for_all_leagues(limit=5):
#     ret = {}
#     print()
#
#     for league in leagues():
#         league_name = league.name
#         objects = Game.objects.filter(league=league).values('homeTeam__name', 'homeTeam__image', 'awayTeam__name',
#                                                             'awayTeam__image'
#                                                             , 'awayTeamScore', 'homeTeamScore', 'startDate',
#                                                             'endDate')[:limit]
#         ret[league_name] = list(objects)
#     return ret


def games_per_league(league):
    try:
        leagueObj = League.objects.get(name=league)
    except League.DoesNotExist:
        raise Http404
    ret = []
    a = leagueObj.games.select_related('league', 'homeTeam', 'awayTeam').all()
    for game in a:
        tmp = model_to_dict(game)
        tmp['league'] = game.league.name
        del tmp['league']
        homeTeam = model_to_dict(game.homeTeam)
        homeTeam['image'] = game.homeTeam.image.url
        homeTeam['league'] = game.league.name
        tmp['homeTeam'] = homeTeam

        awayTeam = model_to_dict(game.awayTeam)
        awayTeam['image'] = game.awayTeam.image.url
        awayTeam['league'] = game.league.name
        tmp['awayTeam'] = awayTeam
        del tmp['updateTeamPoints']
        ret.append(tmp)
    return ret


def live_games():
    ret = []
    a = Game.objects.filter(
        endDate__gte=datetime.now(),
        startDate__lte=datetime.now()
    ).select_related('league', 'homeTeam', 'awayTeam').all()
    for game in a:
        tmp = model_to_dict(game)
        tmp['league'] = game.league.name
        del tmp['league']
        homeTeam = model_to_dict(game.homeTeam)
        homeTeam['image'] = game.homeTeam.image.url
        homeTeam['league'] = game.league.name
        tmp['homeTeam'] = homeTeam

        awayTeam = model_to_dict(game.awayTeam)
        awayTeam['image'] = game.awayTeam.image.url
        awayTeam['league'] = game.league.name
        tmp['awayTeam'] = awayTeam
        del tmp['updateTeamPoints']
        ret.append(tmp)
    return ret


def teams_per_league(league):
    try:
        leagueObj = League.objects.get(name=league)
    except League.DoesNotExist:
        raise Http404
    a = leagueObj.teams.all()
    ret = []
    for team in a:
        tmp = model_to_dict(team)
        tmp['league'] = league
        tmp['image'] = team.image.url
        ret.append(tmp)
    return ret


def comments_per_game(game):
    try:
        game = Game.objects.get(id=game)
    except Game.DoesNotExist:
        raise Http404
    return game.comments


def games_per_team(team):
    try:
        team = Team.objects.get(id=team)
    except Team.DoesNotExist:
        raise Http404
    return team.homeGames.all(), team.awayGames.all()


def players_per_team(team):
    ret = Player.objects.filter(team__name=team)
    print(ret)
    return ret
