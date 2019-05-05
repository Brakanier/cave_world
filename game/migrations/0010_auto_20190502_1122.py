# Generated by Django 2.1.5 on 2019-05-02 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=models.SET(None), related_name='player', to='game.Player'),
        ),
    ]
