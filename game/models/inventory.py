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
        through='InventoryTrophy',
        through_fields=('inventory', 'trophy'),
        blank=True,
    )
    chests = models.ManyToManyField(
        'game.Chest',
        through='InventoryChest',
        through_fields=('inventory', 'chest'),
        blank=True,
    )

    class Meta:
        verbose_name = 'Инвентарь'
        verbose_name_plural = 'Инвентари'


class InventoryChest(models.Model):
    chest = models.ForeignKey(
        'game.Chest',
        on_delete=models.CASCADE,
        null=True,
    )
    inventory = models.ForeignKey(
        'game.Inventory',
        on_delete=models.CASCADE,
        null=True,
    )
    count = models.IntegerField(
        default=0,
    )


class InventoryTrophy(models.Model):
    trophy = models.ForeignKey(
        'game.Trophy',
        on_delete=models.CASCADE,
        null=True,
    )
    inventory = models.ForeignKey(
        'game.Inventory',
        on_delete=models.CASCADE,
        null=True,
    )
    count = models.IntegerField(
        default=0,
    )

