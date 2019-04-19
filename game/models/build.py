from django.db import models

from ..actions.constant import *

from ..actions.functions import *


class Stock(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    lvl = models.IntegerField(
        default=1,
    )
    max = models.IntegerField(
        default=60,
    )
    # Materials
    wood = models.IntegerField(
        default=0,
    )
    stone = models.IntegerField(
        default=0,
    )
    diamond = models.IntegerField(
        default=0
    )
    iron = models.IntegerField(
        default=0,
    )
    gold = models.IntegerField(
        default=0,
    )
    skull = models.IntegerField(
        default=0,
    )
    get_passive_last_time = models.BigIntegerField(
        default=0,
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def stock(self, build, action_time):
        self = build.get_passive(action_time)
        message = 'Склад - ' + str(self.lvl) + ' ур.' + '\n' + \
                  'Камень: ' + str(self.stone) + '/' + str(self.max) + icon('stone') + '\n' + \
                  'Дерево: ' + str(self.wood) + '/' + str(self.max) + icon('wood') + '\n' + \
                  'Железо: ' + str(self.iron) + '/' + str(self.max) + icon('iron') + '\n' + \
                  'Кристаллы: ' + str(self.diamond) + '/' + str(self.max) + icon('diamond') + '\n' + \
                  'Золото: ' + str(self.gold) + '/' + str(self.max) + icon('gold') + '\n' + \
                  'Черепа: ' + str(self.skull) + icon('skull')

        return message


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
    citadel = models.BooleanField(
        default=False,
    )
    tower_lvl = models.IntegerField(
        default=0,
    )
    wall_lvl = models.IntegerField(
        default=0,
    )
    stone_mine_lvl = models.IntegerField(
        default=0,
    )
    wood_mine_lvl = models.IntegerField(
        default=0,
    )
    iron_mine_lvl = models.IntegerField(
        default=0,
    )
    diamond_mine_lvl = models.IntegerField(
        default=0,
    )
    altar = models.BooleanField(
        default=False,
    )
    exchange = models.BooleanField(
        default=False,
    )
    barracks = models.BooleanField(
        default=False,
    )
    archery = models.BooleanField(
        default=False,
    )
    magic = models.BooleanField(
        default=False,
    )
    stock = models.OneToOneField(
        Stock,
        on_delete=models.SET(None),
        null=True,
    )

    class Meta:
        verbose_name = 'Здание'
        verbose_name_plural = 'Здания'

    def get_passive(self, action_time):
        delta = action_time - self.stock.get_passive_last_time
        delta = delta // 3600
        if delta >= 1:
            print(delta)
            if self.wood_mine_lvl > 0:
                wood = delta * (GET_PASSIVE_WOOD + GET_PASSIVE_WOOD_X * self.wood_mine_lvl) // 24
                wood_sum = wood + self.stock.wood
                self.stock.wood = min(wood_sum, self.stock.max)
            if self.stone_mine_lvl > 0:
                stone = delta * (GET_PASSIVE_STONE + GET_PASSIVE_STONE_X * self.stone_mine_lvl) // 24
                stone_sum = stone + self.stock.stone
                self.stock.stone = min(stone_sum, self.stock.max)
            if self.iron_mine_lvl > 0:
                iron = delta * (GET_PASSIVE_IRON + GET_PASSIVE_IRON_X * self.iron_mine_lvl) // 24
                iron_sum = iron + self.stock.iron
                self.stock.iron = min(iron_sum, self.stock.max)
            if self.diamond_mine_lvl > 0:
                diamond = delta * (GET_PASSIVE_DIAMOND + GET_PASSIVE_DIAMOND_X * self.diamond_mine_lvl) // 24
                diamond_sum = diamond + self.stock.diamond
                self.stock.diamond = min(diamond_sum, self.stock.max)
            self.stock.get_passive_last_time = self.stock.get_passive_last_time + (delta * 3600)
            Stock.objects.filter(user_id=self.user_id).update(wood=self.stock.wood,
                                                              stone=self.stock.stone,
                                                              iron=self.stock.iron,
                                                              diamond=self.stock.diamond,
                                                              get_passive_last_time=self.stock.get_passive_last_time)
        return self.stock

    def build_stock(self, action_time):
        self.stock = self.get_passive(action_time)
        if self.stock.lvl >= 10:
            stone_need = self.stock.lvl * STOCK_STONE * 2
        else:
            stone_need = self.stock.lvl * STOCK_STONE
        if self.stock.stone >= stone_need:
            self.stock.stone = self.stock.stone - stone_need
            self.stock.lvl = self.stock.lvl + 1
            self.stock.max = self.stock.lvl * STOCK_MAX_X
            Stock.objects.filter(user_id=self.user_id).update(stone=self.stock.stone,
                                                              lvl=self.stock.lvl,
                                                              max=self.stock.max)
            message = 'Склад улучшен! (' + str(self.stock.lvl) + ' ур.)'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                      'Нужно:\n' + \
                      'Камня: ' + str(stone_need) + icon('stone')
        return message

    # TODO Проверки на уровень для постройки зданий в соответствии с балансом

    def build_forge(self, action_time):
        self.stock = self.get_passive(action_time)
        if not self.forge:
            if self.stock.stone >= FORGE_STONE:
                self.stock.stone = self.stock.stone - FORGE_STONE
                self.forge = True
                Build.objects.filter(user_id=self.user_id).update(forge=self.forge)
                Stock.objects.filter(user_id=self.user_id).update(stone=self.stock.stone)
                message = 'Кузница построена'
            else:
                message = 'Недостаточно ресурсов! \n' + \
                          'Нужно:\n' + \
                          'Камня: ' + str(FORGE_STONE) + icon('stone')
        else:
            message = 'У вас уже есть Кузница'
        return message

    def build_tavern(self, action_time):
        self.stock = self.get_passive(action_time)
        if not self.tavern:
            if self.stock.stone >= TAVERN_STONE \
                    and self.stock.iron >= TAVERN_IRON:
                self.stock.stone = self.stock.stone - TAVERN_STONE
                self.stock.iron = self.stock.iron - TAVERN_IRON
                self.tavern = True
                Stock.objects.filter(user_id=self.user_id).update(stone=self.stock.stone,
                                                                  iron=self.stock.iron)
                Build.objects.filter(user_id=self.user_id).update(tavern=self.tavern)
                message = 'Таверна построена'
            else:
                message = 'Недостаточно ресурсов! \n' + \
                          'Нужно:\n' + \
                          'Камня: ' + str(TAVERN_STONE) + icon('stone') + '\n' + \
                          'Железо: ' + str(TAVERN_IRON) + icon('iron')
        else:
            message = 'У вас уже есть Таверна'
        return message

    def build_citadel(self, action_time):
        self.stock = self.get_passive(action_time)
        if not self.citadel:
            if self.stock.stone >= CITADEL_STONE \
                    and self.stock.iron >= CITADEL_IRON \
                    and self.stock.diamond >= CITADEL_DIAMOND:
                self.stock.stone = self.stock.stone - CITADEL_STONE
                self.stock.iron = self.stock.iron - CITADEL_IRON
                self.stock.diamond = self.stock.diamond - CITADEL_DIAMOND
                self.citadel = True
                Build.objects.filter(user_id=self.user_id).update(citadel=self.citadel)
                Stock.objects.filter(user_id=self.user_id).update(stone=self.stock.stone,
                                                                  iron=self.stock.iron,
                                                                  diamond=self.stock.diamond)
                message = 'Цитадель построена!'
            else:
                message = 'Недостаточно ресурсов! \n' + \
                          'Нужно:\n' + \
                          'Камня: ' + str(CITADEL_STONE) + icon('stone') + '\n' + \
                          'Железо: ' + str(CITADEL_IRON) + icon('iron') + '\n' + \
                          'Кристаллы: ' + str(CITADEL_DIAMOND) + icon('diamond')
        else:
            message = 'У вас уже есть Цитадель'
        return message

    def build_tower(self, action_time):
        self.stock = self.get_passive(action_time)
        if self.citadel:
            need_stone = (self.tower_lvl + 1) * TOWER_STONE
            need_wood = (self.tower_lvl + 1) * TOWER_WOOD
            if self.stock.stone >= need_stone \
                    and self.stock.wood >= need_wood:
                self.stock.stone = self.stock.stone - need_stone
                self.stock.wood = self.stock.wood - need_wood
                self.tower_lvl = self.tower_lvl + 1
                Build.objects.filter(user_id=self.user_id).update(tower_lvl=self.tower_lvl)
                Stock.objects.filter(user_id=self.user_id).update(wood=self.stock.wood,
                                                                  stone=self.stock.stone)
                message = 'Башня улучшена! (' + str(self.tower_lvl) + ' ур.)'
            else:
                message = 'Недостаточно ресурсов! \n' + \
                          'Нужно:\n' + \
                          'Камня: ' + str(need_stone) + icon('stone') + '\n' + \
                          'Дерева: ' + str(need_wood) + icon('wood')
        else:
            message = "Сначала постройте Цитадель!"
        return message

    def build_wall(self, action_time):
        self.stock = self.get_passive(action_time)
        if self.citadel:
            need_stone = (self.wall_lvl + 1) * WALL_STONE
            need_wood = (self.wall_lvl + 1) * WALL_WOOD
            if self.stock.stone >= need_stone \
                    and self.stock.wood >= need_wood:
                self.stock.stone = self.stock.stone - need_stone
                self.stock.wood = self.stock.wood - need_wood
                self.wall_lvl = self.wall_lvl + 1
                Build.objects.filter(user_id=self.user_id).update(wall_lvl=self.wall_lvl)
                Stock.objects.filter(user_id=self.user_id).update(wood=self.stock.wood,
                                                                  stone=self.stock.stone)
                message = 'Стена улучшена! (' + str(self.wall_lvl) + ' ур.)'
            else:
                message = 'Недостаточно ресурсов! \n' + \
                          'Нужно:\n' + \
                          'Камня: ' + str(need_stone) + icon('stone') + '\n' + \
                          'Дерева: ' + str(need_wood) + icon('wood')
        else:
            message = "Сначала постройте Цитадель!"
        return message

    def build_barracks(self, action_time):
        self.stock = self.get_passive(action_time)
        if self.citadel:
            if not self.barracks:
                if self.stock.stone >= BARRACKS_STONE \
                        and self.stock.iron >= BARRACKS_IRON:
                    self.stock.stone = self.stock.stone - BARRACKS_STONE
                    self.stock.iron = self.stock.iron - BARRACKS_IRON
                    self.barracks = True
                    Build.objects.filter(user_id=self.user_id).update(barracks=self.barracks)
                    Stock.objects.filter(user_id=self.user_id).update(stone=self.stock.stone,
                                                                      iron=self.stock.iron)
                    message = 'Казармы построены!'
                else:
                    message = 'Недостаточно ресурсов! \n' + \
                              'Нужно:\n' + \
                              'Камня: ' + str(BARRACKS_STONE) + icon('stone') + '\n' + \
                              'Железа: ' + str(BARRACKS_IRON) + icon('iron')
            else:
                message = "У вас уже есть Казармы!"
        else:
            message = "Сначала постройте Цитадель!"
        return message

    def build_archery(self, action_time):
        self.stock = self.get_passive(action_time)
        if self.citadel:
            if not self.archery:
                if self.stock.stone >= ARCHERY_STONE \
                        and self.stock.wood >= ARCHERY_WOOD:
                    self.stock.stone = self.stock.stone - ARCHERY_STONE
                    self.stock.wood = self.stock.wood - ARCHERY_WOOD
                    self.archery = True
                    Build.objects.filter(user_id=self.user_id).update(archery=self.archery)
                    Stock.objects.filter(user_id=self.user_id).update(stone=self.stock.stone,
                                                                      wood=self.stock.wood)
                    message = 'Стрельбище построено!'
                else:
                    message = 'Недостаточно ресурсов! \n' + \
                              'Нужно:\n' + \
                              'Камня: ' + str(ARCHERY_STONE) + icon('stone') + '\n' + \
                              'Дерева: ' + str(ARCHERY_WOOD) + icon('wood')
            else:
                message = "У вас уже есть Стрельбище!"
        else:
            message = "Сначала постройте Цитадель!"
        return message

    def build_magic(self, action_time):
        self.stock = self.get_passive(action_time)
        if self.citadel:
            if not self.magic:
                if self.stock.stone >= MAGIC_STONE \
                        and self.stock.wood >= MAGIC_WOOD \
                        and self.stock.diamond >= MAGIC_DIAMOND:
                    self.stock.stone = self.stock.stone - MAGIC_STONE
                    self.stock.wood = self.stock.wood - MAGIC_WOOD
                    self.stock.diamond = self.stock.diamond - MAGIC_DIAMOND
                    self.magic = True
                    Build.objects.filter(user_id=self.user_id).update(magic=self.magic)
                    Stock.objects.filter(user_id=self.user_id).update(stone=self.stock.stone,
                                                                      wood=self.stock.wood,
                                                                      diamond=self.stock.diamond)
                    message = 'Башня Магов построена!'
                else:
                    message = 'Недостаточно ресурсов! \n' + \
                              'Нужно:\n' + \
                              'Камня: ' + str(MAGIC_STONE) + icon('stone') + '\n' + \
                              'Дерева: ' + str(MAGIC_WOOD) + icon('wood') + '\n' + \
                              'Кристаллов: ' + str(MAGIC_DIAMOND) + icon('diamond')
            else:
                message = "У вас уже есть Башня Магов!"
        else:
            message = "Сначала постройте Цитадель!"
        return message

    def build_stone_mine(self, action_time, lvl):
        if lvl < 10:
            message = 'Строительство Каменоломни доступно с 10 ур.'
            return message
        self.stock = self.get_passive(action_time)
        need_wood = (self.stone_mine_lvl + 1) * STONE_MINE_WOOD
        need_iron = (self.stone_mine_lvl + 1) * STONE_MINE_IRON
        need_diamond = (self.stone_mine_lvl + 1) * STONE_MINE_DIAMOND
        if self.stock.wood >= need_wood \
                and self.stock.iron >= need_iron \
                and self.stock.diamond >= need_diamond:
            self.stock.wood = self.stock.wood - need_wood
            self.stock.iron = self.stock.iron - need_iron
            self.stock.diamond = self.stock.diamond - need_diamond
            self.stone_mine_lvl = self.stone_mine_lvl + 1
            Build.objects.filter(user_id=self.user_id).update(stone_mine_lvl=self.stone_mine_lvl)
            Stock.objects.filter(user_id=self.user_id).update(wood=self.stock.wood,
                                                              iron=self.stock.iron,
                                                              diamond=self.stock.diamond)
            message = 'Каменоломня улучшена! (' + str(self.stone_mine_lvl) + ' ур.)'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                              'Нужно:\n' + \
                              'Дерева: ' + str(need_wood) + icon('wood') + '\n' + \
                              'Железа: ' + str(need_iron) + icon('iron') + '\n' + \
                              'Кристаллов: ' + str(need_diamond) + icon('diamond')
        return message

    def build_wood_mine(self, action_time, lvl):
        if lvl < 10:
            message = 'Строительство Лесопилки доступно с 10 ур.'
            return message
        self.stock = self.get_passive(action_time)
        need_stone = (self.wood_mine_lvl + 1) * WOOD_MINE_STONE
        need_iron = (self.wood_mine_lvl + 1) * WOOD_MINE_IRON
        need_diamond = (self.wood_mine_lvl + 1) * WOOD_MINE_DIAMOND
        if self.stock.stone >= need_stone \
                and self.stock.iron >= need_iron \
                and self.stock.diamond >= need_diamond:
            self.stock.stone = self.stock.stone - need_stone
            self.stock.iron = self.stock.iron - need_iron
            self.stock.diamond = self.stock.diamond - need_diamond
            self.wood_mine_lvl = self.wood_mine_lvl + 1
            Build.objects.filter(user_id=self.user_id).update(wood_mine_lvl=self.wood_mine_lvl)
            Stock.objects.filter(user_id=self.user_id).update(stone=self.stock.stone,
                                                              iron=self.stock.iron,
                                                              diamond=self.stock.diamond)
            message = 'Лесопилка улучшена! (' + str(self.wood_mine_lvl) + ' ур.)'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                              'Нужно:\n' + \
                              'Камня: ' + str(need_stone) + icon('stone') + '\n' + \
                              'Железа: ' + str(need_iron) + icon('iron') + '\n' + \
                              'Кристаллов: ' + str(need_diamond) + icon('diamond')
        return message

    def build_iron_mine(self, action_time, lvl):
        if lvl < 10:
            message = 'Строительство Рудника доступно с 10 ур.'
            return message
        self.stock = self.get_passive(action_time)
        need_stone = (self.iron_mine_lvl + 1) * IRON_MINE_STONE
        need_wood = (self.iron_mine_lvl + 1) * IRON_MINE_WOOD
        need_diamond = (self.iron_mine_lvl + 1) * IRON_MINE_DIAMOND
        if self.stock.stone >= need_stone \
                and self.stock.wood >= need_wood \
                and self.stock.diamond >= need_diamond:
            self.stock.stone = self.stock.stone - need_stone
            self.stock.wood = self.stock.wood - need_wood
            self.stock.diamond = self.stock.diamond - need_diamond
            self.iron_mine_lvl = self.iron_mine_lvl + 1
            Build.objects.filter(user_id=self.user_id).update(iron_mine_lvl=self.iron_mine_lvl)
            Stock.objects.filter(user_id=self.user_id).update(stone=self.stock.stone,
                                                              wood=self.stock.wood,
                                                              diamond=self.stock.diamond)
            message = 'Рудник улучшен! (' + str(self.iron_mine_lvl) + ' ур.)'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                              'Нужно:\n' + \
                              'Камня: ' + str(need_stone) + icon('stone') + '\n' + \
                              'Дерева: ' + str(need_wood) + icon('wood') + '\n' + \
                              'Кристаллов: ' + str(need_diamond) + icon('diamond')
        return message

    def build_diamond_mine(self, action_time, lvl):
        if lvl < 10:
            message = 'Строительство Прииска доступно с 10 ур.'
            return message
        self.stock = self.get_passive(action_time)
        need_stone = (self.diamond_mine_lvl + 1) * DIAMOND_MINE_STONE
        need_wood = (self.diamond_mine_lvl + 1) * DIAMOND_MINE_WOOD
        need_iron = (self.diamond_mine_lvl + 1) * DIAMOND_MINE_IRON
        if self.stock.stone >= need_stone \
                and self.stock.wood >= need_wood \
                and self.stock.iron >= need_iron:
            self.stock.stone = self.stock.stone - need_stone
            self.stock.wood = self.stock.wood - need_wood
            self.stock.iron = self.stock.iron - need_iron
            self.diamond_mine_lvl = self.diamond_mine_lvl + 1
            Build.objects.filter(user_id=self.user_id).update(diamond_mine_lvl=self.diamond_mine_lvl)
            Stock.objects.filter(user_id=self.user_id).update(stone=self.stock.stone,
                                                              wood=self.stock.wood,
                                                              iron=self.stock.iron)
            message = 'Прииск улучшен! (' + str(self.diamond_mine_lvl) + ' ур.)'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                              'Нужно:\n' + \
                              'Камня: ' + str(need_stone) + icon('stone') + '\n' + \
                              'Дерева: ' + str(need_wood) + icon('wood') + '\n' + \
                              'Железа: ' + str(need_iron) + icon('iron')
        return message

    def build_info(self):
        message = 'Сначала постройте Цитадель!'
        if self.citadel:
            stone_passive = (GET_PASSIVE_STONE + (GET_PASSIVE_STONE_X * self.stone_mine_lvl)) // 24
            wood_passive = (GET_PASSIVE_WOOD + (GET_PASSIVE_WOOD_X * self.wood_mine_lvl)) // 24
            iron_passive = (GET_PASSIVE_IRON + (GET_PASSIVE_IRON_X * self.iron_mine_lvl)) // 24
            diamond_passive = (GET_PASSIVE_DIAMOND + (GET_PASSIVE_DIAMOND_X * self.diamond_mine_lvl)) // 24
            message = 'Башня ' + str(self.tower_lvl) + ' ур.: +' + str(self.tower_lvl) + '%' + icon('war') + '\n' \
                      'Стена ' + str(self.wall_lvl) + ' ур.: +' + str(self.wall_lvl) + '%' + icon('shield') + '\n' + \
                      'Каменоломня ' + str(self.stone_mine_lvl) + ' ур.: ' + str(stone_passive) + icon('stone') + ' в час\n' + \
                      'Лесопилка ' + str(self.wood_mine_lvl) + ' ур.: ' + str(wood_passive) + icon('wood') + ' в час\n' + \
                      'Рудник ' + str(self.iron_mine_lvl) + ' ур.: ' + str(iron_passive) + icon('iron') + ' в час\n' + \
                      'Прииск ' + str(self.diamond_mine_lvl) + ' ур.: ' + str(diamond_passive) + icon('diamond') + ' в час\n'
        return message

    def tavern_bones(self, action_time, res, amount):
        if self.tavern:
            if self.tavern_bones_check(action_time, res, amount):
                result = random.randint(3, 18)
                enemy_result = random.randint(3, 18)
                if result > enemy_result:
                    # Выйгрыш
                    self.tavern_res_remove(res, amount)
                    self.tavern_res_add(res, amount)
                    message = 'Вы выйграли: ' + str(amount*2) + icon(res) + '\n' + \
                              'Ваш результат: ' + str(result) + icon('cube') + '\n' + \
                              'Результат соперника: ' + str(enemy_result) + icon('cube')
                elif result < enemy_result:
                    # Проигрыш
                    self.tavern_res_remove(res, amount)
                    message = 'Вы проиграли: ' + str(amount) + icon(res) + '\n' + \
                              'Ваш результат: ' + str(result) + icon('cube') + '\n' + \
                              'Результат соперника: ' + str(enemy_result) + icon('cube')
                elif result == enemy_result:
                    # Ничья
                    message = 'Ничья!\n' + \
                              'Ваш результат: ' + str(result) + icon('cube') + '\n' + \
                              'Результат соперника: ' + str(enemy_result) + icon('cube')
            else:
                message = 'Нехватает ресурса для ставки!'
            Stock.objects.filter(user_id=self.user_id).update(wood=self.stock.wood,
                                                              stone=self.stock.stone,
                                                              iron=self.stock.iron,
                                                              diamond=self.stock.diamond,
                                                              gold=self.stock.gold,
                                                              )
        else:
            message = 'Сначала постройте Таверну!'
        return message

    def tavern_bones_check(self, action_time, res, amount):
        self.stock = self.get_passive(action_time)
        check = False
        if res == 'wood' and self.stock.wood >= amount:
            check = True
        elif res == 'stone' and self.stock.stone >= amount:
            check = True
        elif res == 'iron' and self.stock.iron >= amount:
            check = True
        elif res == 'diamond' and self.stock.diamond >= amount:
            check = True
        elif res == 'gold' and self.stock.gold >= amount:
            check = True
        return check

    def tavern_res_remove(self, res, amount):
        if res == 'wood':
            self.stock.wood -= amount
        if res == 'stone':
            self.stock.stone -= amount
        if res == 'iron':
            self.stock.iron -= amount
        if res == 'diamond':
            self.stock.diamond -= amount
        if res == 'gold':
            self.stock.gold -= amount
        return self

    def tavern_res_add(self, res, amount):
        if res == 'wood':
            self.stock.wood = min(self.stock.wood + amount*2, self.stock.max)
        if res == 'stone':
            self.stock.stone = min(self.stock.stone + amount*2, self.stock.max)
        if res == 'iron':
            self.stock.iron = min(self.stock.iron + amount*2, self.stock.max)
        if res == 'diamond':
            self.stock.diamond = min(self.stock.diamond + amount*2, self.stock.max)
        if res == 'gold':
            self.stock.gold = min(self.stock.gold + amount*2, self.stock.max)
        return self

