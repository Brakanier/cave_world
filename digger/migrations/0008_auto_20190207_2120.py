# Generated by Django 2.1.5 on 2019-02-07 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digger', '0007_auto_20190207_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='army',
            field=models.OneToOneField(null=True, on_delete=models.SET(None), to='digger.Army'),
        ),
        migrations.AlterField(
            model_name='player',
            name='build',
            field=models.OneToOneField(null=True, on_delete=models.SET(None), to='digger.Build'),
        ),
        migrations.AlterField(
            model_name='player',
            name='forge',
            field=models.OneToOneField(null=True, on_delete=models.SET(None), to='digger.Forge'),
        ),
        migrations.AlterField(
            model_name='player',
            name='stock',
            field=models.OneToOneField(null=True, on_delete=models.SET(None), to='digger.Stock'),
        ),
        migrations.AlterField(
            model_name='player',
            name='war',
            field=models.OneToOneField(null=True, on_delete=models.SET(None), to='digger.War'),
        ),
        migrations.AlterField(
            model_name='war',
            name='enemy_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
