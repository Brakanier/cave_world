# Generated by Django 2.1.5 on 2019-07-20 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_auto_20190716_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='distribution',
            field=models.BooleanField(default=True),
        ),
    ]
