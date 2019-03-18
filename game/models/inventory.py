from django.db import models


class Inventory(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    items = models.ManyToManyField(
        'game.Item',
        blank=True,
    )
    trophy = models.ManyToManyField(
        'game.Trophy',
        blank=True,
    )
    chests = models.ManyToManyField(
        'game.Chest',
        blank=True,
    )

    class Meta:
        verbose_name = 'Инвентарь'
        verbose_name_plural = 'Инвентари'
