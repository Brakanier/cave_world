from django.db import models

from ..actions.functions import *
from ..actions.chests import *

import random
import json


class CaveMap(models.Model):

    cave_map = models.TextField(
        blank=True,
    )

    success = models.IntegerField(
        default=0,
    )

    @staticmethod
    def generate():
        cave_map = {}
        for level in range(1, 4):
            one = random.randint(3, 4)
            two = random.randint(3, 4)
            one, two = CaveMap.change(one, two)
            cave_map[level] = {
                1: one,
                2: two,
            }
        for level in range(4, 11):
            one = random.randint(2, 4)
            if one != 2:
                two = 2
            else:
                two = random.randint(3, 4)
            one, two = CaveMap.change(one, two)
            cave_map[level] = {
                1: one,
                2: two,
            }
        for level in range(11, 21):
            one = random.randint(1, 5)
            if one in (1, 2):
                two = random.randint(3, 5)
            else:
                two = random.randint(2, 3)
            one, two = CaveMap.change(one, two)
            cave_map[level] = {
                1: one,
                2: two,
            }
        for level in range(21, 26):
            one = random.randint(0, 6)
            if one in (0, 1, 2):
                two = random.randint(3, 6)
            else:
                two = random.randint(2, 3)
            one, two = CaveMap.change(one, two)
            cave_map[level] = {
                1: one,
                2: two,
            }
        for level in range(26, 30):
            one = random.randint(0, 6)
            if one in (0, 1, 2):
                two = random.randint(3, 6)
            else:
                two = random.randint(0, 2)
            one, two = CaveMap.change(one, two)
            cave_map[level] = {
                1: one,
                2: two,
            }

        for lvl in cave_map:
            print(str(lvl) + ' Право: ' + str(cave_map[lvl][1]) + ' | Лево: ' + str(cave_map[lvl][2]))
        cave_map = json.dumps(cave_map)
        return cave_map

    @staticmethod
    def change(one, two):
        rand = random.randint(0, 1)
        if rand == 1:
            one, two = two, one
        return one, two


class CaveProgress(models.Model):

    user_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )

    cave = models.ForeignKey(
        CaveMap,
        on_delete=models.SET(None),
        null=True,
    )

    level = models.IntegerField(
        default=0,
    )

    max_level = models.IntegerField(
        default=0,
    )

    def go(self, way):
        cave_lvl = self.level + 1
        cave_map = json.loads(self.cave.cave_map)
        bonus = cave_map[str(cave_lvl)][str(way)]
        print(cave_map[str(cave_lvl)])

        bonus_mess = self.cave_bonus(bonus)
        end_mess = ""

        if bonus == 0:
            end_mess = 'Вы вернулись домой!'
        elif bonus in (3, 4, 5, 6):
            self.level = cave_lvl
            end_mess = 'Пещера раздваивается, выберите путь:\n' + \
                       'Пещера Налево\n' + \
                       'Пещера Направо\n'
        if self.max_level < self.level:
            self.max_level = self.level
        message = bonus_mess + end_mess

    def go_left(self):
        level = self.level + 1
        pass

    def cave_bonus(self, number):
        bonus_mess = ""
        if number == 0:
            lost_part = 20
            lost_war = self.player.war.warrior // lost_part
            lost_arch = self.player.war.archer // lost_part
            lost_wiz = self.player.war.wizard // lost_part
            bonus_mess = 'Двигаясь по пещере вы нашли долину гейзеров.\n Кто ж знал, что пар с ядовитым газом...\n'
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
            lost_part = 100
            if rand == 1:
                lost = self.player.war.warrior // lost_part
                self.player.war.warrior -= lost
                bonus_mess = 'Ваши воины не поделили найденный самородок золота!\nНачалась драка...\n'
                if lost > 0:
                    self.player.war.save(update_fields=['warrior'])
                    bonus_mess += str(lost) + ' 🗡 сорвалось в пропасть!\nВы приказали возвращаться.\n'
                else:
                    bonus_mess += 'Вы успокоили своё воиско и приказали возвращаться!\n'
            if rand == 2:
                lost = self.player.war.archer // lost_part
                self.player.war.archer -= lost
                bonus_mess = 'Ваши лучники не поделили найденный самородок золота!\nНачалась драка...\n'
                if lost > 0:
                    self.player.war.save(update_fields=['archer'])
                    bonus_mess += str(lost) + ' 🏹 сорвалось в пропасть!\nВы приказали возвращаться.\n'
                else:
                    bonus_mess += 'Вы успокоили своё воиско и приказали возвращаться!\n'
            if rand == 3:
                lost = self.player.war.wizard // lost_part
                self.player.war.wizard -= lost
                bonus_mess = 'Ваши маги не поделили найденный самородок золота!\nНачалась драка...\n'
                if lost > 0:
                    self.player.war.save(update_fields=['wizard'])
                    bonus_mess += str(lost) + ' 🔮 сорвалось в пропасть!\nВы приказали возвращаться.\n'
                else:
                    bonus_mess += 'Вы успокоили своё воиско и приказали возвращаться.\n'
        elif number == 2:
            bonus_mess = 'Вы долго шли по пещере и забрели в тупик!\nПровизия на исходе, вы приказали возвращаться!\n'
        elif number == 3:
            bonus_mess = 'Вы нашли проход на следующий уровень пещер!\n'
        elif number == 4:
            self.player.energy += 2
            bonus_mess = 'Вы нашли Цветок Жизни! +2' + icon('energy')
            self.player.save(update_fields=['energy'])
        elif number == 5:
            chest = get_chest('cave_chest')
            add_chest(self.player, chest)
            bonus_mess = 'Вы нашли Пещерный Сундук!'
        elif number == 6:
            chest = get_chest('cave_chest')
            add_chest(self.player, chest, 5)
            bonus_mess = 'Вы нашли 5 Пещерных Сундуков!'
        elif number == 7:
            chest = get_chest('cave_chest')
            add_chest(self.player, chest, 10)
            bonus_mess = 'ВЫ НАШЛИ СОКРОВИЩА!!!\n' + \
                         '10 Пещерных сундуков\n' + \
                         '+5' + icon('exp') + '\n' + \
                         '+5' + icon('skull') + '\n' + \
                         '+20' + icon('energy')

        return bonus_mess
