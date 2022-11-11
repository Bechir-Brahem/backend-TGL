from django.db import models
from django.utils.html import mark_safe

from backend_TGL.settings import STATIC_PATH


class Team(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=STATIC_PATH)

    def image_tag(self):
        if self.image != '':
            return mark_safe('<img src="%s%s" width="150" height="150" />' % ('/', self.image))

    def name_tag(self):
        return self.name

    def __str__(self):
        return self.name


class Game(models.Model):
    league = models.CharField(max_length=200)
    homeTeam = models.ForeignKey('Team', on_delete=models.DO_NOTHING, related_name="homeTeam")
    awayTeam = models.ForeignKey('Team', on_delete=models.DO_NOTHING, related_name="awayTeam")
    homeTeamScore = models.IntegerField(default=0)
    awayTeamScore = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # duration = models.IntegerField(help_text="in minutes")

    def __str__(self):
        return f'({self.id}) {self.league}: {self.homeTeam.name}-{self.awayTeam.name}'
