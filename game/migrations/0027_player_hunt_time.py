# Generated by Django 2.1.5 on 2019-07-11 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0026_player_alcohol_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='hunt_time',
            field=models.BigIntegerField(default=0),
        ),
    ]
