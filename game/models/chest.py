from django.db import models

from .trophy import TrophyChance
from .items import ItemChance


class Chest(models.Model):
    id = models.AutoField(
        db_index=True,
        unique=True,
        primary_key=True,
    )
    title = models.CharField(
        max_length=50,
    )
    slug = models.CharField(
        max_length=30,
        blank=True,
        db_index=True,
    )
    trophy_chance = models.ManyToManyField(
        TrophyChance,
        blank=True,
    )
    items_chance = models.ManyToManyField(
        ItemChance,
        blank=True,
    )

    class Meta:
        verbose_name = 'Сундук'
        verbose_name_plural = 'Сундуки'

    def __str__(self):
        return self.title


class ChestChance(models.Model):
    id = models.AutoField(
        db_index=True,
        unique=True,
        primary_key=True,
    )
    title = models.CharField(
        max_length=50,
    )
    chest = models.ManyToManyField(Chest)
    chance = models.FloatField(
        default=0,
    )

    class Meta:
        verbose_name = 'Шанс сундука'
        verbose_name_plural = 'Шансы сундуков'

    def __str__(self):
        return self.title
