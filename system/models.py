from django.db import models

# Create your models here.


class Registration(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    reg = models.BooleanField(
        default=False,
    )


class Chat(models.Model):
    peer_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    count_users = models.IntegerField(
        default=0,
    )
