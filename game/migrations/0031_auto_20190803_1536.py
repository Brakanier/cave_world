# Generated by Django 2.1.5 on 2019-08-03 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0030_auto_20190730_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caveprogress',
            name='level',
            field=models.IntegerField(default=1),
        ),
    ]