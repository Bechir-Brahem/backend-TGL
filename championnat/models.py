from pprint import pprint

from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q
from django.db.models.functions import Lower
from django.db.models.signals import pre_save
from django.utils.html import mark_safe
from django.http import HttpResponseBadRequest

from backend_TGL.settings import STATIC_PATH


class League(models.Model):
    name = models.CharField(max_length=100,unique=True)
    abbreviation = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.abbreviation+':'+self.name


class Team(models.Model):
    name = models.CharField(max_length=50,unique=True)
    image = models.ImageField(upload_to=STATIC_PATH)
    league = models.ForeignKey('League', on_delete=models.DO_NOTHING, related_name='teams')
    points = models.IntegerField(default=0)

    def image_tag(self):
        if self.image != '':
            return mark_safe('<img src="%s%s" width="150" height="150" />' % ('/', self.image))

    def get_name(self):
        return self.name

    def get_points(self):
        return self.points

    def __str__(self):
        return self.league.abbreviation+':'+self.name


class Game(models.Model):
    league = models.ForeignKey('League', on_delete=models.DO_NOTHING, related_name='games')
    homeTeam = models.ForeignKey('Team', on_delete=models.DO_NOTHING, related_name="homeTeam")
    awayTeam = models.ForeignKey('Team', on_delete=models.DO_NOTHING, related_name="awayTeam")
    homeTeamScore = models.IntegerField(default=0)
    awayTeamScore = models.IntegerField(default=0)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    updateTeamPoints = models.BooleanField(default=True)


    def __str__(self):
        return f'({self.id}) {self.league}: {self.homeTeam.name} {self.homeTeamScore}-' \
               f'{self.awayTeamScore} {self.awayTeam.name}+ {self.startDate}'


def update_team_points(sender, instance, **kwargs):
    if instance.league != instance.homeTeam.league:
        raise Exception('homeTeam League is not the same as the Game League')
    if instance.league != instance.awayTeam.league:
        raise Exception('awayTeam League is not the same as the Game League')


    if not instance.updateTeamPoints:
        return

    preSaveGame = None
    try:
        preSaveGame = Game.objects.get(id=instance.id)
    except Game.DoesNotExist:
        # new object
        pass

    print(instance.homeTeam.points, instance.awayTeam.points)
    if preSaveGame:
        if preSaveGame.homeTeamScore > preSaveGame.awayTeamScore:
            instance.homeTeam.points -= 3
        elif preSaveGame.homeTeamScore < preSaveGame.awayTeamScore:
            instance.awayTeam.points -= 3
        elif preSaveGame.homeTeamScore == preSaveGame.awayTeamScore:
            instance.homeTeam.points -= 1
            instance.awayTeam.points -= 1
    print(instance.homeTeam.points, instance.awayTeam.points)

    pprint('pre save value: ' + str(preSaveGame) if preSaveGame else 'new game')
    pprint('new incoming value' + str(instance))
    print(instance.homeTeamScore)
    print(instance.awayTeamScore)
    print(instance.homeTeamScore > instance.awayTeamScore)
    print(instance.homeTeam.points, instance.awayTeam.points)
    if instance.homeTeamScore > instance.awayTeamScore:
        instance.homeTeam.points += 3
    elif instance.homeTeamScore < instance.awayTeamScore:
        instance.awayTeam.points += 3
    elif instance.homeTeamScore == instance.awayTeamScore:
        instance.homeTeam.points += 1
        instance.awayTeam.points += 1
    instance.homeTeam.save()
    instance.awayTeam.save()
    print(instance.homeTeam.points, instance.awayTeam.points)


pre_save.connect(update_team_points, sender=Game)
