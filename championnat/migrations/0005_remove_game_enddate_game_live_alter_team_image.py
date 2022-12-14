# Generated by Django 4.1.1 on 2022-11-17 14:21

import championnat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championnat', '0004_rename_cartes_jaunes_player_cartons_jaunes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='endDate',
        ),
        migrations.AddField(
            model_name='game',
            name='live',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='team',
            name='image',
            field=models.ImageField(upload_to=championnat.models.PathAndRename('static')),
        ),
    ]
