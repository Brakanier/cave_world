# Generated by Django 2.1.5 on 2019-03-14 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20190314_1446'),
    ]

    operations = [
        migrations.RenameField(
            model_name='war',
            old_name='enemy_armyenemy_army',
            new_name='enemy_army',
        ),
        migrations.RemoveField(
            model_name='player',
            name='war',
        ),
    ]