# Generated by Django 4.1 on 2022-11-13 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('abbreviation', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(upload_to='static')),
                ('points', models.IntegerField(default=0)),
                ('victoires', models.IntegerField(default=0)),
                ('nulles', models.IntegerField(default=0)),
                ('pertes', models.IntegerField(default=0)),
                ('buts_marque', models.IntegerField(default=0)),
                ('buts_encaisse', models.IntegerField(default=0)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='teams', to='championnat.league')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='players', to='championnat.team')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homeTeamScore', models.IntegerField(default=0)),
                ('awayTeamScore', models.IntegerField(default=0)),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
                ('updateTeamPoints', models.BooleanField(default=True)),
                ('awayTeam', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='awayTeam', to='championnat.team')),
                ('homeTeam', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='homeTeam', to='championnat.team')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='games', to='championnat.league')),
            ],
        ),
    ]
