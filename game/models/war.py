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
    shield = models.IntegerField(
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
                  'Всего: ' + str(self.warrior + self.archer + self.wizard) + icon('war') + '\n'
        return message

    def shield_info(self, action_time):
        shield = self.shield * SHIELD_X
        time = action_time - self.defend_last_time
        if time < shield:
            hour = (shield - time) // 3600
            minutes = ((shield - time) - (hour * 3600)) // 60
            sec = (shield - time) - (minutes * 60) - (hour * 3600)
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
            message = 'Поиск противника доступен с 10 ур.'
            return message
        find_time = action_time - self.find_last_time
        if find_time >= FIND_TIME:
            lvl = max(lvl - 2, 10)
            defender = Player.objects.filter(build__citadel=True, lvl__gte=lvl).exclude(
                user_id=self.user_id).order_by('war__defend_last_time').first()

            def is_shield():
                if defender:
                    shield = defender.war.shield * SHIELD_X
                    shield = shield + defender.war.defend_last_time
                    if shield >= action_time:
                        return False
                    else:
                        return defender
                else:
                    return False

            defender = is_shield()

            if defender:
                self.enemy_id = defender.user_id
                message = 'Найден противник!\n' + \
                          'Ник: ' + defender.nickname + '\n' + \
                          'Уровень: ' + str(defender.lvl) + icon('lvl') + '\n' + \
                          'Успейте напасть, пока вас не опередили!'
            else:
                self.enemy_id = None
                message = 'Противник не найден'

            self.find_last_time = action_time
            War.objects.filter(user_id=self.user_id).update(enemy_id=self.enemy_id,
                                                            find_last_time=self.find_last_time)

        else:
            minutes = (FIND_TIME - find_time) // 60
            sec = (FIND_TIME - find_time) - (minutes * 60)
            message = 'Искать противника можно раз в 5 минут\n' + \
                      'До следующего поиска: ' + str(minutes) + ' м. ' + str(sec) + ' сек. ⏳'
        return message

    def attack(self, player, action_time, chat_info):
        if player.lvl < 10:
            message = 'Нападения доступны с 10 ур.'
            return message
        war_time = action_time - self.war_last_time
        if war_time >= WAR_TIME:
            if self.enemy_id:

                # Проверка противника на наличие щита

                defender = Player.objects.get(user_id=self.enemy_id)

                def is_shield():
                    shield = defender.war.shield * SHIELD_X
                    shield = shield + defender.war.defend_last_time
                    if shield >= action_time:
                        return True
                    else:
                        return False

                if is_shield():
                    message = 'Вы опоздали!\n' + \
                              'На ' + defender.nickname + ' уже напали!\n' + \
                              'Найдите нового противника!'
                    self.enemy_id = None
                    War.objects.filter(user_id=self.user_id).update(enemy_id=self.enemy_id)

                else:
                    # Сражение

                    # Атакующий
                    attack_warrior_attack = self.warrior * WARRIOR_ATTACK
                    attack_warrior_hp = self.warrior * WARRIOR_HP
                    attack_archer_attack = self.archer * ARCHER_ATTACK
                    attack_archer_hp = self.archer * ARCHER_HP
                    attack_wizard_attack = self.wizard * WIZARD_ATTACK
                    attack_wizard_hp = self.wizard * WIZARD_HP
                    attack_attack = attack_warrior_attack + attack_archer_attack + attack_wizard_attack
                    attack_hp = attack_warrior_hp + attack_archer_hp + attack_wizard_hp

                    # TOWER BUFF

                    attack_tower_x = player.build.tower_lvl * TOWER_BUFF
                    attack_attack = attack_attack * (1 + attack_tower_x)

                    attack_wall_x = player.build.wall_lvl * WALL_BUFF
                    attack_wall_power = attack_hp * (1 + attack_wall_x)
                    attack_power = attack_attack + attack_hp + attack_wall_power

                    # Защитник

                    # WALL BUFF

                    defender_wall_x = 1 + (WALL_BUFF * defender.build.wall_lvl)
                    def_warrior_hp = WARRIOR_HP * defender_wall_x
                    def_archer_hp = ARCHER_HP * defender_wall_x
                    def_wizard_hp = WIZARD_HP * defender_wall_x

                    defender_warrior_attack = defender.war.warrior * WARRIOR_ATTACK
                    defender_warrior_hp = defender.war.warrior * def_warrior_hp
                    defender_archer_attack = defender.war.archer * ARCHER_ATTACK
                    defender_archer_hp = defender.war.archer * def_archer_hp
                    defender_wizard_attack = defender.war.wizard * WIZARD_ATTACK
                    defender_wizard_hp = defender.war.wizard * def_wizard_hp
                    defender_attack = defender_warrior_attack + defender_archer_attack + defender_wizard_attack
                    defender_hp = defender_warrior_hp + defender_archer_hp + defender_wizard_hp

                    defender_tower_x = player.build.tower_lvl * TOWER_BUFF
                    defender_tower_power = defender_hp * (1 + defender_tower_x)
                    defender_power = defender_attack + defender_hp + defender_tower_power

                    # Остатки армий

                    attack_after_hp = attack_hp - defender_attack
                    defender_after_hp = defender_hp - attack_attack

                    attack_after_warrior = 0
                    attack_after_archer = 0
                    attack_after_wizard = 0
                    if attack_hp > 0 and attack_after_hp > 0:
                        attack_after_warrior = ((attack_warrior_hp / attack_hp) * attack_after_hp) // WARRIOR_HP
                        attack_after_archer = ((attack_archer_hp / attack_hp) * attack_after_hp) // ARCHER_HP
                        attack_after_wizard = ((attack_wizard_hp / attack_hp) * attack_after_hp) // WIZARD_HP
                        attack_after_warrior = round(max(self.warrior*0.6, attack_after_warrior))
                        attack_after_archer = round(max(self.archer*0.6, attack_after_archer))
                        attack_after_wizard = round(max(self.wizard*0.6, attack_after_wizard))
                    attack_lost_warrior = round(self.warrior - attack_after_warrior)
                    attack_lost_archer = round(self.archer - attack_after_archer)
                    attack_lost_wizard = round(self.wizard - attack_after_wizard)

                    defender_after_warrior = 0
                    defender_after_archer = 0
                    defender_after_wizard = 0
                    if defender_hp > 0 and defender_after_hp > 0:
                        defender_after_warrior = ((defender_warrior_hp / defender_hp) * defender_after_hp) // def_warrior_hp
                        defender_after_archer = ((defender_archer_hp / defender_hp) * defender_after_hp) // def_archer_hp
                        defender_after_wizard = ((defender_wizard_hp / defender_hp) * defender_after_hp) // def_wizard_hp
                        defender_after_warrior = round(max(defender.war.warrior * 0.6, defender_after_warrior))
                        defender_after_archer = round(max(defender.war.archer * 0.6, defender_after_archer))
                        defender_after_wizard = round(max(defender.war.wizard * 0.6, defender_after_wizard))
                    defender_lost_warrior = round(defender.war.warrior - defender_after_warrior)
                    defender_lost_archer = round(defender.war.archer - defender_after_archer)
                    defender_lost_wizard = round(defender.war.wizard - defender_after_wizard)

                    if attack_power >= defender_power:

                        # Обновляем склады

                        defender.build.stock = defender.build.get_passive(action_time)
                        player.build.stock = player.build.get_passive(action_time)

                        # Победа нападавшего

                        # Награда
                        # TODO После резлиза следить за наградой, проверить
                        cost = round(defender.build.stock.max * 4 * 0.2 / 11)
                        reward = round(defender.build.stock.max * 4 * 0.3 / 11)
                        reward_skull = 1
                        reward_exp = 5
                        player = exp(player, chat_info, reward_exp)
                        print('Забрали - ' + str(cost))
                        print('Награда - ' + str(reward))

                        # Проигравший

                        defender.build.stock.stone -= min(cost * 4, defender.build.stock.stone)
                        defender.build.stock.wood -= min(cost * 4, defender.build.stock.wood)
                        defender.build.stock.iron -= min(cost * 2, defender.build.stock.iron)
                        defender.build.stock.diamond -= min(cost, defender.build.stock.diamond)

                        defender.war.shield = 8

                        # Выдаём победителю

                        player.build.stock.stone += min(reward * 4, (player.build.stock.max - player.build.stock.stone))
                        player.build.stock.wood += min(reward * 4, (player.build.stock.max - player.build.stock.wood))
                        player.build.stock.iron += min(reward * 2, (player.build.stock.max - player.build.stock.iron))
                        player.build.stock.diamond += min(reward, (player.build.stock.max - player.build.stock.diamond))
                        player.build.stock.skull += reward_skull

                        message = 'Вы напали на ' + defender.nickname + '\n' + \
                                  '⚔ Победа ⚔\n' + \
                                  '[Ваши потери]\n' + \
                                  'Воины: ' + str(attack_lost_warrior) + ' / ' + str(self.warrior) + ' 🗡\n' + \
                                  'Лучники: ' + str(attack_lost_archer) + ' / ' + str(self.archer) + ' 🏹\n' + \
                                  'Маги: ' + str(attack_lost_wizard) + ' / ' + str(self.wizard) + ' 🔮\n' + \
                                  '[Награда]\n' + \
                                  'Дерево: ' + str(reward * 4) + ' 🌲\n' + \
                                  'Камень: ' + str(reward * 4) + ' ◾\n' + \
                                  'Железо: ' + str(reward * 2) + ' ◽\n' + \
                                  'Алмазы: ' + str(reward) + ' 💎\n' + \
                                  'Черепа: ' + str(reward_skull) + ' 💀\n' + \
                                  'Опыт: ' + str(reward_exp) + ' 📚'

                        message_def = 'На вас напал ' + player.nickname + '\n' + \
                                      '⚔ Вы проиграли ⚔\n' + \
                                      '[Ваши потери]\n' + \
                                      'Воины: ' + str(defender_lost_warrior) + ' / ' + str(defender.war.warrior) + ' 🗡\n' + \
                                      'Лучники: ' + str(defender_lost_archer) + ' / ' + str(defender.war.archer) + ' 🏹\n' + \
                                      'Маги: ' + str(defender_lost_wizard) + ' / ' + str(defender.war.wizard) + ' 🔮\n' + \
                                      '[Ресурсов потеряно]\n' + \
                                      'Дерево: ' + str(cost * 4) + ' 🌲\n' + \
                                      'Камень: ' + str(cost * 4) + ' ◾\n' + \
                                      'Железо: ' + str(cost * 2) + ' ◽\n' + \
                                      'Алмазы: ' + str(cost) + ' 💎\n' + \
                                      '🛡 Вам выдан щит от нападений на 8 часов 🛡\n' + \
                                      'Если вы нападёте, щит пропадёт!'

                    else:

                        # Поражение нападавшего

                        defender.war.shield = 8

                        message = 'Вы напали на ' + defender.nickname + '\n' + \
                                  '⚔ Поражение ⚔\n' + \
                                  '[Ваши потери]\n' + \
                                  'Воины: ' + str(attack_lost_warrior) + ' / ' + str(self.warrior) + ' 🗡\n' + \
                                  'Лучники: ' + str(attack_lost_archer) + ' / ' + str(self.archer) + ' 🏹\n' + \
                                  'Маги: ' + str(attack_lost_wizard) + ' / ' + str(self.wizard) + ' 🔮\n'

                        message_def = 'На вас напал ' + player.nickname + '\n' + \
                                      '⚔ Вы победили ⚔\n' + \
                                      '[Ваши потери]\n' + \
                                      'Воины: ' + str(defender_lost_warrior) + ' / ' + str(defender.war.warrior) + ' 🗡\n' + \
                                      'Лучники: ' + str(defender_lost_archer) + ' / ' + str(defender.war.archer) + ' 🏹\n' + \
                                      'Маги: ' + str(defender_lost_wizard) + ' / ' + str(defender.war.wizard) + ' 🔮\n' + \
                                      '🛡 Вам выдан щит от нападений на 8 часов 🛡\n' + \
                                      'Если вы нападёте, щит пропадёт!'

                    # Сохранение

                    self.warrior = attack_after_warrior // 1
                    self.archer = attack_after_archer // 1
                    self.wizard = attack_after_wizard // 1
                    self.war_last_time = action_time
                    self.shield = 0
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
                                                                    enemy_id=self.enemy_id,)
                    Player.objects.filter(user_id=self.user_id).update(energy=player.energy,
                                                                       exp=player.exp,
                                                                       lvl=player.lvl)

                    defender.war.warrior = defender_after_warrior // 1
                    defender.war.archer = defender_after_archer // 1
                    defender.war.wizard = defender_after_wizard // 1
                    defender.war.defend_last_time = action_time
                    Stock.objects.filter(user_id=defender.user_id).update(stone=defender.build.stock.stone,
                                                                          wood=defender.build.stock.wood,
                                                                          iron=defender.build.stock.iron,
                                                                          diamond=defender.build.stock.diamond,
                                                                          skull=defender.build.stock.skull)
                    War.objects.filter(user_id=defender.user_id).update(warrior=defender.war.warrior,
                                                                        archer=defender.war.archer,
                                                                        wizard=defender.war.wizard,
                                                                        defend_last_time=defender.war.defend_last_time,
                                                                        shield=defender.war.shield,
                                                                        enemy_id=defender.war.enemy_id)
                    send_info = {
                        'user_id': defender.user_id,
                        'chat_id': defender.user_id,
                    }
                    try:
                        send(send_info, message_def)
                    except:
                        pass

            else:
                message = 'Найдите противника для нападения!'
        else:
            minutes = (WAR_TIME - war_time) // 60
            sec = (WAR_TIME - war_time) - (minutes * 60)
            message = 'До нападения: ' + str(minutes) + ' м. ' + str(sec) + ' сек. ⏳'
        return message

