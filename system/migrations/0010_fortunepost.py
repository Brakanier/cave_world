# Generated by Django 2.1.5 on 2019-07-20 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_chat_distribution'),
    ]

    operations = [
        migrations.CreateModel(
            name='FortunePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.BigIntegerField(db_index=True, unique=True)),
            ],
        ),
    ]
