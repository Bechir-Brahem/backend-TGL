import datetime

from dateutil import tz
from django.apps import apps


def get_now(): return datetime.datetime.now().astimezone(tz=tz.gettz('Africa/Tunis'))


def reset_teams():
    Team = apps.get_model('championnat', "Team")
    Player = apps.get_model('championnat', "Player")
    Game = apps.get_model('championnat', "Game")
    GameComment = apps.get_model('championnat', "GameComment")
    for team in Team.objects.all():
        team.points = 0
        team.buts_encaisse = 0
        team.buts_marque = 0
        team.pertes = 0
        team.nulles = 0
        team.victoires = 0
        team.save()

    for player in Player.objects.all():
        player.cartons_jaunes = 0
        player.cartons_rouges = 0
        player.buts = 0
        player.save()

    for game in Game.objects.all():
        if game.finished:
            if game.homeTeamScore > game.awayTeamScore:
                game.homeTeam.points += 3
                game.homeTeam.victoires += 1
                game.awayTeam.pertes += 1
            elif game.homeTeamScore < game.awayTeamScore:
                game.awayTeam.points += 3
                game.homeTeam.pertes += 1
                game.awayTeam.victoires += 1
            elif game.homeTeamScore == game.awayTeamScore:
                game.homeTeam.points += 1
                game.awayTeam.points += 1
                game.homeTeam.nulles += 1
                game.awayTeam.nulles += 1

            game.homeTeam.buts_marque += game.homeTeamScore
            game.homeTeam.buts_encaisse += game.awayTeamScore
            game.awayTeam.buts_marque += game.awayTeamScore
            game.awayTeam.buts_encaisse += game.homeTeamScore

            game.awayTeam.save()
            game.homeTeam.save()

    for gameComment in GameComment.objects.all():
        if gameComment.type == 'carton jaune':
            gameComment.player.cartons_jaunes += 1
        elif gameComment.type == 'carton rouge':
            gameComment.player.cartons_rouges += 1
        elif gameComment.type == 'but':
            gameComment.player.buts += 1
        gameComment.player.save()
