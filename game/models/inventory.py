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

    def __str__(self):
        return str(self.user_id) + ' - Инвентарь'


class InventoryChest(models.Model):
    chest = models.ForeignKey(
        'game.Chest',
        on_delete=models.CASCADE,
        null=True,
    )
    inventory = models.ForeignKey(
        'game.Inventory',
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
    )
    count = models.IntegerField(
        default=0,
    )

    class Meta:
        verbose_name = 'Инвентарь сундуков'
        verbose_name_plural = 'Инвентари сундуков'

    def __str__(self):
        return str(self.inventory) + ' - ' + str(self.chest) + ' [' + str(self.count) + ']'


class InventoryTrophy(models.Model):
    trophy = models.ForeignKey(
        'game.Trophy',
        on_delete=models.CASCADE,
        null=True,
    )
    inventory = models.ForeignKey(
        'game.Inventory',
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
    )
    count = models.IntegerField(
        default=0,
    )

    class Meta:
        verbose_name = 'Инвентарь трофеев'
        verbose_name_plural = 'Инвентари трофеев'

    def __str__(self):
        return str(self.inventory) + ' - ' + str(self.trophy) + ' [' + str(self.count) + ']'
