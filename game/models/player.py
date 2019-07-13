from django.db import models
from django.db.models import F, Sum

from .build import Stock
from .items import Item
from ..actions.functions import *
from ..actions.chests import *
from ..actions.tavern_alcohol import alcohol

import threading
import random
import time

# Create your models here.


class Player(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    chat_id = models.BigIntegerField(
        db_index=True,
        default=0,
        blank=True,
    )
    distribution = models.BooleanField(
        default=True,
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
    change_nickname_time = models.BigIntegerField(
        default=0,
    )
    lvl = models.IntegerField(
        default=1,
    )
    exp = models.BigIntegerField(
        default=0,
    )
    energy = models.IntegerField(
        default=30,
    )
    max_energy = models.IntegerField(
        default=30,
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
    alcohol_time = models.BigIntegerField(
        default=0,
    )
    hunt_time = models.BigIntegerField(
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
        related_name='player',
    )
    war = models.OneToOneField(
        'game.War',
        on_delete=models.SET(None),
        null=True,
        related_name='player',
    )
    inventory = models.OneToOneField(
        'game.Inventory',
        on_delete=models.SET(None),
        null=True,
        related_name='player',
    )
    cave_progress = models.OneToOneField(
        'game.CaveProgress',
        on_delete=models.SET(None),
        null=True,
        blank=True,
        related_name='player',
    )

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return self.nickname

    # Действия

    def get_stone(self, action_time, chat_info, amount=1):
        self.build.stock = self.build.get_passive(action_time)
        items = self.inventory.items.all()
        self = energy(self, action_time)

        if self.energy >= GET_ENERGY * amount:

            diamond_pickaxe = in_items(items, 'diamond_pickaxe')
            skull_pickaxe = in_items(items, 'skull_pickaxe')
            stone = 8 * amount

            if skull_pickaxe:
                stone *= 3
            elif diamond_pickaxe:
                stone *= 2

            stone = stone + random.randint(-4 * amount, 4 * amount)

            if self.build.stock.res_place('stone', stone):
                self.energy = self.energy - GET_ENERGY * amount
                self.build.stock.res_add('stone', stone)
                self = exp(self, chat_info, GET_ENERGY * amount)

                message = 'Добыто камня: ' + str(stone) + icon('stone') + '\n' + \
                          'Энергия: ' + str(self.energy) + '/' + str(self.max_energy) + icon('energy') + '\n' + \
                          'Опыт: ' + str(self.exp) + '/' + str(exp_need(self.lvl)) + icon('exp')

                self.build.stock.save(update_fields=['stone'])
                message = get_chest_mine(self, message)
            else:
                message = 'Не хватает места! (Улучшите склад)\n'

            self.save(update_fields=['energy', 'last_energy_action', 'exp', 'lvl'])
        else:
            message = 'Недостаточно энергии!'
        return message

    def get_wood(self, action_time, chat_info, amount=1):
        self.build.stock = self.build.get_passive(action_time)
        items = self.inventory.items.all()
        self = energy(self, action_time)
        if self.energy >= GET_ENERGY * amount:
            diamond_pickaxe = in_items(items, 'diamond_pickaxe')
            skull_pickaxe = in_items(items, 'skull_pickaxe')
            wood = 8 * amount

            if skull_pickaxe:
                wood *= 3
            elif diamond_pickaxe:
                wood *= 2

            wood = wood + random.randint(-4 * amount, 4 * amount)

            if self.build.stock.res_place('wood', wood):
                    self.energy = self.energy - GET_ENERGY * amount
                    self.build.stock.res_add('wood', wood)
                    self = exp(self, chat_info, GET_ENERGY * amount)

                    message = 'Добыто дерева: ' + str(wood) + icon('wood') + '\n' + \
                              'Энергия: ' + str(self.energy) + '/' + str(self.max_energy) + icon('energy') + '\n' + \
                              'Опыт: ' + str(self.exp) + '/' + str(exp_need(self.lvl)) + icon('exp')

                    self.build.stock.save(update_fields=['wood'])
            else:
                message = 'Не хватает места! (Улучшите склад)\n'

            self.save(update_fields=['energy', 'last_energy_action', 'exp', 'lvl'])
        else:
            message = 'Недостаточно энергии!'
        return message

    def get_iron(self, action_time, chat_info, amount=1):
        self.build.stock = self.build.get_passive(action_time)
        items = self.inventory.items.all()
        stone_pickaxe = in_items(items, 'stone_pickaxe')

        if stone_pickaxe:
            self = energy(self, action_time)

            if self.energy >= GET_ENERGY * amount:
                diamond_pickaxe = in_items(items, 'diamond_pickaxe')
                skull_pickaxe = in_items(items, 'skull_pickaxe')
                iron = 4 * amount

                if skull_pickaxe:
                    iron *= 3
                elif diamond_pickaxe:
                    iron *= 2

                iron = iron + random.randint(-2 * amount, 2 * amount)

                if self.build.stock.res_place('iron', iron):
                        self.energy = self.energy - GET_ENERGY * amount
                        self.build.stock.res_add('iron', iron)
                        self = exp(self, chat_info, GET_ENERGY * amount)

                        message = 'Добыто железа: ' + str(iron) + icon('iron') + '\n' + \
                                  'Энергия: ' + str(self.energy) + '/' + str(self.max_energy) + icon('energy') + '\n' + \
                                  'Опыт: ' + str(self.exp) + '/' + str(exp_need(self.lvl)) + icon('exp')

                        self.build.stock.save(update_fields=['iron'])
                        message = get_chest_mine(self, message)
                else:
                    message = 'Не хватает места! (Улучшите склад)\n'

                self.save(update_fields=['energy', 'last_energy_action', 'exp', 'lvl'])

            else:
                message = 'Недостаточно энергии!'
        else:
            message = 'Вы не можете добывать' + icon('iron') + ' Железо!\n' + \
                      'Нужна Каменная Кирка!'
        return message

    def get_diamond(self, action_time, chat_info, amount=1):
        self.build.stock = self.build.get_passive(action_time)
        items = self.inventory.items.all()
        iron_pickaxe = in_items(items, 'iron_pickaxe')
        if iron_pickaxe:
            self = energy(self, action_time)
            if self.energy >= GET_ENERGY * amount:
                diamond_pickaxe = in_items(items, 'diamond_pickaxe')
                skull_pickaxe = in_items(items, 'skull_pickaxe')
                diamond = 2 * amount

                if skull_pickaxe:
                    diamond *= 3
                elif diamond_pickaxe:
                    diamond *= 2

                diamond = diamond + random.randint(-1 * amount, 1 * amount)

                if self.build.stock.res_place('diamond', diamond):
                        self.energy = self.energy - GET_ENERGY * amount
                        self.build.stock.res_add('diamond', diamond)
                        self = exp(self, chat_info, GET_ENERGY * amount)

                        message = 'Добыто кристаллов: ' + str(diamond) + icon('diamond') + '\n' + \
                                  'Энергия: ' + str(self.energy) + '/' + str(self.max_energy) + icon('energy') + '\n' + \
                                  'Опыт: ' + str(self.exp) + '/' + str(exp_need(self.lvl)) + icon('exp')

                        self.build.stock.save(update_fields=['diamond'])
                        message = get_chest_mine(self, message)
                else:
                    message = 'Не хватает места! (Улучшите склад)\n'

                self.save(update_fields=['energy', 'last_energy_action', 'exp', 'lvl'])
            else:
                message = 'Недостаточно энергии!'
        else:
            message = 'Вы не можете добывать' + icon('diamond') + ' Кристаллы!\n' + \
                      'Нужна Железная Кирка!'
        return message

    def bonus(self, action_time):
        time = action_time - self.bonus_time
        if time > BONUS_TIME:

            bonus_k = 1 + (self.lvl // 5)
            stone = BONUS_STONE * bonus_k
            wood = BONUS_WOOD * bonus_k
            iron = BONUS_IRON * bonus_k
            diamond = BONUS_DIAMOND * bonus_k
            gold = BONUS_GOLD * bonus_k
            self.build.stock.stone += stone
            self.build.stock.wood += wood
            self.build.stock.iron += iron
            self.build.stock.diamond += diamond
            self.build.stock.gold += gold

            self.bonus_time = action_time

            self.build.stock.save(update_fields=['stone', 'wood', 'iron', 'diamond', 'gold'])
            self.save(update_fields=['bonus_time'])

            message = 'Вы получили ежедневный бонус!\n+ ' + \
                      str(stone) + icon('stone') + '\n + ' + \
                      str(wood) + icon('wood') + '\n + ' + \
                      str(iron) + icon('iron') + '\n + ' + \
                      str(diamond) + icon('diamond') + '\n + ' + \
                      str(gold) + icon('gold')
        else:
            hour = (BONUS_TIME - time) // 3600
            minutes = ((BONUS_TIME - time) - (hour * 3600)) // 60
            sec = (BONUS_TIME - time) - (minutes * 60) - (hour * 3600)
            message = 'До бонуса: ' + str(hour) + ' ч. ' + str(minutes) + ' м. ' + str(sec) + ' сек.'
        return message

    def craft_stone_pickaxe(self, action_time):
        if not self.build.forge:
            return 'Сначала постройте Кузницу!'
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
                message = 'Недостаточно камня!'
        else:
            message = 'У вас уже есть ' + item.title + '!'
        return message

    def craft_iron_pickaxe(self, action_time):
        if not self.build.forge:
            return 'Сначала постройте Кузницу!'
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
                message = 'Недостаточно железа!'
        else:
            message = 'У вас уже есть ' + item.title + '!'
        return message

    def craft_diamond_pickaxe(self, action_time):
        if not self.build.forge:
            return 'Сначала постройте Кузницу!'
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
                message = 'Недостаточно кристаллов!'
        else:
            message = 'У вас уже есть ' + item.title + '!'
        return message

    def craft_skull_pickaxe(self, action_time):
        if not self.build.forge:
            return 'Сначала постройте Кузницу!'
        self.build.stock = self.build.get_passive(action_time)
        item = in_items(self.inventory.items.all(), 'skull_pickaxe')
        if not item:
            if self.build.stock.res_check('skull', SKULL_PICKAXE):
                self.build.stock.res_remove('skull', SKULL_PICKAXE)
                pickaxe = Item.objects.get(slug='skull_pickaxe')
                self.inventory.items.add(pickaxe)
                self.build.stock.save(update_fields=['skull'])

                message = 'Поздравляю!\n' + \
                          'Вы скрафтили' + icon('skull') + ' ' + pickaxe.title + icon('skull') + ' !\n'
                effects = pickaxe.effects.all()
                for effect in effects:
                    message += effect.title + '!\n'

            else:
                message = 'Недостаточно черепов!'
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
                  'ID: ' + str(self.user_id) + '\n' + \
                  'Имя: ' + self.first_name + '\n' + \
                  'Фамилия: ' + self.last_name + '\n' + \
                  'Уровень: ' + str(self.lvl) + icon('lvl') + '\n' + \
                  'Опыт: ' + str(self.exp) + '/' + str(exp_need(self.lvl)) + icon('exp') + '\n' + \
                  'Энергия: ' + str(self.energy) + '/' + str(self.max_energy) + icon('energy')

        return message

    def go_inventory(self):
        if not self.place == 'inventory':
            self.place = 'inventory'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
        message = 'Инвентарь'
        return message

    def go_chests(self):
        message = get_chests(self)
        if not message:
            message = 'У вас нет сундуков!'
            self.place = 'inventory'
        else:
            self.place = 'chests'
        Player.objects.filter(user_id=self.user_id).update(place=self.place)
        return message

    def top(self):
        self.place = 'top'
        Player.objects.filter(user_id=self.user_id).update(place=self.place)
        message = 'Выберите топ:\n' + \
                  'По уровню 👑 - топ лвл\n' + \
                  'По зданиям 🔨 - топ здания\n' + \
                  'По успешным нападениям ⚔ - топ атака\n' + \
                  'По успешным оборонам 🛡 - топ защита\n' + \
                  'По черепам 💀 - топ череп\n' + \
                  'По золоту ✨ - топ золото\n'
        # 'По пещерам 🕸 - топ пещеры\n'
        return message

    def top_lvl(self):
        top = Player.objects.order_by('-lvl')[0:10].values_list('nickname', 'lvl', 'user_id')
        count = 1
        main_message = 'Топ игроков по Уровню 👑\n'
        for user in top:
            message = str(count) + ' | [id' + str(user[2]) + '|' + user[0] + '] - ' + str(user[1]) + ' 👑\n'
            count += 1
            main_message = main_message + message
        return main_message

    def top_skull(self):
        top = Player.objects.order_by('-build__stock__skull')[0:10].values_list('nickname', 'build__stock__skull', 'user_id')
        count = 1
        main_message = 'Топ игроков по Черепам 💀\n'
        for user in top:
            message = str(count) + ' | [id' + str(user[2]) + '|' + user[0] + '] - ' + str(user[1]) + ' 💀\n'
            count += 1
            main_message = main_message + message
        return main_message

    def top_attack(self):
        top = Player.objects.filter(lvl__gte=10).order_by('-war__success_attack')[0:10].values_list('nickname', 'war__success_attack', 'user_id')
        count = 1
        main_message = 'Топ игроков по Успешным Атакам ⚔\n'
        for user in top:
            message = str(count) + ' | [id' + str(user[2]) + '|' + user[0] + '] - ' + str(user[1]) + ' ⚔\n'
            count += 1
            main_message = main_message + message
        return main_message

    def top_defend(self):
        top = Player.objects.filter(lvl__gte=10).order_by('-war__success_defend')[0:10].values_list('nickname', 'war__success_defend', 'user_id')
        count = 1
        main_message = 'Топ игроков по Успешным Оборонам 🛡\n'
        for user in top:
            message = str(count) + ' | [id' + str(user[2]) + '|' + user[0] + '] - ' + str(user[1]) + ' 🛡\n'
            count += 1
            main_message = main_message + message
        return main_message

    def top_gold(self):
        top = Player.objects.order_by('-build__stock__gold')[0:10].values_list('nickname', 'build__stock__gold', 'user_id')
        count = 1
        main_message = 'Топ Богачей ✨\n'
        for user in top:
            message = str(count) + ' | [id' + str(user[2]) + '|' + user[0] + '] - ' + str(user[1]) + ' ✨\n'
            count += 1
            main_message = main_message + message
        return main_message

    def top_cave(self):
        top = Player.objects.filter(cave_progress__success__gt=0).order_by('-cave_progress__success')[0:10].values_list('nickname', 'cave_progress__success', 'user_id')
        count = 1
        main_message = 'Топ Исследователей 🕸\n'
        for user in top:
            message = str(count) + ' | [id' + str(user[2]) + '|' + user[0] + '] - ' + str(user[1]) + ' 🕸\n'
            count += 1
            main_message = main_message + message
        return main_message

    def top_build(self):
        build_top = Player.objects.annotate(build_point=(F('build__stock__lvl') +
                                                         F('build__market_lvl') +
                                                         F('build__wall_lvl') +
                                                         F('build__tower_lvl') +
                                                         F('build__stone_mine_lvl') +
                                                         F('build__wood_mine_lvl') +
                                                         F('build__iron_mine_lvl') +
                                                         F('build__diamond_mine_lvl'))).order_by("-build_point")[0:10]

        count = 1
        main_message = 'Топ Строителей 🔨\n'
        for user in build_top:
            message = str(count) + ' | [id' + str(user.user_id) + '|' + user.nickname + '] - ' + str(user.build_point) + ' 🔨\n'
            count += 1
            main_message = main_message + message
        return main_message

    # Строительство

    def cave_build(self):
        if not self.place == 'cave_build':
            self.place = 'cave_build'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
        if self.build.stock.lvl >= 50:
            stone_need = self.build.stock.lvl * STOCK_STONE * 3
        elif self.build.stock.lvl >= 10:
            stone_need = self.build.stock.lvl * STOCK_STONE * 2
        else:
            stone_need = self.build.stock.lvl * STOCK_STONE
        message_stock = 'Склад' + icon('stock') + ': ' + str(stone_need) + icon('stone') + '\n'
        message_forge = 'Кузница' + icon('craft') + ': ' + str(FORGE_STONE) + icon('stone') + '\n'
        message_tavern = 'Таверна' + icon('tavern') + ': ' + str(TAVERN_STONE) + icon('stone') + ' + ' + \
                         str(TAVERN_IRON) + icon('iron') + '\n'
        message_citadel = 'Цитадель' + icon('citadel') + ': ' + \
                          str(CITADEL_STONE) + icon('stone') + ' + ' + \
                          str(CITADEL_IRON) + icon('iron') + ' + ' + \
                          str(CITADEL_DIAMOND) + icon('diamond') + '\n'
        market_stone = (self.build.market_lvl + 1) * MARKET_STONE
        market_wood = (self.build.market_lvl + 1) * MARKET_WOOD
        market_iron = (self.build.market_lvl + 1) * MARKET_IRON
        market_diamond = (self.build.market_lvl + 1) * MARKET_DIAMOND
        message_market = 'Рынок: ' + \
                         str(market_stone) + icon('stone') + ' + ' + \
                         str(market_wood) + icon('wood') + ' + ' + \
                         str(market_iron) + icon('iron') + ' + ' + \
                         str(market_diamond) + icon('diamond')
        message = 'Стоимость:' + '\n'
        message = message + message_stock
        if not self.build.forge:
            message = message + message_forge
        if not self.build.tavern:
            message = message + message_tavern
        if not self.build.citadel:
            message = message + message_citadel
        if self.build.market_lvl < 10:
            message = message + message_market
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
                       str((self.build.wall_lvl + 1) * WALL_WOOD) + icon('wood')
        message = 'Стоимость:\n'
        message = message + message_tower + message_wall
        if not self.build.barracks:
            barracks = '\nКазармы: ' + str(BARRACKS_STONE) + icon('stone') + ' + ' + str(BARRACKS_IRON) + icon('iron')
            message += barracks
        if not self.build.archery:
            archery = '\nСтрельбище: ' + str(ARCHERY_STONE) + icon('stone') + ' + ' + str(ARCHERY_WOOD) + icon('wood')
            message += archery
        if not self.build.magic:
            magic = '\nБашня Магов: ' + str(MAGIC_STONE) + icon('stone') + ' + ' + str(MAGIC_WOOD) + icon('wood') + ' + ' + str(MAGIC_DIAMOND) + icon('diamond')
            message += magic
        if self.lvl >= 10:
            stone = self.build.stone_mine_lvl + 1
            wood = self.build.wood_mine_lvl + 1
            iron = self.build.iron_mine_lvl + 1
            diamond = self.build.diamond_mine_lvl + 1
            stone_mine = '\nКаменоломня: ' + str(stone * STONE_MINE_WOOD) + icon('wood') + ' + ' + \
                         str(stone * STONE_MINE_IRON) + icon('iron') + ' + ' + \
                         str(stone * STONE_MINE_DIAMOND) + icon('diamond')
            wood_mine = '\nЛесопилка: ' + str(wood * WOOD_MINE_STONE) + icon('stone') + ' + ' + \
                         str(wood * WOOD_MINE_IRON) + icon('iron') + ' + ' + \
                         str(wood * WOOD_MINE_DIAMOND) + icon('diamond')
            iron_mine = '\nРудник: ' + str(iron * IRON_MINE_WOOD) + icon('stone') + ' + ' + \
                         str(iron * IRON_MINE_WOOD) + icon('wood') + ' + ' + \
                         str(iron * IRON_MINE_DIAMOND) + icon('diamond')
            diamond_mine = '\nПрииск: ' + str(diamond * DIAMOND_MINE_STONE) + icon('stone') + ' + ' + \
                         str(diamond * DIAMOND_MINE_WOOD) + icon('wood') + ' + ' + \
                         str(diamond * DIAMOND_MINE_IRON) + icon('iron')
            message += stone_mine + wood_mine + iron_mine + diamond_mine

        return message

    # Локации

    def mine(self):
        if self.place == 'mine':
            message = 'Вы уже в Шахте'
        else:
            self.place = 'mine'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = 'Вы спустились в Шахту'
        return message

    def cave(self):
        if self.place == 'cave':
            message = 'Вы уже в Подземелье\n'
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

    def citadel(self, action_time):
        if self.place != 'citadel':
            self.place = 'citadel'
            self.save(update_fields=['place'])

        if self.war.shield > action_time:
            shield = self.war.shield - action_time
            hour = shield // 3600
            minutes = (shield - (hour * 3600)) // 60
            sec = shield - (minutes * 60) - (hour * 3600)
            shield = str(hour) + ' ч. ' + \
                     str(minutes) + ' м. ' + \
                     str(sec) + ' сек.' + icon('time')
        else:
            shield = 'У вас нет щита!'

        army_mess = '⚔ Армия:\n' + \
                    'Воины: ' + str(self.war.warrior) + icon('sword') + '\n' + \
                    'Лучники: ' + str(self.war.archer) + icon('bow') + '\n' + \
                    'Маги: ' + str(self.war.wizard) + icon('orb') + '\n' + \
                    'Всего: ' + str(self.war.sum_army()) + icon('war') + '\n'
        build_mess = '🔨 Военные здания:\n' + \
                     'Башня: +' + str(self.build.tower_lvl) + '%' + icon('war') + '\n' + \
                     'Стена: +' + str(self.build.wall_lvl) + '%' + icon('shield') + '\n'
        stat_mess = '📜 Информация:\n' + \
                    'Успешных атак: ' + str(self.war.success_attack) + icon('war') + '\n' + \
                    'Успешных оборон: ' + str(self.war.success_defend) + icon('shield') + '\n' + \
                    'Щит: ' + shield

        mess = '🏰 Цитадель 🏰\n' + 'Главный оплот вашего поселения. Здесь вы управляете армией и военными походами.\n'
        return mess + army_mess + build_mess + stat_mess

    def hunt(self, action_time):
        if self.place != 'hunt':
            self.place = 'hunt'
            self.save(update_fields=['place'])

        if self.hunt_time > action_time:
            hunt = self.hunt_time - action_time
            hour = hunt // 3600
            minutes = (hunt - (hour * 3600)) // 60
            sec = hunt - (minutes * 60) - (hour * 3600)
            hunt = 'Охота через: ' + \
                   str(hour) + ' ч. ' + \
                   str(minutes) + ' м. ' + \
                   str(sec) + ' с.' + icon('time')
        else:
            hunt = 'Выберите кого отправить:\n' + \
                   '- Охота воины\n' + \
                   '- Охота лучники\n' + \
                   '- Охота маги\n'

        mess = '🎯 Охота 🎯\n' + \
               'Охота - это всегда опасно.\n' + \
               'На охоте ваши воиска могут найти что-то полезное, ' + \
               'принести мясо животных, которое хорошо ценится на местном рынке ' + \
               'или потерять несколько бойцов из отряда!\n' + \
               'Отправлять воиска на охоту можно раз в 2 часа.\n' + hunt

        return mess

    def buy(self, action_time):
        message = 'Здесь вы можете нанять себе армию!'
        if self.place != 'army':
            self.place = 'army'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)

        self.build.get_passive(action_time)
        max_war = self.build.stock.iron // 16
        max_arch = min(self.build.stock.iron // 6, self.build.stock.wood // 20)
        max_wiz = min(self.build.stock.iron // 2, self.build.stock.wood // 12, self.build.stock.diamond // 4)

        war = '\n🗡 Воин: ' + str(WARRIOR_IRON) + '◽ ' + '(' + str(max_war) + ')'
        arch = '\n🏹 Лучник: ' + str(ARCHER_IRON) + '◽' + str(ARCHER_WOOD) + '🌲 ' + '(' + str(max_arch) + ')'
        wiz = '\n🔮 Маг: ' + str(WIZARD_IRON) + \
              '◽' + str(WIZARD_WOOD) + \
              '🌲' + str(WIZARD_DIAMOND) + '💎 ' + \
              '(' + str(max_wiz) + ')'
        if self.build.barracks or self.build.archery or self.build.magic:
            if self.build.barracks:
                message += war
            if self.build.archery:
                message += arch
            if self.build.magic:
                message += wiz
        else:
            message += '\nНет доступных воиск.\n' + \
                       'Постройте казармы/стрельбище/башню магов!'
        return message

    def forge(self):
        if not self.build.forge:
            return "Сначала постройте Кузницу!"
        if self.place == 'forge':
            message = 'Вы уже в Кузнице!\n'
        else:
            self.place = 'forge'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = 'Вы зашли в Кузницу!\n'
        info = 'Кузница открывает доступ к крафту.\n' + \
               'Команды:\n' + \
               'Кирки - Список всех кирок для крафта.\n' + \
               'Ковать [предмет] - Крафтить предмет.\n'
        message += info
        return message

    def forge_pickaxe(self):
        if self.place != 'forge_pickaxe':
            self.place = 'forge_pickaxe'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
        message = 'Стоимость крафта:\n'
        items = self.inventory.items.all()
        message = message + pickaxe_info(items)
        return message

    def tavern(self):
        if not self.build.tavern:
            return "Сначала постройте Таверну!"
        if self.place == 'tavern':
            message = 'Вы уже в Таверне!\n'
        else:
            self.place = 'tavern'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = 'Вы зашли в Таверну!\n'
        info = 'Таверна открывает доступ к игре' + icon('cube') + ' Кости' + icon('cube') + '\n' + \
               'Чтобы сыграть в' + icon('cube') + ' Кости' + icon('cube') + ' напишите команду:\n' + \
               'Кости [ресурс] [кол-во]'
        message += info
        return message

    def bones(self):
        if self.build.tavern:
            message = icon('cube') + ' Игра Кости' + icon('cube') + '\n' + \
                    'Чтобы сыграть в "Кости" напишите команду:\n' + 'Кости [ресурс] [кол-во]'
        else:
            message = "Сначала постройте Таверну!"
        return message

    def war_menu(self):
        if self.place == 'war':
            message = 'Вы уже в меню Войны'
        else:
            self.place = 'war'
            Player.objects.filter(user_id=self.user_id).update(place=self.place)
            message = '⚔ Меню войны ⚔\n' + \
                      'Найдите противника и разгромите его!\n' + \
                      'Команды:\n' + \
                      'Поиск - Поиск противника для нападения\n' + \
                      'Разведка - информация о противнике (10' + icon('diamond') + ')\n' + \
                      'Атака - Напасть на противника\n'
        return message

    def send_mess(self, message):
        try:
            send_info = {
                'user_id': self.user_id,
                'chat_id': self.user_id,
            }
            send(send_info, message)
        except:
            if self.chat_id != self.user_id:
                send_info = {
                    'user_id': self.user_id,
                    'peer_id': self.chat_id,
                    'chat_id': self.chat_id - 2000000000,
                    'nick': self.nickname,
                }
                try:
                    send(send_info, message)
                except:
                    pass

    def _send_res(self, command, action_time):
        if self.build.market_lvl == 0:
            return 'Сначала постройте Рынок!\nКоманда: Строить рынок'

        send_time = action_time - self.build.market_send_time
        send_time_cd = MARKET_SEND_TIME
        send_max = self.build.market_lvl * 50

        # Уменьшаем перезарядку с 11 уровня, 1 уровень = 5% времени
        if self.build.market_lvl > 10:
            fast_k = 1 - ((self.build.market_lvl - 10) * 0.05)
            send_time_cd = int(MARKET_SEND_TIME * fast_k)
            send_max = 500

        if send_time >= send_time_cd:

            # Проверяем ресурс
            part = command.split()
            res = {
                'дерево': 'wood',
                'камень': 'stone',
                'железо': 'iron',
                'кристаллы': 'diamond',
            }
            try:
                res = res[part[1]]
            except:
                return 'Ошибка.\nОтправить [ресурс] [кол-во] [ID-игрока]'

            # Валидация команды
            if len(part) == 4 and res and part[2].isdigit() and part[3].isdigit():

                res_type = res
                res_amount = int(part[2])
                addr_id = int(part[3])

                # Условия выхода
                if res_amount > send_max:
                    return 'Вы пытаетесь отправить слишком много ресурсов!\n' + \
                           'Рынок ' + str(self.build.market_lvl) + ' ур. - ' + \
                           str(send_max) + ' ресурса макс. за раз.'
                if self.user_id == addr_id:
                    return "Вы пытаетесь отправить ресурсы себе."

                if self.build.stock.res_check(res_type, res_amount):
                    try:
                        addr = Player.objects.get(user_id=addr_id)
                        self.build.stock.res_remove(res_type, res_amount)
                        addr.build.stock.res_add(res_type, res_amount)
                        self.build.market_send_time = action_time

                        # Сохранение
                        self.build.save(update_fields=['market_send_time'])
                        addr.build.stock.save(update_fields=[res_type])
                        self.build.stock.save(update_fields=[res_type])

                        addr_mess = self.nickname + ' прислал вам ' + str(res_amount) + icon(res_type)
                        addr.send_mess(addr_mess)
                        message = 'Отправлено ' + str(res_amount) + icon(res_type) + ' - ' + addr.nickname
                    except Player.DoesNotExist:
                        message = 'Получатель не найден!'
                else:
                    message = 'Недостаточно ресурса!'
            else:
                message = 'Ошибка.\n' + \
                          'Отправить [ресурс] [кол-во] [ID-игрока]'
        else:
            hour = (send_time_cd - send_time) // 3600
            minutes = (send_time_cd - send_time - (hour * 3600)) // 60
            sec = (send_time_cd - send_time) - (minutes * 60) - (hour * 3600)
            message = 'Отправлять ресурсы можно раз в несколько часов.\n' + \
                      'До следующей отправки: ' + str(hour) + ' ч. ' + str(minutes) + ' м. ' + str(sec) + ' сек. ⏳'

        return message

    def send_res(self, command, action_time):
        if self.build.market_lvl == 0:
            return 'Сначала постройте Рынок!\nКоманда: Строить рынок'
        time = action_time - self.build.market_send_time
        if time >= MARKET_SEND_TIME:
            part = command.split()
            res = {
                'дерево': 'wood',
                'камень': 'stone',
                'железо': 'iron',
                'кристаллы': 'diamond',
            }
            try:
                res = res[part[1]]
            except:
                return 'Ошибка.\n' + \
                       'Отправить [ресурс] [кол-во] [ID-игрока]'
            if len(part) == 4 and res and part[2].isdigit() and part[3].isdigit():
                type = res
                amount = int(part[2])
                id = int(part[3])
                if amount > self.build.market_lvl * 50:
                    return 'Вы пытаетесь отправить слишком много ресурсов!\n' + \
                           'Рынок ' + str(self.build.market_lvl) + ' ур. - ' + \
                           str(self.build.market_lvl * 50) + ' ресурса макс. за раз.'
                if self.build.stock.res_check(type, amount):
                    if self.user_id == id:
                        return "Вы пытаетесь отправить ресурсы себе."
                    try:
                        addr = Player.objects.get(user_id=id)
                        self.build.stock.res_remove(type, amount)
                        value = min(addr.build.stock.__getattribute__(type) + amount, addr.build.stock.max)
                        addr.build.stock.__setattr__(type, value)
                        self.build.market_send_time = action_time
                        self.build.save(update_fields=['market_send_time'])
                        addr.build.stock.save(update_fields=[type])
                        self.build.stock.save(update_fields=[type])

                        addr_mess = self.nickname + ' прислал вам ' + str(amount) + icon(type)
                        addr.send_mess(addr_mess)
                        message = 'Отправлено ' + str(amount) + icon(type) + ' - ' + addr.nickname
                    except Player.DoesNotExist:
                        message = 'Получатель не найден!'
                else:
                    message = 'Недостаточно ресурса!'
            else:
                message = 'Ошибка.\n' + \
                          'Отправить [ресурс] [кол-во] [ID-игрока]'
        else:
            hour = (MARKET_SEND_TIME - time) // 3600
            minutes = (MARKET_SEND_TIME - time - (hour * 3600)) // 60
            sec = (MARKET_SEND_TIME - time) - (minutes * 60) - (hour * 3600)
            message = 'Отправлять ресурсы можно раз в 4 часа.\n' + \
                      'До следующей отправки: ' + str(hour) + ' ч. ' + str(minutes) + ' м. ' + str(sec) + ' сек. ⏳'

        return message

    @staticmethod
    def give_chests(command):
        part = command.split()
        if len(part) == 4 and part[3].isdigit():
            if part[2].isdigit():
                id = int(part[2])
            else:
                id = get_id(part[2])

            slug = part[1]
            amount = int(part[3])
            try:
                addr = Player.objects.get(user_id=id)
                chest = Chest.objects.get(slug=slug)
                add_chest(addr, chest, amount)

                if addr.chat_id != 0 and addr.chat_id != addr.user_id:
                    chat_info = {
                        'user_id': addr.user_id,
                        'peer_id': addr.chat_id,
                        'chat_id': addr.chat_id - 2000000000,
                        'nick': addr.nickname,
                    }
                else:
                    chat_info = {
                        'user_id': addr.user_id,
                        'peer_id': addr.user_id,
                        'chat_id': addr.user_id,
                        'nick': addr.nickname,
                    }
                mess = 'Вам выдали ' + str(amount) + ' ' + chest.title
                try:
                    send(chat_info, mess)
                except:
                    pass

                nick = '[id' + str(addr.user_id) + '|' + addr.nickname + ']\n'
                mess = 'Выдано: ' + str(amount) + ' ' + chest.title + ' для ' + nick

                return mess
            except Player.DoesNotExist:
                return "Игрок не найден!"
            except Chest.DoesNotExist:
                return "Сундук не найден!"
        return "Ошибка"

    @staticmethod
    def give_skull(command):
        part = command.split()
        if len(part) == 4 and part[1] == 'skull' and part[3].isdigit():
            if part[2].isdigit():
                id = int(part[2])
            else:
                id = get_id(part[2])

            amount = int(part[3])
            try:
                player = Player.objects.filter(user_id=id).select_related('build__stock').get()
                player.build.stock.skull += amount
                player.build.stock.save(update_fields=['skull'])

                if player.chat_id != 0 and player.chat_id != player.user_id:
                    chat_info = {
                        'user_id': player.user_id,
                        'peer_id': player.chat_id,
                        'chat_id': player.chat_id - 2000000000,
                        'nick': player.nickname,
                    }
                else:
                    chat_info = {
                        'user_id': player.user_id,
                        'peer_id': player.user_id,
                        'chat_id': player.user_id,
                        'nick': player.nickname,
                    }
                
                mess = 'Вам выдано ' + str(amount) + ' 💀 за поддержку проекта!'
                try:
                    send(chat_info, mess)
                except:
                    pass

                nick = '[id' + str(player.user_id) + '|' + player.nickname + ']\n'
                mess = 'Выдано: ' + str(amount) + ' 💀 для ' + nick

                return mess
            except Player.DoesNotExist:
                return "Игрок не найден!"

    def change_nickname(self, nick, action_time):
        if action_time < self.change_nickname_time:
            nick_time = self.change_nickname_time - action_time
            sec = nick_time
            minutes = sec // 60
            hour = minutes // 60
            day = hour // 24
            message = 'Изменять ник можно раз в 10 дней.\n' + \
                      'До следующего раза: ' + str(day) + ' дней ' + \
                      str(hour % 24) + ' ч. ' + \
                      str(minutes % 60) + ' м. ' + \
                      str(sec % 60) + ' сек. ⏳'
            return message
        if Player.objects.filter(nickname=nick).exists():
            return "Ник занят!"
        elif len(nick) > 30:
            return "Ник слишком длинный!"
        else:
            self.change_nickname_time = action_time + NICKNAME_TIME
            self.nickname = nick
            self.save(update_fields=['nickname', 'change_nickname_time'])
            return 'Ваш ник - ' + self.nickname + \
                   '\n Напишите "ник" или "ник время", чтобы узнать когда можно будет сменить ник!'

    def check_change_nickname_time(self, action_time):
        if action_time < self.change_nickname_time:
            nick_time = self.change_nickname_time - action_time
            sec = nick_time
            minutes = sec // 60
            hour = minutes // 60
            day = hour // 24
            message = 'Время до смены ника:\n' + \
                      str(day) + ' дней ' + \
                      str(hour % 24) + ' ч. ' + \
                      str(minutes % 60) + ' м. ' + \
                      str(sec % 60) + ' сек. ⏳'
            return message
        else:
            return "Вы можете сменить ник!\nНик [Новый ник]"

    def alcohol(self, chat_info, action_time):

        if chat_info['user_id'] == chat_info['peer_id']:
            return "Можно использовать только в беседах!"

        if self.build.stock.res_check('gold', 500):

            if self.alcohol_time > action_time:
                alco = (
                    'Ты сильно пьян!',
                    'Ты еле стоишь...',
                    'Еще один кубок? Ты еле стоишь...',
                    'Тебе хватит на сегодня...',
                )
                tavern_owner = random.choice(alco)
                return 'Хозяин Таверны: "' + tavern_owner + '"'

            self.build.stock.res_remove('gold', 500)
            self.build.stock.save(update_fields=['gold'])

            vk = vk_connect()
            users = vk.messages.getConversationMembers(
                access_token=token(),
                peer_id=str(chat_info['peer_id']),
                group_id='176853872',
            )

            user_ids = [user['member_id'] for user in users['items']]

            alcohol_time = action_time + random.randint(180, 600)

            Player.objects.filter(user_id__in=user_ids).update(alcohol_time=alcohol_time, energy=F('energy')+10)

            threading.Thread(target=alcohol, args=(vk, self, user_ids, chat_info['peer_id'])).start()

            all_el = (
                'Тащите лучшую бочку хмельного!',
                'У меня как раз есть бочка прекрасного эля!',
                'Бочку эля!',
                'Несите бочку лучшего эля!',
                'Всем лучшего эля в кубки!',
            )
            tavern_owner = random.choice(all_el)
            mess = 'Хозяин Таверны: "' + tavern_owner + '"'

        else:
            need_gold = (
                'Заработай больше золота и приходи...',
                'Даже не пытайся, только опозоришься...',
                'Все знают что твой карман пуст...',
                'Сыграй лучше в кости на свои гроши, может там тебе повезет...',
            )
            tavern_owner = random.choice(need_gold)
            mess = 'Хозяин Таверны: "' + tavern_owner + '"'

        return mess

    def alcohol_mess(self, action_time, mess):

        if self.alcohol_time > action_time:
            rand = random.randint(0, 1)

            if rand:
                parts = mess.split('\n')
                mess = ''

                for mess_str in parts:
                    mess += mess_str[::-1] + '\n'

            else:
                mess = list(mess)
                rand_max = len(mess) - 1

                for i in range(5):
                    first = random.randint(0, rand_max)
                    second = random.randint(0, rand_max)
                    mess[first], mess[second] = mess[second], mess[first]

                mess = "".join(mess)

            mess += "\nВы пьяны!"
        return mess

    def hunting_war(self, action_time):
        if self.war.warrior < 1:
            return "У вас нет воинов для охоты!"

        if self.hunt_time > action_time:
            hunt = self.hunt_time - action_time
            hour = hunt // 3600
            minutes = (hunt - (hour * 3600)) // 60
            sec = hunt - (minutes * 60) - (hour * 3600)
            mess = 'Охота через: ' + \
                   str(hour) + ' ч. ' + \
                   str(minutes) + ' м. ' + \
                   str(sec) + ' с.' + icon('time')
            return mess

        mess = ''
        rand = random.randint(0, 100)
        if 0 <= rand < 20:
            # Большая добыча
            reward = self.war.warrior // 2
            mess = 'Ваши воины смогли выследить и завалить большое стадо бизонов!\n' + \
                   'Они принесли много мяса!\n' + \
                   'С продажи мяса вы получили ' + str(reward) + icon('gold')
            self.build.stock.gold += reward
            self.build.stock.save(update_fields=['gold'])
        elif 20 <= rand < 40:
            # Средняя добыча
            reward = self.war.warrior // 4
            mess = 'Ваши воины решили что смогут догнать антилоп, частично у них получилось!\n' + \
                   'Они принесли среднее кол-во мяса!\n' + \
                   'С продажи мяса вы получили ' + str(reward) + icon('gold')
            self.build.stock.gold += reward
            self.build.stock.save(update_fields=['gold'])
        elif 40 <= rand < 60:
            # Маленькая добыча
            reward = self.war.warrior // 6
            mess = 'Один не совсем умный боец предложил охотиться на белок, и все его поддержали... \n' + \
                   'Они принесли мало мяса... \n' + \
                   'С продажи мяса вы получили ' + str(reward) + icon('gold')
            self.build.stock.gold += reward
            self.build.stock.save(update_fields=['gold'])
        elif 60 <= rand < 80:
            # Нет добычи
            mess = 'Ваши воины наткнулись на стаю волков. \n' + \
                   'К счастью волки не смогли прокусить их доспехи. \n' + \
                   'Зато утащили всю добычу!\n' + \
                   'Воины вернулись ни с чем...'
        elif 80 <= rand < 90:
            # Потери
            die = 1 + (self.war.warrior // 10)
            mess = 'Отряд воинов наткнулся на логово медведей. ' + \
                   'Часть отряда была разорвана вместе с доспехами.' + \
                   '\nПотери: ' + str(die) + icon('sword')
            self.war.warrior -= die
            self.war.save(update_fields=['warrior'])
        elif 90 <= rand <= 100:
            # Алтарь
            skull = 2 + (self.war.warrior // 100)
            die = 1 + (self.war.warrior // 10)
            skull = skull // 2

            mess = 'Ваши воины нашли 💀 Древний Алтарь 💀\n' + \
                   'Не долго думая, они решили вынести все накопленные черепа, чем разгневали Хранителя Подземелья. \n' + \
                   'Часть ваших воинов пополнила коллекцию черепов...\n' + \
                   'Некоторым удалось прихватить череп и выжить!' + \
                   '\nДобыто: ' + str(skull) + icon('skull') + \
                   '\nПотери: ' + str(die) + icon('sword')

            self.war.warrior -= die
            self.war.save(update_fields=['warrior'])
            self.build.stock.skull += skull
            self.build.stock.save(update_fields=['skull'])

        self.hunt_time = action_time + 7200
        self.save(update_fields=['hunt_time'])
        return mess

    def hunting_arch(self, action_time):
        if self.war.archer < 1:
            return "У вас нет лучников для охоты!"

        if self.hunt_time > action_time:
            hunt = self.hunt_time - action_time
            hour = hunt // 3600
            minutes = (hunt - (hour * 3600)) // 60
            sec = hunt - (minutes * 60) - (hour * 3600)
            mess = 'Охота через: ' + \
                   str(hour) + ' ч. ' + \
                   str(minutes) + ' м. ' + \
                   str(sec) + ' с.' + icon('time')
            return mess

        mess = ''
        rand = random.randint(0, 100)
        if 0 <= rand < 20:
            # Большая добыча
            reward = self.war.archer // 2
            mess = 'Ваши лучники отлично стреляют!\n' + \
                   'Они принесли много мяса!\n' + \
                   'С продажи мяса вы получили ' + str(reward) + icon('gold')
            self.build.stock.gold += reward
            self.build.stock.save(update_fields=['gold'])
        elif 20 <= rand < 40:
            # Средняя добыча
            reward = self.war.archer // 4
            mess = 'Подстрелив несколько антилоп, ваши лучники решили, что этого достаточно. \n' + \
                   'И устроили турнир, кто собьёт больше яблок с деревьев. \n' + \
                   'Они принесли среднее кол-во мяса!\n' + \
                   'С продажи мяса вы получили ' + str(reward) + icon('gold')
            self.build.stock.gold += reward
            self.build.stock.save(update_fields=['gold'])
        elif 40 <= rand < 60:
            # Маленькая добыча
            reward = self.war.archer // 6
            mess = 'Ваши лучники начали соревноваться в стрельбе по птицам и забыли про охоту... \n' + \
                   'Они принесли мало мяса... \n' + \
                   'С продажи мяса вы получили ' + str(reward) + icon('gold')
            self.build.stock.gold += reward
            self.build.stock.save(update_fields=['gold'])
        elif 60 <= rand < 80:
            # Нет добычи
            mess = 'Ваши лучники нашли большое стадо буйволов... \n' + \
                   'Как оказалось, буйволам не нравится когда в них летят стрелы. \n' + \
                   'А лучники очень быстро бегают...\n' + \
                   'Они вернулись ни с чем...'
        elif 80 <= rand < 90:
            # Потери
            die = self.war.archer // 10
            mess = 'Ваши лучники нашли пещеру и решили изучить её.\n' + \
                   'Выжившие помнят только крики...' + \
                   '\nПотери: ' + str(die) + icon('bow')
            self.war.archer -= die
            self.war.save(update_fields=['archer'])
        elif 90 <= rand <= 100:
            # Алтарь
            skull = 2 + (self.war.archer // 100)
            die = 1 + (self.war.archer // 20)

            mess = 'Ваши лучники нашли 💀 Древний Алтарь 💀\n' + \
                   'При помощи стрел и веревок они решили достать черепа с алтаря, чем разгневали Хранителя Подземелья. \n' + \
                   'Часть ваших лучников подошла слишком близко и пополнила коллекцию черепов... \n' + \
                   'Хорошо, что у лучников нет тяжелых доспехов!\n' + \
                   '\nДобыто: ' + str(skull) + icon('skull') + \
                   '\nПотери: ' + str(die) + icon('bow')

            self.war.archer -= die
            self.war.save(update_fields=['archer'])
            self.build.stock.skull += skull
            self.build.stock.save(update_fields=['skull'])

        self.hunt_time = action_time + 7200
        self.save(update_fields=['hunt_time'])
        return mess

    def hunting_wiz(self, action_time):
        if self.war.wizard < 1:
            return "У вас нет магов для охоты!"

        if self.hunt_time > action_time:
            hunt = self.hunt_time - action_time
            hour = hunt // 3600
            minutes = (hunt - (hour * 3600)) // 60
            sec = hunt - (minutes * 60) - (hour * 3600)
            mess = 'Охота через: ' + \
                   str(hour) + ' ч. ' + \
                   str(minutes) + ' м. ' + \
                   str(sec) + ' с.' + icon('time')
            return mess

        mess = ''
        rand = random.randint(0, 100)
        if 0 <= rand < 20:
            # Большая добыча
            reward = self.war.wizard // 2
            mess = 'Ваши маги нашли много разных животных и доставили их в замороженном виде! \n' + \
                   'Они принесли много мяса! \n' + \
                   'С продажи мяса вы получили ' + str(reward) + icon('gold')
            self.build.stock.gold += reward
            self.build.stock.save(update_fields=['gold'])
        elif 20 <= rand < 40:
            # Средняя добыча
            reward = self.war.wizard // 4
            mess = 'Бизоны или буйволы? Не проблема! \n' + \
                   'Увы, часть мяса сгорела от огненных заклинаний. \n' + \
                   'Они принесли среднее кол-во мяса!\n' + \
                   'С продажи мяса вы получили ' + str(reward) + icon('gold')
            self.build.stock.gold += reward
            self.build.stock.save(update_fields=['gold'])
        elif 40 <= rand < 60:
            # Маленькая добыча
            reward = self.war.wizard // 6
            mess = 'Маги достаточно ленивы, чтобы бегать за живностью по полям и лесам... \n' + \
                   'Они принесли мало мяса... \n' + \
                   'С продажи мяса вы получили ' + str(reward) + icon('gold')
            self.build.stock.gold += reward
            self.build.stock.save(update_fields=['gold'])
        elif 60 <= rand < 80:
            # Нет добычи
            mess = 'Нет ничего лучше медитации! \n' + \
                   'Ваши маги достигли ясности разума, но забыли зачем пошли... \n' + \
                   'Они вернулись ни с чем...'
        elif 80 <= rand < 90:
            # Потери
            die = 1 + (self.war.wizard // 10)
            mess = 'Вы знали, что магия сильно влияет на природу? \n' + \
                   'Очередное заклинание спровоцировало появление каменного голема... \n' + \
                   'Теперь в мире гуляет голем украшенный магическими мантиями...' + \
                   '\nПотери: ' + str(die) + icon('orb')
            self.war.wizard -= die
            self.war.save(update_fields=['wizard'])
        elif 90 <= rand <= 100:
            # Алтарь

            mess = 'Ваши маги нашли 💀 Древний Алтарь 💀\n' + \
                   'Согласно мудрости наставника: "Не трожь то, что старше тебя", алтарь остался нетронутым... \n' + \
                   'Маги вернулись ни с чем, но живые!'

        self.hunt_time = action_time + 7200
        self.save(update_fields=['hunt_time'])
        return mess

