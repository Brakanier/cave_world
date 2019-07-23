from django.db import models

from ..actions.functions import *
from ..actions.chests import *

import random
import json


class CaveMap(models.Model):

    cave_map = models.TextField(
        blank=True,
    )

    @staticmethod
    def generate():
        y = random.randint(5, 6)
        x = random.randint(5, 6)
        print('Y: ' + str(y) + ' X: ' + str(x))

        cave_map = [[0] * x for i in range(y)]

        ic = {
            'unknown': '🌫',
            'way': '🐾',
            'flower': '🍀',
            'chest': '📦',
            'stop': '🚧',
            'break': '🕳',
            'enemy': '🦇',
            'die': '☠',
            'down': '🚪',
            'enter': ''
        }
        events = {
            0: 'unknown',
            1: 'way',
            2: 'flower',
            3: 'chest',
            4: 'stop',
            5: 'break',
            6: 'enemy',
            7: 'die',
            8: 'down',
        }

        def gen_bad_event(y, x):
            event = random.randint(4, 7)
            event_y = random.randint(0, y - 1)
            event_x = random.randint(0, x - 1)
            print('Y: ' + str(y) + ' X: ' + str(x))
            if cave_map[event_y][event_x] == 0:
                print(events[event] + ' - Y: ' + str(event_y) + ' X: ' + str(event_x))
                cave_map[event_y][event_x] = event
            else:
                gen_bad_event(y, x)

        def down(y, x):
            event = 8
            event_y = random.randint(0, y - 1)
            event_x = random.randint(0, x - 1)
            if cave_map[event_y][event_x] == 0:
                print(events[event] + ' - Y: ' + str(event_y) + ' X: ' + str(event_x))
                cave_map[event_y][event_x] = event
                return event_y, event_x
            else:
                down(y, x)

        exit_y, exit_x = down(y, x)

        for i in range(min(y, x) - 1):
            if CaveMap.find_path(0, 0, exit_y, exit_x, y, x, cave_map):
                continue
            else:
                break

        def gen_good_event(x, y):
            event = random.randint(2, 3)
            event_y = random.randint(0, y - 1)
            event_x = random.randint(0, x - 1)
            if cave_map[event_y][event_x] == 0:
                print(events[event] + ' - Y: ' + str(event_y) + ' X: ' + str(event_x))
                cave_map[event_y][event_x] = event
            else:
                gen_good_event(x, y)

        for i in range(max(x, y)):
            gen_good_event(x, y)
        '''
        x_map = ''
        for y in cave_map:
            for x in y:
                x_map += ' ' + ic[events[x]] + ' '
            x_map += '\n'
        print(x_map)
        #cave_map = json.dumps(cave_map)
        '''
        return 'test'

    @staticmethod
    def change(one, two):
        rand = random.randint(0, 1)
        if rand == 1:
            one, two = two, one
        return one, two

    @staticmethod
    def find_path(enter_y, enter_x, exit_y, exit_x, size_y, size_x, cave_map):

        # Нормализация
        for y in range(len(cave_map)):
            for x in range(len(cave_map[y])):
                if cave_map[y][x] in [4, 5, 6, 7]:
                    cave_map[y][x] = -2
                else:
                    cave_map[y][x] = 0

        cave_map[enter_y][enter_x] = 1
        cave_map[exit_y][exit_x] = -1

        wave = 1
        for i in range(len(cave_map) * len(cave_map[0])):
            wave += 1
            for y in range(len(cave_map)):
                for x in range(len(cave_map[y])):
                    if cave_map[y][x] == -2:
                        continue
                    if cave_map[y][x] == wave - 1:
                        if y > 0 and cave_map[y - 1][x] == 0:
                            cave_map[y - 1][x] = wave
                        if y < (len(cave_map) - 1) and cave_map[y + 1][x] == 0:
                            cave_map[y + 1][x] = wave
                        if x > 0 and cave_map[y][x - 1] == 0:
                            cave_map[y][x - 1] = wave
                        if x < (len(cave_map[y]) - 1) and cave_map[y][x + 1] == 0:
                            cave_map[y][x + 1] = wave

                        if (abs(y - exit_y) + abs(x - exit_x)) == 1:
                            cave_map[exit_y][exit_x] = wave
                            x_map = ''
                            for n in range(len(cave_map)):
                                for m in range(len(cave_map[n])):
                                    x_map += ' ' + str(cave_map[n][m]) + ' '
                                x_map += '\n'
                            print(x_map)
                            return True
        return False


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
    success = models.IntegerField(
        default=0,
        db_index=True,
    )
    time = models.BigIntegerField(
        default=0,
    )

    def info(self):
        start_mess = ''
        if self.player.place == 'cave_go':
            start_mess = 'Вы сейчас на ' + str(self.level) + ' ур. пещер.\n'

        mess = start_mess
        mess += 'Вы доходили максимум до ' + str(self.max_level) + ' ур. этой пещеры.\n' + \
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
        self.max_level = 1
        self.time = action_time + 3600
        self.save(update_fields=['max_level', 'level', 'cave', 'time'])
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
