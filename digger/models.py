from django.db import models

# Create your models here.

class Player(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
    )
    nickname = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
    )
    lvl = models.IntegerField(
        default=1,

    )
    energy = models.IntegerField(
        default=10,
    )
    max_energy = models.IntegerField(
        default=10,
    )
    def create(self, user_id):
        self.user_id = user_id
        return self
