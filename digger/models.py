from django.db import models

# Create your models here.


class Stock(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
        null=True,
    )
    lvl = models.IntegerField(
        default=1,
    )
    need = models.IntegerField(
        default=50,
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
    iron = models.IntegerField(
        default=0,
    )
    iron_max = models.IntegerField(
        default=100,
    )
    gold = models.IntegerField(
        default=0,
    )
    gold_max = models.IntegerField(
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


class Forge(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    kit_warrior = models.IntegerField(
        default=0,
    )
    kit_archer = models.IntegerField(
        default=0,
    )
    kit_wizard = models.IntegerField(
        default=0,
    )
    pickaxe_stone = models.BooleanField(
        default=False,
    )
    pickaxe_iron = models.BooleanField(
        default=False,
    )
    pickaxe_diamond = models.BooleanField(
        default=False,
    )
    pickaxe_skull = models.BooleanField(
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
    forge = models.OneToOneField(
        Forge,
        on_delete=models.CASCADE,
        null=True,
    )


    def create(self, user_id, stock, furnace):
        self.furnace = furnace
        self.stock = stock
        self.user_id = user_id
        return self
