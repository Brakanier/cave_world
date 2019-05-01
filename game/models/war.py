from django.db import models

from ..actions.functions import *
from .build import Stock
from .player import Player


class War(models.Model):
    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )
    enemy_id = models.BigIntegerField(
        null=True,
        blank=True,
    )
    shield = models.BigIntegerField(
        default=0,
    )
    success_attack = models.IntegerField(
        default=0,
    )
    success_defend = models.IntegerField(
        default=0,
    )
    find_last_time = models.BigIntegerField(
        default=0,
    )
    war_last_time = models.BigIntegerField(
        default=0,
    )
    defend_last_time = models.BigIntegerField(
        default=0,
    )
    boss_last_time = models.BigIntegerField(
        default=0,
    )
    crusade_last_time = models.BigIntegerField(
        default=0,
    )
    crusade_part = models.IntegerField(
        default=0,
    )
    enemy = models.CharField(
        max_length=30,
        blank=True,
        default='',
    )
    enemy_army = models.IntegerField(
        default=0,
    )
    warrior = models.IntegerField(
        default=0,
    )
    archer = models.IntegerField(
        default=0,
    )
    wizard = models.IntegerField(
        default=0,
    )

    class Meta:
        verbose_name = 'Война'
        verbose_name_plural = 'Войны'

    def army(self):
        message = 'Армия:\n' + \
                  'Воины: ' + str(self.warrior) + icon('sword') + '\n' + \
                  'Лучники: ' + str(self.archer) + icon('bow') + '\n' + \
                  'Маги: ' + str(self.wizard) + icon('orb') + '\n' + \
                  'Всего: ' + str(self.sum_army()) + icon('war') + '\n'
        return message

    def shield_info(self, action_time):
        if self.shield > action_time:
            shield = self.shield - action_time
            hour = shield // 3600
            minutes = (shield - (hour * 3600)) // 60
            sec = shield - (minutes * 60) - (hour * 3600)
            message = 'Щит действует еще: ' + \
                      str(hour) + ' ч. ' + \
                      str(minutes) + ' м. ' + \
                      str(sec) + ' сек.' + icon('time')
        else:
            message = 'У вас нет щита!'
        return message

    def craft_warrior(self, build, action_time, amount=1):
        build.stock = build.get_passive(action_time)
        if build.barracks:
            need_iron = amount * WARRIOR_IRON
            if build.stock.iron >= need_iron:
                build.stock.iron = build.stock.iron - need_iron
                self.warrior = self.warrior + amount
                Stock.objects.filter(user_id=self.user_id).update(iron=build.stock.iron)
                War.objects.filter(user_id=self.user_id).update(warrior=self.warrior)
                message = 'Вы наняли ' + str(amount) + icon('sword')
            else:
                message = 'Недостаточно ресурсов!\n' + \
                          'Для ' + str(amount) + icon('sword') + ' нужно:\n' + \
                          'Железа: ' + str(need_iron) + icon('iron')
        else:
            message = 'Сначала постройте Казармы!'
        return message

    def craft_archer(self, build, action_time, amount=1):
        build.stock = build.get_passive(action_time)
        if build.archery:
            need_iron = amount * ARCHER_IRON
            need_wood = amount * ARCHER_WOOD
            if build.stock.iron >= need_iron \
                    and build.stock.wood >= need_wood:
                build.stock.iron = build.stock.iron - need_iron
                build.stock.wood = build.stock.wood - need_wood
                self.archer = self.archer + amount
                Stock.objects.filter(user_id=self.user_id).update(iron=build.stock.iron,
                                                                  wood=build.stock.wood)
                War.objects.filter(user_id=self.user_id).update(archer=self.archer)
                message = 'Вы наняли ' + str(amount) + icon('bow')
            else:
                message = 'Недостаточно ресурсов!\n' + \
                          'Для ' + str(amount) + icon('bow') + ' нужно:\n' + \
                          'Дерева: ' + str(need_wood) + icon('wood') + '\n' + \
                          'Железа: ' + str(need_iron) + icon('iron')
        else:
            message = 'Сначала постройте Стрельбище!'
        return message

    def craft_wizard(self, build, action_time, amount=1):
        build.stock = build.get_passive(action_time)
        if build.magic:
            need_iron = amount * WIZARD_IRON
            need_wood = amount * WIZARD_WOOD
            need_diamond = amount * WIZARD_DIAMOND
            if build.stock.iron >= need_iron \
                    and build.stock.wood >= need_wood \
                    and build.stock.diamond >= need_diamond:
                build.stock.iron = build.stock.iron - need_iron
                build.stock.wood = build.stock.wood - need_wood
                build.stock.diamond = build.stock.diamond - need_diamond
                self.wizard = self.wizard + amount
                Stock.objects.filter(user_id=self.user_id).update(iron=build.stock.iron,
                                                                  wood=build.stock.wood,
                                                                  diamond=build.stock.diamond)
                War.objects.filter(user_id=self.user_id).update(wizard=self.wizard)
                message = 'Вы наняли ' + str(amount) + icon('orb')
            else:
                message = 'Недостаточно ресурсов!\n' + \
                          'Для ' + str(amount) + icon('orb') + ' нужно:\n' + \
                          'Дерева: ' + str(need_wood) + icon('wood') + '\n' + \
                          'Железа: ' + str(need_iron) + icon('iron') + '\n' + \
                          'Кристаллы: ' + str(need_diamond) + icon('diamond')
        else:
            message = 'Сначала постройте Башню Магов!'
        return message

    def find_enemy(self, lvl, action_time):
        if lvl < 10:
            message = 'Сражения и поиск противника доступны с 10 ур.'
            return message
        find_time = action_time - self.find_last_time
        if find_time >= FIND_TIME:
            lvl = max(lvl - 10, 12)
            defenders = Player.objects.filter(build__citadel=True, lvl__gte=lvl, war__shield__lte=action_time).exclude(
                user_id=self.user_id).all()

            if defenders:
                defender = random.choice(defenders)
                self.enemy_id = defender.user_id
                message = 'Найден противник!\n' + \
                          'Ник: ' + defender.nickname + '\n' + \
                          'Вы можете разведывать противника:\n' + \
                          'Разведка - информация о противнике (10' + icon('diamond') + ')'
            else:
                self.enemy_id = None
                message = 'Противник не найден!'

            self.find_last_time = action_time
            War.objects.filter(user_id=self.user_id).update(enemy_id=self.enemy_id,
                                                            find_last_time=self.find_last_time)

        else:
            minutes = (FIND_TIME - find_time) // 60
            sec = (FIND_TIME - find_time) - (minutes * 60)
            message = 'Искать противника можно раз в 5 минут\n' + \
                      'До следующего поиска: ' + str(minutes) + ' м. ' + str(sec) + ' сек. ⏳'
        return message

    def scouting(self, action_time):
        if self.enemy_id:
            defender = Player.objects.get(user_id=self.enemy_id)
            if defender.war.shield > action_time:
                message = 'Вы опоздали!\n' + \
                          'На ' + defender.nickname + ' уже напали!\n' + \
                          'Найдите нового противника!'
                self.enemy_id = None
                War.objects.filter(user_id=self.user_id).update(enemy_id=self.enemy_id)
            elif self.player.build.stock.diamond >= 10:
                self.player.build.stock.diamond -= 10
                self.player.build.stock.save(update_fields=['diamond'])
                def_army = defender.war.sum_army()
                def_army_min = max(def_army - random.randint(30, 100), 0)
                def_army_max = def_army + random.randint(30, 100)
                message = 'Разведка: ' + defender.nickname + '\n' + \
                          'Уровень: ' + str(defender.lvl) + icon('lvl') + '\n' + \
                          'Армия: ' + str(def_army_min) + ' ~ ' + str(def_army_max) + icon('war')
                rand_scouting = random.randint(0, 100)
                if rand_scouting >= 0:
                    def_message = 'Вас разведывал: ' + self.player.nickname
                    defender.war.send_defender(def_message)
            else:
                message = "Нужно 10 " + icon('diamond')
        else:
            message = "Сначала найдите противника!"
        return message

    def send_defender(self, message):
        try:
            send_info = {
                'user_id': self.player.user_id,
                'chat_id': self.player.user_id,
            }
            send(send_info, message)
        except:
            if self.player.chat_id != self.player.user_id:
                send_info = {
                    'user_id': self.player.user_id,
                    'peer_id': self.player.chat_id,
                    'chat_id': self.player.chat_id - 2000000000,
                    'nick': self.player.nickname,
                }
                try:
                    send(send_info, message)
                except:
                    pass

    def sum_army(self):
        sum_army = self.warrior + self.archer + self.wizard
        return sum_army

    def sum_attack(self, enemy):
        on_war, on_arch, on_wiz = self.get_attack()
        if enemy.war.warrior <= 0:
            on_war = 0
        if enemy.war.archer <= 0:
            on_arch = 0
        if enemy.war.wizard <= 0:
            on_wiz = 0
        sum_attack = on_war + on_arch + on_wiz
        return sum_attack

    def get_modify(self, count):
        if count > 0:
            sum_army = self.sum_army()
            average = sum_army / 3
            diff = min(abs(count - average) / sum_army, 0.3)
            modify = 1 - diff
        else:
            modify = 0
        return modify

    def get_attack(self):
        mod_war = self.get_modify(self.warrior)
        mod_arch = self.get_modify(self.archer)
        mod_wiz = self.get_modify(self.wizard)
        tower_buff = 1 + (self.player.build.tower_lvl * TOWER_BUFF)
        war_war = tower_buff * WARRIOR_ATTACK * self.warrior * mod_war / 3
        war_arch = tower_buff * WARRIOR_ATTACK * self.warrior * mod_war * 2 / 3
        war_wiz = tower_buff * WARRIOR_ATTACK * self.warrior * mod_war * 0.5 / 3
        arch_arch = tower_buff * ARCHER_ATTACK * self.archer * mod_arch / 3
        arch_war = tower_buff * ARCHER_ATTACK * self.archer * mod_arch * 0.5 / 3
        arch_wiz = tower_buff * ARCHER_ATTACK * self.archer * mod_arch * 2 / 3
        wiz_wiz = tower_buff * WIZARD_ATTACK * self.wizard * mod_wiz / 3
        wiz_war = tower_buff * WIZARD_ATTACK * self.wizard * mod_wiz * 2 / 3
        wiz_arch = tower_buff * WIZARD_ATTACK * self.wizard * mod_wiz * 0.5 / 3
        on_war = war_war + arch_war + wiz_war
        on_arch = war_arch + arch_arch + wiz_arch
        on_wiz = war_wiz + arch_wiz + wiz_wiz
        return on_war, on_arch, on_wiz

    def get_alive(self, enemy):
        mod_war = self.get_modify(self.warrior)
        mod_arch = self.get_modify(self.archer)
        mod_wiz = self.get_modify(self.wizard)
        on_war, on_arch, on_wiz = enemy.war.get_attack()
        wall_buff = 1 + (self.player.build.wall_lvl * WALL_BUFF)
        if mod_war > 0:
            war_hp_one = WARRIOR_HP * wall_buff * mod_war
            war_hp = self.warrior * war_hp_one
            war_hp_after = war_hp - on_war
            war_alive = war_hp_after / war_hp_one
        else:
            war_alive = 0
        if mod_arch > 0:
            arch_hp_one = ARCHER_HP * wall_buff * mod_arch
            arch_hp = self.archer * arch_hp_one
            arch_hp_after = arch_hp - on_arch
            arch_alive = arch_hp_after / arch_hp_one
        else:
            arch_alive = 0
        if mod_wiz > 0:
            wiz_hp_one = WIZARD_HP * wall_buff * mod_wiz
            wiz_hp = self.wizard * wiz_hp_one
            wiz_hp_after = wiz_hp - on_wiz
            wiz_alive = wiz_hp_after / wiz_hp_one
        else:
            wiz_alive = 0
        return war_alive, arch_alive, wiz_alive

    def get_die(self, enemy, die_x=0.4):
        war_alive, arch_alive, wiz_alive = self.get_alive(enemy)
        war_die = min(round(self.warrior - war_alive), round(self.warrior * die_x))
        arch_die = min(round(self.archer - arch_alive), round(self.archer * die_x))
        wiz_die = min(round(self.wizard - wiz_alive), round(self.wizard * die_x))
        return war_die, arch_die, wiz_die

    def get_reward(self, enemy):
        war_die, arch_die, wiz_die = self.get_die(enemy)
        iron_war = war_die * WARRIOR_IRON
        iron_arch = arch_die * ARCHER_IRON
        iron_wiz = wiz_die * WIZARD_IRON
        wood_arch = arch_die * ARCHER_WOOD
        wood_wiz = wiz_die * WIZARD_WOOD
        diamond = wiz_die * WIZARD_DIAMOND
        iron = iron_war + iron_arch + iron_wiz
        wood = wood_arch + wood_wiz
        stone = int((iron + wood + diamond) / 3)
        return stone, wood, iron, diamond

    def attack(self, player, action_time, chat_info):
        if player.lvl < 10:
            message = 'Нападения доступны с 10 ур.'
            return message
        war_time = action_time - self.war_last_time
        if war_time >= WAR_TIME:
            if self.enemy_id:

                # Проверка противника на наличие щита

                defender = Player.objects.get(user_id=self.enemy_id)

                if defender.war.shield > action_time:
                    message = 'Вы опоздали!\n' + \
                              'На ' + defender.nickname + ' уже напали!\n' + \
                              'Найдите нового противника!'
                    self.enemy_id = None
                    self.save(update_fields=['enemy_id'])

                else:

                    # Сражение

                    # Атакующий - a
                    a_attack = self.sum_attack(defender)
                    a_war_die, a_arch_die, a_wiz_die = self.get_die(defender)
                    a_sum_die = a_war_die + a_arch_die + a_wiz_die

                    # Защитник - d
                    d_attack = defender.war.sum_attack(player)

                    print(a_attack)
                    print(d_attack)

                    if a_attack >= d_attack:

                        self.success_attack += 1

                        # Обновляем склады

                        defender.build.stock = defender.build.get_passive(action_time)
                        player.build.stock = player.build.get_passive(action_time)

                        # Победа нападавшего

                        # Награда
                        stone, wood, iron, diamond = self.get_reward(defender)
                        reward_skull = 1
                        reward_exp = 5
                        player = exp(player, chat_info, reward_exp)

                        # Проигравший
                        cost_stone = int(defender.build.stock.stone / 10)
                        cost_wood = int(defender.build.stock.wood / 10)
                        cost_iron = int(defender.build.stock.iron / 10)
                        cost_diamond = int(defender.build.stock.diamond / 10)
                        defender.build.stock.stone -= cost_stone
                        defender.build.stock.wood -= cost_wood
                        defender.build.stock.iron -= cost_iron
                        defender.build.stock.diamond -= cost_diamond

                        defender.war.shield = action_time + (8 * 3600)

                        # Выдаём победителю

                        player.build.stock.stone += min(stone, (player.build.stock.max - player.build.stock.stone))
                        player.build.stock.wood += min(wood * 4, (player.build.stock.max - player.build.stock.wood))
                        player.build.stock.iron += min(iron * 2, (player.build.stock.max - player.build.stock.iron))
                        player.build.stock.diamond += min(diamond, (player.build.stock.max - player.build.stock.diamond))
                        player.build.stock.skull += reward_skull

                        d_war_die, d_arch_die, d_wiz_die = defender.war.get_die(player, 0.2)
                        d_sum_die = d_war_die + d_arch_die + d_wiz_die

                        message = 'Вы напали на ' + defender.nickname + '\n' + \
                                  '⚔ Победа ⚔\n' + \
                                  '[Ваши потери]\n' + \
                                  'Воины: ' + str(a_war_die) + ' / ' + str(self.warrior) + ' 🗡\n' + \
                                  'Лучники: ' + str(a_arch_die) + ' / ' + str(self.archer) + ' 🏹\n' + \
                                  'Маги: ' + str(a_wiz_die) + ' / ' + str(self.wizard) + ' 🔮\n' + \
                                  'Всего: ' + str(a_sum_die) + ' / ' + str(self.sum_army()) + ' ⚔\n' + \
                                  '[Потери противника]\n' + \
                                  'Воины: ' + str(d_war_die) + ' / ' + str(defender.war.warrior) + ' 🗡\n' + \
                                  'Лучники: ' + str(d_arch_die) + ' / ' + str(defender.war.archer) + ' 🏹\n' + \
                                  'Маги: ' + str(d_wiz_die) + ' / ' + str(defender.war.wizard) + ' 🔮\n' + \
                                  'Всего: ' + str(d_sum_die) + ' / ' + str(defender.war.sum_army()) + ' ⚔\n' + \
                                  '[Награда]\n' + \
                                  'Дерево: ' + str(wood) + ' 🌲\n' + \
                                  'Камень: ' + str(stone) + ' ◾\n' + \
                                  'Железо: ' + str(iron) + ' ◽\n' + \
                                  'Алмазы: ' + str(diamond) + ' 💎\n' + \
                                  'Черепа: ' + str(reward_skull) + ' 💀\n' + \
                                  'Опыт: ' + str(reward_exp) + ' 📚'

                        message_def = 'На вас напал ' + player.nickname + '\n' + \
                                      '⚔ Вы проиграли ⚔\n' + \
                                      '[Ваши потери]\n' + \
                                      'Воины: ' + str(d_war_die) + ' / ' + str(defender.war.warrior) + ' 🗡\n' + \
                                      'Лучники: ' + str(d_arch_die) + ' / ' + str(defender.war.archer) + ' 🏹\n' + \
                                      'Маги: ' + str(d_wiz_die) + ' / ' + str(defender.war.wizard) + ' 🔮\n' + \
                                      'Всего: ' + str(d_sum_die) + ' / ' + str(defender.war.sum_army()) + ' ⚔\n' + \
                                      '[Потери противника]\n' + \
                                      'Воины: ' + str(a_war_die) + ' / ' + str(self.warrior) + ' 🗡\n' + \
                                      'Лучники: ' + str(a_arch_die) + ' / ' + str(self.archer) + ' 🏹\n' + \
                                      'Маги: ' + str(a_wiz_die) + ' / ' + str(self.wizard) + ' 🔮\n' + \
                                      'Всего: ' + str(a_sum_die) + ' / ' + str(self.sum_army()) + ' ⚔\n' + \
                                      '[Ресурсов потеряно]\n' + \
                                      'Дерево: ' + str(cost_wood) + ' 🌲\n' + \
                                      'Камень: ' + str(cost_stone) + ' ◾\n' + \
                                      'Железо: ' + str(cost_iron) + ' ◽\n' + \
                                      'Алмазы: ' + str(cost_diamond) + ' 💎\n' + \
                                      '🛡 Вам выдан щит от нападений на 8 часов 🛡\n' + \
                                      'Если вы нападёте, щит пропадёт!'

                    else:

                        # Поражение нападавшего

                        defender.war.success_defend += 1
                        defender.war.shield = action_time + (2 * 3600)

                        d_war_die, d_arch_die, d_wiz_die = defender.war.get_die(player)
                        d_sum_die = d_war_die + d_arch_die + d_wiz_die

                        message = 'Вы напали на ' + defender.nickname + '\n' + \
                                  '⚔ Поражение ⚔\n' + \
                                  '[Ваши потери]\n' + \
                                  'Воины: ' + str(a_war_die) + ' / ' + str(self.warrior) + ' 🗡\n' + \
                                  'Лучники: ' + str(a_arch_die) + ' / ' + str(self.archer) + ' 🏹\n' + \
                                  'Маги: ' + str(a_wiz_die) + ' / ' + str(self.wizard) + ' 🔮\n' + \
                                  'Всего: ' + str(a_sum_die) + ' / ' + str(self.sum_army()) + ' ⚔\n'

                        message_def = 'На вас напал ' + player.nickname + '\n' + \
                                      '⚔ Вы победили ⚔\n' + \
                                      '[Ваши потери]\n' + \
                                      'Воины: ' + str(d_war_die) + ' / ' + str(defender.war.warrior) + ' 🗡\n' + \
                                      'Лучники: ' + str(d_arch_die) + ' / ' + str(defender.war.archer) + ' 🏹\n' + \
                                      'Маги: ' + str(d_wiz_die) + ' / ' + str(defender.war.wizard) + ' 🔮\n' + \
                                      'Всего: ' + str(d_sum_die) + ' / ' + str(defender.war.sum_army()) + ' ⚔\n' + \
                                      '[Потери Противника]\n' + \
                                      'Воины: ' + str(a_war_die) + ' / ' + str(self.warrior) + ' 🗡\n' + \
                                      'Лучники: ' + str(a_arch_die) + ' / ' + str(self.archer) + ' 🏹\n' + \
                                      'Маги: ' + str(a_wiz_die) + ' / ' + str(self.wizard) + ' 🔮\n' + \
                                      'Всего: ' + str(a_sum_die) + ' / ' + str(self.sum_army()) + ' ⚔\n' + \
                                      '🛡 Вам выдан щит от нападений на 2 часа 🛡\n' + \
                                      'Если вы нападёте, щит пропадёт!'

                    # Сохранение

                    self.warrior -= a_war_die
                    self.archer -= a_arch_die
                    self.wizard -= a_wiz_die
                    self.war_last_time = action_time
                    self.shield = action_time
                    self.enemy_id = None
                    Stock.objects.filter(user_id=self.user_id).update(stone=player.build.stock.stone,
                                                                      wood=player.build.stock.wood,
                                                                      iron=player.build.stock.iron,
                                                                      diamond=player.build.stock.diamond,
                                                                      skull=player.build.stock.skull)
                    War.objects.filter(user_id=self.user_id).update(warrior=self.warrior,
                                                                    archer=self.archer,
                                                                    wizard=self.wizard,
                                                                    war_last_time=self.war_last_time,
                                                                    shield=self.shield,
                                                                    enemy_id=self.enemy_id,
                                                                    success_attack=self.success_attack)
                    Player.objects.filter(user_id=self.user_id).update(exp=player.exp,
                                                                       energy=player.energy,
                                                                       lvl=player.lvl)

                    defender.war.warrior -= d_war_die
                    defender.war.archer -= d_arch_die
                    defender.war.wizard -= d_wiz_die
                    defender.war.defend_last_time = action_time
                    Stock.objects.filter(user_id=defender.user_id).update(stone=defender.build.stock.stone,
                                                                          wood=defender.build.stock.wood,
                                                                          iron=defender.build.stock.iron,
                                                                          diamond=defender.build.stock.diamond)
                    War.objects.filter(user_id=defender.user_id).update(warrior=defender.war.warrior,
                                                                        archer=defender.war.archer,
                                                                        wizard=defender.war.wizard,
                                                                        defend_last_time=defender.war.defend_last_time,
                                                                        shield=defender.war.shield,
                                                                        success_defend=defender.war.success_defend)

                    defender.war.send_defender(message_def)
            else:
                message = 'Найдите противника для нападения!'
        else:
            minutes = (WAR_TIME - war_time) // 60
            sec = (WAR_TIME - war_time) - (minutes * 60)
            message = 'До нападения: ' + str(minutes) + ' м. ' + str(sec) + ' сек. ⏳'
        return message

