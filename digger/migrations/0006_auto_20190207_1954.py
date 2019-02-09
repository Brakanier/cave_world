# Generated by Django 2.1.5 on 2019-02-07 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digger', '0005_auto_20190206_2352'),
    ]

    operations = [
        migrations.CreateModel(
            name='War',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(db_index=True, unique=True)),
                ('enemy_id', models.BigIntegerField(null=True)),
                ('shield_type', models.IntegerField(null=True)),
                ('find_last_time', models.BigIntegerField(default=0)),
                ('war_last_time', models.BigIntegerField(default=0)),
                ('pve_last_time', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='war',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='digger.War'),
        ),
    ]