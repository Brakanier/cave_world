from django.db import models

from ..actions.functions import *
from ..actions.chests import *

import random
import json


class CaveMap(models.Model):

    cave_map = models.TextField(
        blank=True,
    )


class CaveProgress(models.Model):

    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )

    cave = models.ForeignKey(
        CaveMap,
        on_delete=models.SET(None),
        null=True,
        blank=True,
    )
    player_map = models.TextField(
        blank=True,
        null=True,
    )
    y = models.IntegerField(
        blank=True,
        default=None,
        null=True,
    )
    x = models.IntegerField(
        blank=True,
        default=None,
        null=True,
    )
    level = models.IntegerField(
        default=1,
    )
    success = models.IntegerField(
        default=0,
        db_index=True,
    )
    time = models.BigIntegerField(
        default=0,
    )

    def info(self):
        mess = 'Легенда карты:\n' + \
        '🌫 - неизвестная клетка\n' + \
        '🐾 - ваш путь\n' + \
        '🍀 - цветок жизни\n' + \
        '🎁 - пещерный сундук\n' + \
        '🚧 - тупик\n' + \
        '💨 - ядовитые гейзеры\n' + \
        '👻 - заблудшие\n' + \
        '🚩 - вход на уровень\n' + \
        '🕳 - проход на след. уровень\n' + \
        '🤴 - вы\n\n' + \
        'Сокровищ найдено: ' + str(self.success)
        return mess

    def start(self, action_time):
        if (self.time - action_time) > 3600:
            cave_time = self.time - action_time
            sec = cave_time
            minutes = sec // 60
            hour = minutes // 60
            time_mess = 'Вы нашли сокровища, Хранитель Подземелья закрыл вам проход в пещеры.\n' + \
                        'Проход откроется через: ' + \
                        str(hour % 24) + ' ч. ' + \
                        str(minutes % 60) + ' м. ' + \
                        str(sec % 60) + ' сек. ⏳'
            return time_mess
        if action_time < self.time:
            cave_time = self.time - action_time
            sec = cave_time
            minutes = sec // 60
            hour = minutes // 60
            time_mess = 'В пещеры можно отправиться раз в час.\n' + \
                        'До следующего раза: ' + \
                        str(hour % 24) + ' ч. ' + \
                        str(minutes % 60) + ' м. ' + \
                        str(sec % 60) + ' сек. ⏳'
            return time_mess

        army = self.player.lvl * 3

        if self.player.war.sum_army() < army:
            return 'Для исследования пещер вам нужно минимум ' + str(army) + ' ⚔ армии!'
        mess = ''
        if not self.cave:
            self.cave = CaveMap.objects.get()
            mess = 'Пещеры изменились!\n'
        self.level = 1
        self.time = action_time + 3600
        self.save(update_fields=['level', 'cave', 'time'])
        self.player.place = 'cave_go'
        self.player.save(update_fields=['place'])
        mess += 'Вы зашли в пещеры!\n' + \
                'Вы сейчас на ' + str(self.level) + ' ур. пещер.\n' + \
                'Выберите в какую сторону идти:\n' + \
                '- Пещеры налево\n' + \
                '- Пещеры направо\n' + \
                'Не используйте другие команды! Вас выбросит из пещеры!\n'
        return mess

    def go(self, way, action_time):
        if self.player.place != 'cave_go':
            return "Вы не в пещерах!\n- Пещеры войти"
        if not self.cave:
            self.player.place = 'cave'
            self.player.save(update_fields=['place'])
            return 'Кто-то нашёл сокровища...\n' + \
                   'Произошёл обвал...\n' + \
                   'Пути в пещерах изменились, начните исследование заново!\n' + \
                   '- Пещеры войти\n'
        cave_lvl = self.level
        cave_map = json.loads(self.cave.cave_map)
        bonus = cave_map[str(cave_lvl)][str(way)]

        bonus_mess = self.cave_bonus(bonus, cave_lvl + 1)
        end_mess = ""
        start_mess = 'Вы сейчас на ' + str(self.level) + ' ур.\n'
        if way == 1:
            start_mess += 'Вы пошли налево...\n'
        elif way == 2:
            start_mess += 'Вы пошли направо...\n'
        if bonus == 0:
            end_mess = 'Вы вернулись домой!'
        elif bonus in (3, 4, 5, 6):
            self.level = cave_lvl + 1
            if cave_lvl < 30:
                end_mess = '\nПещера раздваивается, выберите путь:\n' + \
                           '- Пещеры налево\n' + \
                           '- Пещеры направо\n'
        if self.max_level < self.level:
            self.max_level = self.level
        if bonus in (0, 1, 2):
            self.player.place = 'cave'
            self.player.save(update_fields=['place'])

        if bonus == 7:
            self.max_level = 1
            start_mess += 'Впереди какое-то свечение...\n Вы подходите ближе...\n'
            self.success += 1
            self.time = action_time + 3600 * 10
            CaveMap.objects.filter(pk=self.cave.pk).delete()
            cave = CaveMap.objects.create()
            cave.cave_map = cave.generate()
            cave.save()

        self.save(update_fields=['level', 'max_level', 'success', 'time'])

        message = start_mess + bonus_mess + end_mess
        return message

    def cave_bonus(self, number, lvl):
        bonus_mess = ""
        if number == 0:
            lost_part = 20
            lost_war = self.player.war.warrior // lost_part
            lost_arch = self.player.war.archer // lost_part
            lost_wiz = self.player.war.wizard // lost_part
            bonus_mess = 'Двигаясь по пещере вы нашли долину гейзеров.\nКто ж знал, что пар с ядовитым газом...\n'
            lost_mess = '[Ваши потери]\n' + \
                        'Воины: ' + str(lost_war) + ' / ' + str(self.player.war.warrior) + ' 🗡\n' + \
                        'Лучники: ' + str(lost_arch) + ' / ' + str(self.player.war.archer) + ' 🏹\n' + \
                        'Маги: ' + str(lost_wiz) + ' / ' + str(self.player.war.wizard) + ' 🔮\n'
            if lost_war > 0 or lost_arch > 0 or lost_wiz > 0:
                bonus_mess += lost_mess

            self.player.war.warrior -= lost_war
            self.player.war.archer -= lost_arch
            self.player.war.wizard -= lost_wiz
            self.player.war.save(update_fields=['warrior', 'archer', 'wizard'])

        elif number == 1:
            rand = random.randint(1, 3)
            lost_part = 20
            if rand == 1:
                lost = self.player.war.warrior // lost_part
                self.player.war.warrior -= lost
                bonus_mess = 'Ваши 🗡 воины 🗡 не поделили найденный самородок золота!\nНачалась драка...\n'
                if lost > 0:
                    self.player.war.save(update_fields=['warrior'])
                    bonus_mess += str(lost) + ' 🗡 сорвалось в пропасть!\nВы приказали возвращаться.\n'
                else:
                    bonus_mess += 'Вы успокоили своё воиско и приказали возвращаться!\n'
            if rand == 2:
                lost = self.player.war.archer // lost_part
                self.player.war.archer -= lost
                bonus_mess = 'Ваши 🏹 лучники 🏹 не поделили найденный самородок золота!\nНачалась драка...\n'
                if lost > 0:
                    self.player.war.save(update_fields=['archer'])
                    bonus_mess += str(lost) + ' 🏹 сорвалось в пропасть!\nВы приказали возвращаться.\n'
                else:
                    bonus_mess += 'Вы успокоили своё воиско и приказали возвращаться!\n'
            if rand == 3:
                lost = self.player.war.wizard // lost_part
                self.player.war.wizard -= lost
                bonus_mess = 'Ваши 🔮 маги 🔮 не поделили найденный самородок золота!\nНачалась драка...\n'
                if lost > 0:
                    self.player.war.save(update_fields=['wizard'])
                    bonus_mess += str(lost) + ' 🔮 сорвалось в пропасть!\nВы приказали возвращаться.\n'
                else:
                    bonus_mess += 'Вы успокоили своё воиско и приказали возвращаться.\n'
        elif number == 2:
            bonus_mess = 'Вы долго шли по пещере и забрели в тупик!\nПровизия на исходе, вы приказали возвращаться!\n'
        elif number == 3:
            bonus_mess = 'Вы нашли проход на ' + str(lvl) + ' ур. пещер!\n'
        elif number == 4:
            self.player.energy += 2
            bonus_mess = 'Вы нашли Цветок Жизни! +2' + icon('energy') + '\n' + \
                         'Вы нашли проход на ' + str(lvl) + ' ур. пещер!\n'
            self.player.save(update_fields=['energy'])
        elif number == 5:
            chest = get_chest('cave_chest')
            add_chest(self.player, chest)
            bonus_mess = 'Вы нашли 🎁 Пещерный Сундук 🎁!\n' + \
                         'Вы нашли проход на ' + str(lvl) + ' ур. пещер!\n'
        elif number == 6:
            chest = get_chest('cave_chest')
            add_chest(self.player, chest, 3)
            bonus_mess = 'Вы нашли 3 🎁 Пещерных Сундуков 🎁!\n' + \
                         'Вы нашли проход на ' + str(lvl) + ' ур. пещер!\n'
        elif number == 7:
            chest = get_chest('cave_chest')
            add_chest(self.player, chest, 10)
            self.player.build.stock.res_add('diamond', 100)
            self.player.build.stock.gold += 200
            self.player.build.stock.res_add('iron', 200)
            self.player.build.stock.skull += 12
            self.player.build.stock.save(update_fields=['diamond', 'gold', 'iron', 'skull'])
            self.player.energy += 20
            self.player.place = 'cave'
            self.player.save(update_fields=['energy', 'place'])
            bonus_mess = 'Поздравляю!!!' + \
                         'Вы нашли сокровища Хранителя Подземелья!\n' + \
                         '+10 Пещерных сундуков 🎁\n' + \
                         '+200' + icon('iron') + '\n' + \
                         '+100' + icon('diamond') + '\n' + \
                         '+200' + icon('gold') + '\n' + \
                         '+10' + icon('skull') + '\n' + \
                         '+20' + icon('energy')

        return bonus_mess
