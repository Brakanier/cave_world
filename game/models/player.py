from django.db import models

from .build import Stock
from .items import Item
from ..actions.functions import *

import random

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
        db_index=True,
        unique=True,
    )
    lvl = models.IntegerField(
        default=1,
    )
    exp = models.BigIntegerField(
        default=0,
    )
    energy = models.IntegerField(
        default=20,
    )
    max_energy = models.IntegerField(
        default=20,
    )
    last_energy_action = models.BigIntegerField(
        default=0,
    )
    energy_regen = models.IntegerField(
        default=1,
    )
    bonus_time = models.BigIntegerField(
        default=0,
    )
    place = models.CharField(
        max_length=50,
        default='cave',
    )
    build = models.OneToOneField(
        'game.Build',
        on_delete=models.SET(None),
        null=True,
    )
    war = models.OneToOneField(
        'game.War',
        on_delete=models.SET(None),
        null=True,
    )
    inventory = models.OneToOneField(
        'game.Inventory',
        on_delete=models.SET(None),
        null=True,
    )

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def create(self, user_id, build, war):
        self.build = build
        self.war = war
        self.user_id = user_id
        return self

    # Действия

    def get_stone(self, action_time, chat_info, amount=1):
        self.build.stock = self.build.get_passive(action_time)
        self = energy(self, action_time)
        if self.energy >= GET_ENERGY * amount:
            stone = 8 * amount
            stone = stone + random.randint(-4 * amount, 4 * amount)
            space = self.build.stock.max - self.build.stock.stone
            if space > 0:
                if space >= stone:
                    self.energy = self.energy - GET_ENERGY * amount
                    stone = min(stone, space)
                    self.build.stock.stone = self.build.stock.stone + stone
                    self = exp(self, chat_info, GET_ENERGY * amount)
                    message = 'Добыто камня: ' + str(stone) + icon('stone') + '\n' + \
                              'Энергия: ' + str(self.energy) + '/' + str(self.max_energy) + icon('energy') + '\n' + \
                              'Опыт: ' + str(self.exp) + '/' + str(exp_need(self.lvl)) + icon('exp')
                    Stock.objects.filter(user_id=self.user_id).update(stone=self.build.stock.stone)
                else:
                    message = 'Нехватает места!\n'
            else:
                message = 'Склад заполнен!'
            Player.objects.filter(user_id=self.user_id).update(energy=self.energy,
                                                               last_energy_action=self.last_energy_action,
                                                               exp=self.exp,
                                                               lvl=self.lvl)
        else:
            message = 'Недостаточно энергии!'
        return message

    def get_wood(self, action_time, chat_info, amount=1):
        self.build.stock = self.build.get_passive(action_time)
        self = energy(self, action_time)
        if self.energy >= GET_ENERGY * amount:
            wood = 8 * amount
            wood = wood + random.randint(-4 * amount, 4 * amount)
            space = self.build.stock.max - self.build.stock.wood
            if space > 0:
                if space >= wood:
                    self.energy = self.energy - GET_ENERGY * amount
                    wood = min(wood, space)
                    self.build.stock.wood = self.build.stock.wood + wood
                    self = exp(self, chat_info, GET_ENERGY * amount)
                    message = 'Добыто дерева: ' + str(wood) + icon('wood') + '\n' + \
                              'Энергия: ' + str(self.energy) + '/' + str(self.max_energy) + icon('energy') + '\n' + \
                              'Опыт: ' + str(self.exp) + '/' + str(exp_need(self.lvl)) + icon('exp')
                    Stock.objects.filter(user_id=self.user_id).update(wood=self.build.stock.wood)
                else:
                    message = 'Нехватает места!\n'
            else:
                message = 'Склад заполнен!'
            Player.objects.filter(user_id=self.user_id).update(energy=self.energy,
                                                               last_energy_action=self.last_energy_action,
                                                               exp=self.exp,
                                                               lvl=self.lvl)
        else:
            message = 'Недостаточно энергии!'
        return message

    def get_iron(self, action_time, chat_info, amount=1):
        self.build.stock = self.build.get_passive(action_time)
        item = in_items(self.inventory.items.all(), 'stone_pickaxe')
        if item:
            self = energy(self, action_time)
            if self.energy >= GET_ENERGY * amount:
                iron = 4 * amount
                iron = iron + random.randint(-2 * amount, 2 * amount)
                space = self.build.stock.max - self.build.stock.iron
                if space > 0:
                    if space >= iron:
                        self.energy = self.energy - GET_ENERGY * amount
                        iron = min(iron, space)
                        self.build.stock.iron = self.build.stock.iron + iron
                        self = exp(self, chat_info, GET_ENERGY * amount)
                        message = 'Добыто железа: ' + str(iron) + icon('iron') + '\n' + \
                                  'Энергия: ' + str(self.energy) + '/' + str(self.max_energy) + icon('energy') + '\n' + \
                                  'Опыт: ' + str(self.exp) + '/' + str(exp_need(self.lvl)) + icon('exp')
                        Stock.objects.filter(user_id=self.user_id).update(iron=self.build.stock.iron)
                    else:
                        message = 'Нехватает места!\n'
                else:
                    message = 'Склад заполнен!'
                Player.objects.filter(user_id=self.user_id).update(energy=self.energy,
                                                                   last_energy_action=self.last_energy_action,
                                                                   exp=self.exp,
                                                                   lvl=self.lvl)
            else:
                message = 'Недостаточно энергии!'
        else:
            message = 'Вы не можете добывать' + icon('iron') + ' Железо!\n' + \
                      'Нужна Каменная Кирка!'
        return message

    def get_diamond(self, action_time, chat_info, amount=1):
        self.build.stock = self.build.get_passive(action_time)
        item = in_items(self.inventory.items.all(), 'iron_pickaxe')
        if item:
            self = energy(self, action_time)
            if self.energy >= GET_ENERGY * amount:
                diamond = 2 * amount
                diamond = diamond + random.randint(-1 * amount, 1 * amount)
                space = self.build.stock.max - self.build.stock.diamond
                if space > 0:
                    if space >= diamond:
                        self.energy = self.energy - GET_ENERGY * amount
                        diamond = min(diamond, space)
                        self.build.stock.diamond = self.build.stock.diamond + diamond
                        self = exp(self, chat_info, GET_ENERGY * amount)
                        message = 'Добыто кристалов: ' + str(diamond) + icon('diamond') + '\n' + \
                                  'Энергия: ' + str(self.energy) + '/' + str(self.max_energy) + icon('energy') + '\n' + \
                                  'Опыт: ' + str(self.exp) + '/' + str(exp_need(self.lvl)) + icon('exp')
                        Stock.objects.filter(user_id=self.user_id).update(diamond=self.build.stock.diamond)
                    else:
                        message = 'Не хватает места!\n'
                else:
                    message = 'Склад заполнен!'
                Player.objects.filter(user_id=self.user_id).update(energy=self.energy,
                                                                   last_energy_action=self.last_energy_action,
                                                                   exp=self.exp,
                                                                   lvl=self.lvl)
            else:
                message = 'Недостаточно энергии!'
        else:
            message = 'Вы не можете добывать' + icon('diamond') + ' Кристалы!\n' + \
                      'Нужна Железная Кирка!'
        return message

    def bonus(self, action_time):
        time = action_time - self.bonus_time
        if time > BONUS_TIME:
            self.bonus_time = action_time
            self.build.stock.stone = self.build.stock.stone + BONUS_STONE
            self.build.stock.wood = self.build.stock.wood + BONUS_WOOD
            self.build.stock.iron = self.build.stock.iron + BONUS_IRON
            self.build.stock.diamond = self.build.stock.diamond + BONUS_DIAMOND
            self.build.stock.gold = self.build.stock.gold + BONUS_GOLD
            Stock.objects.filter(user_id=self.user_id).update(stone=self.build.stock.stone,
                                                              wood=self.build.stock.wood,
                                                              iron=self.build.stock.iron,
                                                              diamond=self.build.stock.diamond,
                                                              gold=self.build.stock.gold)
            Player.objects.filter(user_id=self.user_id).update(bonus_time=self.bonus_time)
            message = 'Вы получили ежедневный бонус!\n+ ' + \
                      str(BONUS_STONE) + icon('stone') + '\n + ' + \
                      str(BONUS_WOOD) + icon('wood') + '\n + ' + \
                      str(BONUS_IRON) + icon('iron') + '\n + ' + \
                      str(BONUS_DIAMOND) + icon('diamond') + '\n + ' + \
                      str(BONUS_GOLD) + icon('gold')
        else:
            hour = (BONUS_TIME - time) // 3600
            minutes = ((BONUS_TIME - time) - (hour * 3600)) // 60
            sec = (BONUS_TIME - time) - (minutes * 60) - (hour * 3600)
            message = 'До бонуса: ' + str(hour) + ' ч. ' + str(minutes) + ' м. ' + str(sec) + ' сек.'
        return message

    def craft_stone_pickaxe(self, action_time):
        self.build.stock = self.build.get_passive(action_time)
        item = in_items(self.inventory.items.all(), 'stone_pickaxe')
        if not item:
            if self.build.stock.stone >= STONE_PICKAXE:
                self.build.stock.stone = self.build.stock.stone - STONE_PICKAXE
                pickaxe = Item.objects.get(slug='stone_pickaxe')
                self.inventory.items.add(pickaxe)
                Stock.objects.filter(user_id=self.user_id).update(stone=self.build.stock.stone)
                message = 'Поздравляю!\n' + \
                          'Вы скрафтили' + icon('stone') + ' ' + pickaxe.title + icon('stone') + ' !\n'
                effects = pickaxe.effects.all()
                for effect in effects:
                    message += effect.title + '!\n'
            else:
                message = 'Недостаточно камня'
        else:
            message = 'У вас уже есть ' + item.title + '!'
        return message

    def craft_iron_pickaxe(self, action_time):
        self.build.stock = self.build.get_passive(action_time)
        item = in_items(self.inventory.items.all(), 'iron_pickaxe')
        if not item:
            if self.build.stock.iron >= IRON_PICKAXE:
                self.build.stock.iron = self.build.stock.iron - IRON_PICKAXE
                pickaxe = Item.objects.get(slug='iron_pickaxe')
                self.inventory.items.add(pickaxe)
                Stock.objects.filter(user_id=self.user_id).update(iron=self.build.stock.iron)
                message = 'Поздравляю!\n' + \
                          'Вы скрафтили' + icon('iron') + ' ' + pickaxe.title + icon('iron') + ' !\n'
                effects = pickaxe.effects.all()
                for effect in effects:
                    message += effect.title + '!\n'
            else:
                message = 'Недостаточно камня'
        else:
            message = 'У вас уже есть ' + item.title + '!'
        return message

    def craft_diamond_pickaxe(self, action_time):
        self.build.stock = self.build.get_passive(action_time)
        item = in_items(self.inventory.items.all(), 'diamond_pickaxe')
        if not item:
            if self.build.stock.diamond >= DIAMOND_PICKAXE:
                self.build.stock.diamond = self.build.stock.diamond - DIAMOND_PICKAXE
                pickaxe = Item.objects.get(slug='diamond_pickaxe')
                self.inventory.items.add(pickaxe)
                Stock.objects.filter(user_id=self.user_id).update(diamond=self.build.stock.diamond)
                message = 'Поздравляю!\n' + \
                          'Вы скрафтили' + icon('diamond') + ' ' + pickaxe.title + icon('diamond') + ' !\n'
                effects = pickaxe.effects.all()
                for effect in effects:
                    message += effect.title + '!\n'

            else:
                message = 'Недостаточно камня'
        else:
            message = 'У вас уже есть ' + item.title + '!'
        return message

    # Инфо

    def profile(self, action_time):
        if not self.place == 'profile':
            self.place = 'profile'

        self = energy(self, action_time)
        Player.objects.filter(user_id=self.user_id).update(energy=self.energy,
                                                           last_energy_action=self.last_energy_action,
                                                           place=self.place)
        message = 'Ник: ' + self.nickname + '\n' + \
                  'Имя: ' + self.first_name + '\n' + \
                  'Фамилия: ' + self.last_name + '\n' + \
                  'Уровень: ' + str(self.lvl) + icon('lvl') + '\n' + \
                  'Опыт: ' + str(self.exp) + '/' + str(exp_need(self.lvl)) + icon('exp') + '\n' + \
                  'Энергия: ' + str(self.energy) + '/' + str(self.max_energy) + icon('energy')

        return message

    def top(self):
        self.place = 'top'
        Player.objects.filter(user_id=self.user_id).update(place=self.place)
        message = 'Выберите топ'
        return message

    def top_lvl(self):
        top = Player.objects.order_by('-lvl').values_list('nickname', 'lvl')[0:9]
        count = 1
        main_message = 'Топ игроков по уровню 👑\n'
        for user in top:
            message = str(count) + ' | ' + str(user[0]) + ' - ' + str(user[1]) + ' 👑\n'
            count += 1
            main_message = main_message + message
        return main_message

    # Строительство

    def cave_build(self):
        if not self.place == 'cave_build':
            self.place = 'cave_build'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
        message_stock = 'Склад' + icon('stock') + ': ' + str(self.build.stock.lvl * STOCK_STONE) + icon('stone') + '\n'
        message_forge = 'Кузница' + icon('craft') + ': ' + str(FORGE_STONE) + icon('stone') + '\n'
        message_tavern = 'Таверна' + icon('tavern') + ': ' + str(TAVERN_STONE) + icon('stone') + ' + ' + \
                         str(TAVERN_IRON) + icon('iron') + '\n'
        message_citadel = 'Цитадель' + icon('citadel') + ': ' + \
                          str(CITADEL_STONE) + icon('stone') + ' + ' + \
                          str(CITADEL_IRON) + icon('iron') + ' + ' + \
                          str(CITADEL_DIAMOND) + icon('diamond') + '\n'
        message = 'Стоимость:' + '\n'
        message = message + message_stock
        if not self.build.forge:
            message = message + message_forge
        if not self.build.tavern:
            message = message + message_tavern
        if not self.build.citadel:
            message = message + message_citadel
        return message

    def land_build(self):
        if not self.place == 'land_build':
            self.place = 'land_build'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
        # башня
        message_tower = 'Башня: ' + \
                        str((self.build.tower_lvl + 1) * TOWER_STONE) + icon('stone') + ' + ' + \
                        str((self.build.tower_lvl + 1) * TOWER_WOOD) + icon('wood') + '\n'
        # стена
        message_wall = 'Стена: ' + \
                       str((self.build.wall_lvl + 1) * WALL_STONE) + icon('stone') + ' + ' + \
                       str((self.build.wall_lvl + 1) * WALL_WOOD) + icon('wood') + '\n'
        message = 'Стоимость:\n'
        message = message + message_tower + message_wall
        return message

    # Локации

    def mine(self):
        if self.place == 'mine':
            message = 'Вы уже в Шахте'
        else:
            self.place = 'mine'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = 'Вы спустили в Шахту'
        return message

    def cave(self):
        if self.place == 'cave':
            message = 'Вы уже в Подземелье'
        else:
            self.place = 'cave'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = 'Вы вернулись в Подземелье'
        return message

    def land(self):
        if self.place == 'land':
            message = 'Вы уже в Землях'
        else:
            self.place = 'land'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = 'Вы вышли в Земли'
        return message

    def buy(self):
        if self.place == 'army':
            message = 'Вы уже в меню найма!'
        else:
            self.place = 'army'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = 'Здесь вы можете нанять себе армию!'
        return message

    def forge(self):
        if self.place == 'forge':
            message = 'Вы уже в Кузнице'
        else:
            self.place = 'forge'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = 'Вы зашли в Кузницу'
        return message

    def forge_pickaxe(self):
        if not self.place == 'forge_pickaxe':
            self.place = 'forge_pickaxe'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
        message = 'Стоимость крафта:\n'
        items = self.inventory.items.all()
        message = message + pickaxe_info(items)
        return message

    def tavern(self):
        if self.place == 'tavern':
            message = 'Вы уже в Таверне'
        else:
            self.place = 'tavern'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = 'Вы зашли в Таверну!\n'
        return message

    def war_menu(self):
        if self.place == 'war':
            message = 'Вы уже в меню Войны'
        else:
            self.place = 'war'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = '⚔ Меню войны ⚔\n' + \
                      'Найдите противника и разгромите его!'
        return message
