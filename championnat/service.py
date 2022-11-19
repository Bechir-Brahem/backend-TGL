from django.http import Http404

from .models import Game, League, Player, Team


def leagues():
    return League.objects.all()


def games_per_league(league):
    try:
        leagueObj = League.objects.get(name=league)
    except League.DoesNotExist:
        raise Http404
    return leagueObj.games.all()


def live_games():
    return Game.objects.filter(live=True).all()


def teams_per_league(league):
    try:
        leagueObj = League.objects.get(name=league)
    except League.DoesNotExist:
        raise Http404
    return leagueObj.teams.all()


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


def game_per_id(game):
    try:
        game = Game.objects.get(id=game)
    except Game.DoesNotExist:
        raise Http404
    return game


def players_per_team(team):
    return Player.objects.filter(team__name=team)


def players_per_league(league):
    return Player.objects.filter(team__league__name=league)
