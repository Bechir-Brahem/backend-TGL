import datetime
import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.deconstruct import deconstructible
from django.utils.html import mark_safe

from backend_TGL.settings import STATIC_PATH
from .helper import get_now


class League(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


path_and_rename = PathAndRename(STATIC_PATH)


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to=path_and_rename)
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name='teams')
    points = models.IntegerField(default=0)
    victoires = models.IntegerField(default=0)
    nulles = models.IntegerField(default=0)
    pertes = models.IntegerField(default=0)
    buts_marque = models.IntegerField(default=0)
    buts_encaisse = models.IntegerField(default=0)

    def image_tag(self):
        if self.image != '':
            return mark_safe('<img src="%s%s" width="150" height="150" />' % ('/', self.image))

    def __str__(self):
        return self.league.abbreviation + ':' + self.name


class Player(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='players')
    fullname = models.CharField(max_length=50)
    cartons_jaunes = models.IntegerField(default=0)
    cartons_rouges = models.IntegerField(default=0)
    buts = models.IntegerField(default=0)

    def __str__(self):
        return self.team.name + ': ' + self.fullname


class Game(models.Model):
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name='games')
    homeTeam = models.ForeignKey('Team', on_delete=models.CASCADE, related_name="homeGames", )
    awayTeam = models.ForeignKey('Team', on_delete=models.CASCADE, related_name="awayGames")
    homeTeamScore = models.IntegerField(default=0)
    awayTeamScore = models.IntegerField(default=0)

    firstHalfStartDate = models.DateTimeField(default=datetime.datetime.now())
    firstHalfEndDate = models.DateTimeField(default=datetime.datetime.now())
    secondHalfStartDate = models.DateTimeField(default=datetime.datetime.now())
    secondHalfEndDate = models.DateTimeField(default=datetime.datetime.now())

    firstHalfFinished = models.BooleanField(default=False)
    secondHalfStarted = models.BooleanField(default=False)

    dayInLeague = models.IntegerField(default=0)
    live = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    # endDate = models.DateTimeField()
    updateTeamPoints = models.BooleanField(default=True)

    def __str__(self):
        return f'({self.id}) {self.league}: {self.homeTeam.name} {self.homeTeamScore}-' \
               f'{self.awayTeamScore} {self.awayTeam.name}+ {self.firstHalfStartDate}'

    def arbitreLink(self):
        return mark_safe(f"<a href={reverse('arbitre', kwargs={'game_id': self.id})}><u>Lien pour l'arbitre</u></a>")

    def counter(self):
        counter = 0
        if self.live and not self.firstHalfFinished and not self.secondHalfStarted and not self.finished:
            tmp = get_now() - self.firstHalfStartDate
            counter = tmp.total_seconds()
        elif self.live and self.firstHalfFinished and not self.secondHalfStarted and not self.finished:
            tmp = self.firstHalfEndDate - self.firstHalfStartDate
            counter = tmp.total_seconds()
        elif self.live and self.firstHalfFinished and self.secondHalfStarted and not self.finished:
            tmp = self.firstHalfEndDate - self.firstHalfStartDate
            counter = tmp.total_seconds()
            tmp = get_now() - self.secondHalfStartDate
            counter += tmp.total_seconds()
        elif not self.live and self.firstHalfFinished and self.secondHalfStarted and self.finished:
            tmp = self.firstHalfEndDate - self.firstHalfStartDate
            counter = tmp.total_seconds()
            tmp = self.secondHalfEndDate - self.secondHalfStartDate
            counter += tmp.total_seconds()
        return counter


class GameComment(models.Model):
    time = models.IntegerField(default=0)
    choices = (
        ('but', 'but'),
        ('carton jaune', 'carton jaune'),
        ('carton rouge', 'carton rouge')
    )
    type = models.CharField(max_length=15, choices=choices)
    player = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='comments')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return str(self.time) + "' " + self.type + ' ' + str(self.player)


def update_team_points(sender, instance, **kwargs):
    if instance.league != instance.homeTeam.league:
        raise Exception('homeTeam League is not the same as the Game League')
    if instance.league != instance.awayTeam.league:
        raise Exception('awayTeam League is not the same as the Game League')

    if not instance.updateTeamPoints:
        return
    if not instance.finished:
        return

    preSaveGame = None
    try:
        preSaveGame = Game.objects.get(id=instance.id)
    except Game.DoesNotExist:
        # new object
        pass

    if preSaveGame:
        if preSaveGame.homeTeamScore > preSaveGame.awayTeamScore:
            instance.homeTeam.points -= 3
            instance.homeTeam.victoires -= 1
            instance.awayTeam.pertes -= 1
        elif preSaveGame.homeTeamScore < preSaveGame.awayTeamScore:
            instance.awayTeam.points -= 3
            instance.homeTeam.pertes -= 1
            instance.awayTeam.victoires -= 1
        elif preSaveGame.homeTeamScore == preSaveGame.awayTeamScore:
            instance.homeTeam.points -= 1
            instance.awayTeam.points -= 1
            instance.homeTeam.nulles -= 1
            instance.awayTeam.nulles -= 1
        instance.homeTeam.buts_marque -= preSaveGame.homeTeamScore
        instance.homeTeam.buts_encaisse -= preSaveGame.awayTeamScore
        instance.awayTeam.buts_marque -= preSaveGame.awayTeamScore
        instance.awayTeam.buts_encaisse -= preSaveGame.homeTeamScore

    if instance.homeTeamScore > instance.awayTeamScore:
        instance.homeTeam.points += 3
        instance.homeTeam.victoires += 1
        instance.awayTeam.pertes += 1
    elif instance.homeTeamScore < instance.awayTeamScore:
        instance.awayTeam.points += 3
        instance.homeTeam.pertes += 1
        instance.awayTeam.victoires += 1
    elif instance.homeTeamScore == instance.awayTeamScore:
        instance.homeTeam.points += 1
        instance.awayTeam.points += 1
        instance.homeTeam.nulles += 1
        instance.awayTeam.nulles += 1

    instance.homeTeam.buts_marque += instance.homeTeamScore
    instance.homeTeam.buts_encaisse += instance.awayTeamScore
    instance.awayTeam.buts_marque += instance.awayTeamScore
    instance.awayTeam.buts_encaisse += instance.homeTeamScore

    instance.homeTeam.save()
    instance.awayTeam.save()


def update_player_info(sender, instance, **kwargs):
    preSaveComment = None
    try:
        preSaveComment = GameComment.objects.get(id=instance.id)
    except GameComment.DoesNotExist:
        # new object
        pass

    if preSaveComment:
        if preSaveComment.type == 'carton jaune':
            instance.player.cartons_jaunes -= 1
        elif preSaveComment.type == 'carton rouge':
            instance.player.cartons_rouges -= 1
        elif preSaveComment.type == 'but':
            instance.player.buts -= 1

    if instance.type == 'carton jaune':
        instance.player.cartons_jaunes += 1
    elif instance.type == 'carton rouge':
        instance.player.cartons_rouges += 1
    elif instance.type == 'but':
        instance.player.buts += 1
    instance.player.save()


pre_save.connect(update_team_points, sender=Game)
pre_save.connect(update_player_info, sender=GameComment)
