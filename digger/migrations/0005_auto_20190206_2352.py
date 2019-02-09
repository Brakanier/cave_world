# Generated by Django 2.1.5 on 2019-02-06 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digger', '0004_auto_20190206_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='build',
            name='tower_need_stone',
        ),
        migrations.RemoveField(
            model_name='build',
            name='tower_need_wood',
        ),
        migrations.RemoveField(
            model_name='build',
            name='wall_need_stone',
        ),
        migrations.AddField(
            model_name='build',
            name='tower_need',
            field=models.IntegerField(default=75),
        ),
        migrations.AddField(
            model_name='build',
            name='wall_need',
            field=models.IntegerField(default=150),
        ),
        migrations.AlterField(
            model_name='stock',
            name='need',
            field=models.IntegerField(default=0),
        ),
    ]