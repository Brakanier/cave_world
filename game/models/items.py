from django.db import models

from .effects import Effect


class Item(models.Model):
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
    effects = models.ManyToManyField(Effect)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.title

