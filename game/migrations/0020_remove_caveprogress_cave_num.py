# Generated by Django 2.1.5 on 2019-05-19 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0019_caveprogress_cave_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caveprogress',
            name='cave_num',
        ),
    ]
