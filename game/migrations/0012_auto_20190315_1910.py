# Generated by Django 2.1.5 on 2019-03-15 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_inventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='chests',
            field=models.ManyToManyField(blank=True, to='game.Chest'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='items',
            field=models.ManyToManyField(blank=True, to='game.Item'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='trophy',
            field=models.ManyToManyField(blank=True, to='game.Trophy'),
        ),
    ]