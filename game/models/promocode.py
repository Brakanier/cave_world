from django.db import models

from ..actions.functions import *
from ..actions.chests import *


class PromoCode(models.Model):
    user_id = user_id = models.BigIntegerField(
        db_index=True,
    )
    code = models.CharField(
        max_length=30,
        db_index=True,
    )
