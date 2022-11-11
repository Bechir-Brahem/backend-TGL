from datetime import datetime

from django.core import serializers
from django.http import Http404

from .models import Game, Team,League


def leagues():
    return League.objects.all()


def games_for_all_leagues(limit=5):
    ret = {}
    print()

    for league in leagues():
        league_name = league.name
        objects = Game.objects.filter(league=league).values('homeTeam__name', 'homeTeam__image', 'awayTeam__name',
                                                            'awayTeam__image'
                                                            , 'awayTeamScore', 'homeTeamScore', 'startTime',
                                                            'endTime')[:limit]
        ret[league_name] = list(objects)
    return ret


def games_per_league(league):
    try:
        leagueObj=League.objects.get(name=league)
    except League.DoesNotExist:
        raise Http404
    ret = []
    a=leagueObj.games.select_related('league','homeTeam','awayTeam').all()
    for game in a:
        tmp=model_to_dict(game)
        tmp['league']=game.league.name
        homeTeam = model_to_dict(game.homeTeam)
        homeTeam['image']=game.homeTeam.image.url
        homeTeam['league']=game.league.name
        tmp['homeTeam']=homeTeam
        del tmp['homeTeam']['id']

        awayTeam = model_to_dict(game.awayTeam)
        awayTeam['image']=game.awayTeam.image.url
        awayTeam['league']=game.league.name
        tmp['awayTeam']=awayTeam
        del tmp['awayTeam']['id']
        del tmp['updateTeamPoints']
        ret.append(tmp)
    return ret

from django.forms.models import model_to_dict
def live_games():
    ret = []
    a= Game.objects.filter(
        endTime__gte=datetime.now(),
        startTime__lte=datetime.now()
    ).select_related('league','homeTeam','awayTeam').all()
    for game in a:
        tmp = model_to_dict(game)
        del tmp['id']
        tmp['league'] = game.league.name
        homeTeam = model_to_dict(game.homeTeam)
        homeTeam['image'] = game.homeTeam.image.url
        homeTeam['league'] = game.league.name
        tmp['homeTeam'] = homeTeam
        del tmp['homeTeam']['id']

        awayTeam = model_to_dict(game.awayTeam)
        awayTeam['image'] = game.awayTeam.image.url
        awayTeam['league'] = game.league.name
        tmp['awayTeam'] = awayTeam
        del tmp['awayTeam']['id']
        del tmp['updateTeamPoints']
        ret.append(tmp)
    return ret


def teams_per_league(league):
    try:
        leagueObj=League.objects.get(name=league)
    except League.DoesNotExist:
        raise Http404
    a= leagueObj.objects.select_related('league').all()
    ret =[]
    for team in a:
        tmp=model_to_dict(team)
        tmp['league']=league
        del tmp['league_id']
        ret.append(tmp)
    return ret
    # a=Game.objects.filter(league=league).values_list('homeTeam',flat=True)
    # b=Game.objects.filter(league=league).values_list('awayTeam',flat=True)
    # teams_pk=a.union(b).distinct()
    # teams=Team.objects.filter(pk__in=teams_pk)
    # team
    #
    # from django.forms.models import model_to_dict
    # ret = []
    # for team in teams:
    #     tmp=model_to_dict(team)
    #     tmp['image']=team.image.url
    #     ret.append(tmp)
    # print(ret)
    #
    # return ret
