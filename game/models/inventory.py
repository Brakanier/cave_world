from django.db import models

from .items import Item
from .trophy import Trophy
from .chest import Chest


class Inventory(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    items = models.ManyToManyField(
        Item,
        blank=True,
    )
    trophy = models.ManyToManyField(
        Trophy,
        blank=True,
    )
    chests = models.ManyToManyField(
        Chest,
        blank=True,
    )

    class Meta:
        verbose_name = 'Инвентарь'
        verbose_name_plural = 'Инвентари'
