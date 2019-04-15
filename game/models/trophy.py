from django.db import models


class Trophy(models.Model):
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
