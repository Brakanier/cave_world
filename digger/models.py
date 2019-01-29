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
    wood = models.IntegerField(
        default=0,
    )
    wood_max = models.IntegerField(
        default=100,
    )
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
    gate = models.BooleanField(
        default=False,
    )


class Army(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    warrior = models.IntegerField(
        default=0,
    )
    warrior_hp = models.IntegerField(
        default=10,
    )
    warrior_attack = models.IntegerField(
        default=5,
    )
    archer = models.IntegerField(
        default=0,
    )
    archer_hp = models.IntegerField(
        default=10,
    )
    archer_attack = models.IntegerField(
        default=15,
    )
    wizard = models.IntegerField(
        default=0,
    )
    wizard_hp = models.IntegerField(
        default=10,
    )
    wizard_attack = models.IntegerField(
        default=30,
    )


class Forge(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    need = models.IntegerField(
        default=30,
    )
    sword = models.IntegerField(
        default=0,
    )
    bow = models.IntegerField(
        default=0,
    )
    orb = models.IntegerField(
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


class Tavern(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    need_stone = models.IntegerField(
        default=30,
    )
    need_iron = models.IntegerField(
        default=30,
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
    tavern = models.OneToOneField(
        Tavern,
        on_delete=models.CASCADE,
        null=True,
    )
    army = models.OneToOneField(
        Army,
        on_delete=models.CASCADE,
        null=True,
    )

    def create(self, user_id, stock, forge, tavern):
        self.forge = forge
        self.tavern = tavern
        self.stock = stock
        self.user_id = user_id
        return self
