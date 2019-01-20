from django.db import models

# Create your models here.


class Stock(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
        null=True,
    )
    lvl = models.IntegerField(
        default=0,
    )
    # Materials
    stone = models.IntegerField(
        default=0,
    )
    stone_max = models.IntegerField(
        default=100,
    )
    diamond = models.IntegerField(
        default=0
    )
    diamond_max = models.IntegerField(
        default=100,
    )
    #  Ore
    ore_iron = models.IntegerField(
        default=0,
    )
    ore_iron_max = models.IntegerField(
        default=100,
    )
    ore_gold = models.IntegerField(
        default=0,
    )
    ore_gold_max = models.IntegerField(
        default=100,
    )
    # Ingot
    ingot_iron = models.IntegerField(
        default=0
    )
    ingot_iron_max = models.IntegerField(
        default=100,
    )
    ingot_gold = models.IntegerField(
        default=0
    )
    ingot_gold_max = models.IntegerField(
        default=100,
    )
    skull = models.IntegerField(
        default=0,
    )

    def create(self, user_id):
        self.user_id = user_id
        return self


class Build(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    forge = models.BooleanField(
        default=False,
    )
    tavern = models.BooleanField(
        default=False,
    )
    lift = models.BooleanField(
        default=False,
    )


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
        blank=True,
    )
    lvl = models.IntegerField(
        default=1,

    )
    exp_need = models.BigIntegerField(
        default=10
    )
    exp = models.BigIntegerField(
        default=0,
    )
    energy = models.IntegerField(
        default=10,
    )
    max_energy = models.IntegerField(
        default=10,
    )
    last_energy_action = models.BigIntegerField(
        default=0,
    )
    energy_regen = models.IntegerField(
        default=1,
    )
    place = models.CharField(
        max_length=50,
        default='cave',
    )
    stock = models.OneToOneField(
        Stock,
        on_delete=models.CASCADE,
        null=True,
    )
    build = models.OneToOneField(
        Build,
        on_delete=models.CASCADE,
        null=True,
    )

    def create(self, user_id, stock):
        self.stock = stock
        self.user_id = user_id
        return self
