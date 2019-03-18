# Generated by Django 2.1.5 on 2019-03-15 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20190315_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(db_index=True, unique=True)),
                ('chests', models.ManyToManyField(to='game.Chest')),
                ('items', models.ManyToManyField(to='game.Item')),
                ('trophy', models.ManyToManyField(to='game.Trophy')),
            ],
        ),
    ]