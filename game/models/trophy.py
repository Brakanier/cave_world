from django.db import models


class Trophy(models.Model):
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
    value = models.IntegerField(
        default=0,
    )

    class Meta:
        verbose_name = 'Трофей(дроп)'
        verbose_name_plural = 'Трофеи(дроп)'

    def __str__(self):
        return self.title


class TrophyChance(models.Model):
    id = models.AutoField(
        db_index=True,
        unique=True,
        primary_key=True,
    )
    title = models.CharField(
        max_length=50,
    )
    trophy = models.ManyToManyField(Trophy)
    chance = models.FloatField(
        default=0,
    )

    class Meta:
        verbose_name = 'Шанс трофея'
        verbose_name_plural = 'Шансы трофеев'

    def __str__(self):
        return self.title
