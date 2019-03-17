from django.db import models


class Effect(models.Model):
    id = models.AutoField(
        db_index=True,
        unique=True,
        primary_key=True,
    )
    title = models.CharField(
        max_length=50,
    )
    value = models.FloatField(
        default=0,
    )

    class Meta:
        verbose_name = 'Эффект'
        verbose_name_plural = 'Эффекты'

    def __str__(self):
        return self.title
