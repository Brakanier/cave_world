# Generated by Django 2.1.5 on 2019-04-19 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20190415_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='chat_id',
            field=models.BigIntegerField(blank=True, db_index=True, default=0),
        ),
    ]
