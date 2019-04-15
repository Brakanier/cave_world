from django.db import models


class Chest(models.Model):
    id = models.AutoField(
        db_index=True,
        unique=True,
        primary_key=True,
    )
    title = models.CharField(
        max_length=50,
        db_index=True,
    )
    slug = models.CharField(
        max_length=30,
        blank=True,
        db_index=True,
    )

    trophy_chance = models.ManyToManyField(
        'game.ChestTrophy',
        related_name='trophy_chest',
        blank=True,
    )
    items_chance = models.ManyToManyField(
        'game.ChestItem',
        related_name='item_chest',
        blank=True,
    )

    class Meta:
        verbose_name = 'Сундук'
        verbose_name_plural = 'Сундуки'

    def __str__(self):
        return self.title


class ChestTrophy(models.Model):
    trophy = models.ForeignKey(
        'game.Trophy',
        on_delete=models.CASCADE,
        null=True,
    )
    chest = models.ForeignKey(
        'game.Chest',
        on_delete=models.CASCADE,
        null=True,
    )
    chance = models.FloatField(
        default=0,
    )

    class Meta:
        verbose_name = 'Сундук с трофеем'
        verbose_name_plural = 'Сундуки с трофеями'

    def __str__(self):
        return str(self.chest) + ' - ' + str(self.trophy) + ' | ' + str(self.chance * 100) + ' %'


class ChestItem(models.Model):
    item = models.ForeignKey(
        'game.Item',
        on_delete=models.CASCADE,
        null=True,
    )
    chest = models.ForeignKey(
        'game.Chest',
        on_delete=models.CASCADE,
        null=True,
    )
    chance = models.FloatField(
        default=0,
    )

    class Meta:
        verbose_name = 'Сундук с предметом'
        verbose_name_plural = 'Сундуки с предметами'

    def __str__(self):
        return str(self.chest) + ' - ' + str(self.item) + ' | ' + str(self.chance * 100) + ' %'
