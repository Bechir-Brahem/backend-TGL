from datetime import datetime

from .models import Game


def leagues():
    return Game.objects.values_list('league')


def games_for_all_leagues(limit=5):
    ret = {}
    print()

    for league in leagues():
        league = league[0]
        objects = Game.objects.filter(league=league).values('homeTeam__name', 'homeTeam__image', 'awayTeam__name',
                                                            'awayTeam__image'
                                                            , 'awayTeamScore', 'homeTeamScore', 'start_time',
                                                            'end_time')[:limit]
        ret[league] = list(objects)
    return ret


def games_per_league(league):
    return list(
        Game.objects.filter(
            league=league
        ).values('homeTeam__name', 'homeTeam__image', 'awayTeam__name',
                 'awayTeam__image', 'awayTeamScore', 'homeTeamScore',
                 'start_time', 'end_time'))


def live_games():
    return list(Game.objects.filter(
        end_time__gte=datetime.now(),
        start_time__lte=datetime.now()
    ).values('homeTeam__name', 'homeTeam__image', 'awayTeam__name',
             'awayTeam__image', 'awayTeamScore', 'homeTeamScore',
             'start_time', 'end_time'))
