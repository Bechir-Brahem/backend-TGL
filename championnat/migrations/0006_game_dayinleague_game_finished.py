# Generated by Django 4.1.1 on 2022-11-17 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championnat', '0005_remove_game_enddate_game_live_alter_team_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='dayInLeague',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]