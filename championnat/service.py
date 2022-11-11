from datetime import datetime

from django.core import serializers

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
                                                            , 'awayTeamScore', 'homeTeamScore', 'start_time',
                                                            'end_time')[:limit]
        ret[league_name] = list(objects)
    return ret


def games_per_league(league):
    try:
        leagueObj=League.objects.get(name=league)
    except League.DoesNotExist:
        raise ModuleNotFoundError

    print(list(leagueObj.games.all()))
    return list(
        leagueObj.games.values())


def live_games():
    return list(Game.objects.filter(
        end_time__gte=datetime.now(),
        start_time__lte=datetime.now()
    ).values('homeTeam__name', 'homeTeam__image', 'awayTeam__name',
             'awayTeam__image', 'awayTeamScore', 'homeTeamScore',
             'start_time', 'end_time'))


def teams_per_league(league):
    leagueObj=League.objects.get(name=league)
    return list(leagueObj.teams.all().values())
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
