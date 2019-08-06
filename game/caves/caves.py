from ..models.cave import CaveProgress, CaveMap
from ..actions.chests import *

import random
import json


class CaveManager:

    def __init__(self, player):
        self.direction = None
        self.__get_or_create_cave()
        # Небольшой костыль, раньше по умолчанию уровнь был 0, теперь начинается с 1
        if player.cave_progress.level == 0:
            player.cave_progress.level = 1
        self.level = player.cave_progress.level
        self.level_map = self.full_cave[str(self.level)]['map']
        self.level_enter = self.full_cave[str(self.level)]['enter']
        self.level_exit = self.full_cave[str(self.level)]['exit']
        self.time = player.cave_progress.time
        self.y = player.cave_progress.y
        self.x = player.cave_progress.x
        self.player_map = {}
        self.__get_player_map(player)


    def move(self, player, command):
        old_y = self.y
        old_x = self.x
        if player.place not in ('cave_go', 'cave_down', 'cave_up'):
            return 'Вы не в пещерах!'
        if not self.check_command(command):
            return 'Неверная команда перемещения!'
        if not self.check_direction:
            return 'Невозможно двигаться в эту сторону!'
        if not player.cave_progress.cave:
            player.cave_progress.cave = CaveMap.objects.get()
            player.cave_progress.time = 0
            player.cave_progress.y = None
            player.cave_progress.x = None
            player.cave_progress.level = 1
            player.cave_progress.save(update_fields=['cave', 'time'])
            player.place = 'cave'
            player.save(update_fields=['place'])
            return 'Кто-то нашёл сокровища...\n' + \
            'Произошёл обвал...\n' + \
            'Пути в пещерах изменились, начните исследование заново!\n' + \
            '- Пещеры войти'

        self.__move_coords()

        old_event = self.get_event(old_y, old_x)
        if old_event in (0, 1):
            self.player_map[str(self.level)]['map'][old_y][old_x] = 1

        event = self.get_event(self.y, self.x)
        event_mess = self.__use_event(player, event)
        
        player.cave_progress.level = self.level
        player.cave_progress.y = self.y
        player.cave_progress.x = self.x
        player.cave_progress.player_map = json.dumps(self.player_map)
        player.cave_progress.save(update_fields=['y', 'x', 'player_map', 'level'])
        if event == 8:
            if self.level == 10:
                player.cave_progress.cave.delete()
        return self.draw_level(self.player_map) + event_mess

    def go_up(self, player):
        if player.place not in ('cave_go', 'cave_down', 'cave_up'):
            return 'Вы не в пещерах!'
        if not player.cave_progress.cave:
            player.cave_progress.cave = CaveMap.objects.get()
            player.cave_progress.time = 0
            player.cave_progress.y = None
            player.cave_progress.x = None
            player.cave_progress.level = 1
            player.cave_progress.save(update_fields=['cave', 'time'])
            player.place = 'cave'
            player.save(update_fields=['place'])
            return 'Кто-то нашёл сокровища...\n' + \
            'Произошёл обвал...\n' + \
            'Пути в пещерах изменились, начните исследование заново!\n' + \
            '- Пещеры войти'

        self.level -= 1
        self.level_exit = self.full_cave[str(self.level)]['exit']
        self.y = self.level_exit[0]
        self.x = self.level_exit[1]
        self.player_map[str(self.level)]['map'][self.level_exit[0]][self.level_exit[1]] = 8
        player.cave_progress.level = self.level
        player.cave_progress.y = self.y
        player.cave_progress.x = self.x
        player.cave_progress.player_map = json.dumps(self.player_map)
        player.cave_progress.save(update_fields=['level', 'y', 'x', 'player_map'])
        player.place = 'cave_go'
        player.save(update_fields=['place'])
        event_mess = 'Вы поднялись на ' + str(self.level) + ' уровень!\nВыберите в какую сторону идти\n'
        return self.draw_level(self.player_map) + event_mess
    
    def go_down(self, player):
        if player.place not in ('cave_go', 'cave_down', 'cave_up'):
            return 'Вы не в пещерах!'
        if not player.cave_progress.cave:
            player.cave_progress.cave = CaveMap.objects.get()
            player.cave_progress.time = 0
            player.cave_progress.y = None
            player.cave_progress.x = None
            player.cave_progress.level = 1
            player.cave_progress.save(update_fields=['cave', 'time'])
            player.place = 'cave'
            player.save(update_fields=['place'])
            return 'Кто-то нашёл сокровища...\n' + \
            'Произошёл обвал...\n' + \
            'Пути в пещерах изменились, начните исследование заново!\n' + \
            '- Пещеры войти'
        
        self.level += 1
        self.level_enter = self.full_cave[str(self.level)]['enter']
        self.y = self.level_enter[0]
        self.x = self.level_enter[1]
        self.player_map[str(self.level)]['map'][self.level_enter[0]][self.level_enter[1]] = 9
        player.cave_progress.level = self.level
        player.cave_progress.y = self.y
        player.cave_progress.x = self.x
        player.cave_progress.player_map = json.dumps(self.player_map)
        player.cave_progress.save(update_fields=['level', 'y', 'x', 'player_map'])
        player.place = 'cave_go'
        player.save(update_fields=['place'])
        event_mess = 'Вы спустились на ' + str(self.level) + ' уровень!\nВыберите в какую сторону идти\n'
        return self.draw_level(self.player_map) + event_mess

    def __is_known_event(self, event):
        if self.player_map[str(self.level)]['map'][self.y][self.x] == event:
            return True
        else:
            return False

    def __use_event(self, player, event):
        event_mess = ''
        if event in (0, 1):
            event_mess = ''
            player.place = 'cave_go'
        elif event == 2:
            if self.__is_known_event(event):
                event_mess = 'Вы тут уже были!'
            else:
                event_mess = 'Вы нашли Цветок Жизни +2 ⚡'
                player.energy += 2
                player.save(update_fields=['energy'])
            player.place = 'cave_go'
        elif event == 3:
            if self.__is_known_event(event):
                event_mess = 'Вы тут уже были!'
            else:
                event_mess = 'Вы нашли Пещерный сундук 🎁'
                chest = get_chest('cave_chest')
                add_chest(player, chest)
            player.place = 'cave_go'
        elif event == 5:
            event_mess = 'Вы забрели в тупик.\nВы и ваша армия измотаны, пришлось вернуться домой.'
            player.place = 'cave'
            player.save(update_fields=['place'])
        elif event == 6:
            event_mess = '- Что это за хрип?\n - Заблудшие!\n\n'
            mind = random.randint(0, 1)
            mind_mess = '\n\nЛорд! В какую сторону отступать!?'
            if mind:
                player.place = 'cave'
                mind_mess = '- Лорд потерял сознание!\n- Хватайте его и убираемся отсюда!!!\nВас вернули домой...'
            lost_part = 10
            lost_war = player.war.warrior // lost_part
            lost_arch = player.war.archer // lost_part
            lost_wiz = player.war.wizard // lost_part
            lost_mess = '[Ваши потери]\n' + \
            'Воины: ' + str(lost_war) + ' / ' + str(player.war.warrior) + ' 🗡\n' + \
            'Лучники: ' + str(lost_arch) + ' / ' + str(player.war.archer) + ' 🏹\n' + \
            'Маги: ' + str(lost_wiz) + ' / ' + str(player.war.wizard) + ' 🔮'

            if lost_war > 0 or lost_arch > 0 or lost_wiz > 0:
                event_mess += lost_mess
            event_mess += mind_mess
            player.war.warrior -= lost_war
            player.war.archer -= lost_arch
            player.war.wizard -= lost_wiz
            player.war.save(update_fields=['warrior', 'archer', 'wizard'])
            #TODO сражение с заблудшими
            player.place = 'cave_go'
        elif event == 7:
            lost_part = 20
            lost_war = player.war.warrior // lost_part
            lost_arch = player.war.archer // lost_part
            lost_wiz = player.war.wizard // lost_part
            event_mess = 'Двигаясь по пещере вы нашли долину гейзеров.\nКто ж знал, что пар с ядовитым газом...\n'
            lost_mess = '[Ваши потери]\n' + \
            'Воины: ' + str(lost_war) + ' / ' + str(player.war.warrior) + ' 🗡\n' + \
            'Лучники: ' + str(lost_arch) + ' / ' + str(player.war.archer) + ' 🏹\n' + \
            'Маги: ' + str(lost_wiz) + ' / ' + str(player.war.wizard) + ' 🔮\n\n' + \
            'Вы вернулись домой, чтобы вылечить ожоги...'

            if lost_war > 0 or lost_arch > 0 or lost_wiz > 0:
                event_mess += lost_mess

            player.war.warrior -= lost_war
            player.war.archer -= lost_arch
            player.war.wizard -= lost_wiz
            player.war.save(update_fields=['warrior', 'archer', 'wizard'])
            player.place = 'cave'
            player.save(update_fields=['place'])
        elif event == 8:
            if self.level == 10:
                chest = get_chest('cave_chest')
                add_chest(player, chest, 10)
                player.build.stock.stone += 500
                player.build.stock.wood += 500
                player.build.stock.iron += 250
                player.build.stock.diamond += 500
                player.build.stock.gold += 500
                player.build.stock.skull += 10
                player.build.stock.save(update_fields=['stone', 'wood', 'iron', 'diamond', 'gold', 'skull'])
                player.energy += 20
                player.save(update_fields=['energy'])
                event_mess = 'Поздравляю!!!\n' + \
                'Вы нашли сокровища Хранителя Подземелья!\n' + \
                '+10 Пещерных сундуков 🎁\n' + \
                '+500 ◾\n' + \
                '+500 🌲\n' + \
                '+250 ◽\n' + \
                '+500 ✨\n' + \
                '+10 💀\n' + \
                '+20 ⚡'
                player.place = 'cave'
            else:
                event_mess = 'Вы нашли спуск на следующий уровень пещер!\n' + \
                'Хотите спуститься на ' + str(self.level + 1) + ' уровень?'
                player.place = 'cave_down'
        elif event == 9:
            if self.level > 1:
                event_mess = 'Здесь вы спустились на этот уровень.\n' + \
                'Хотите подняться на ' + str(self.level - 1) + ' уровень?'
                player.place = 'cave_up'
        player.save(update_fields=['place'])
        # Проверяем событие, чтобы записать в карту игрока
        if event < 2:
            self.player_map[str(self.level)]['map'][self.y][self.x] = 1
        else:
            self.player_map[str(self.level)]['map'][self.y][self.x] = event
        return event_mess

    def __set_player_map(self):
        print('Установка карты игроку')
        full_map = self.full_cave
        for lvl in full_map:
            for y in range(len(full_map[lvl]['map'])):
                for x in range(len(full_map[lvl]['map'][y])):
                    full_map[lvl]['map'][y][x] = 0
        self.player_map = full_map
        
    def __get_player_map(self, player):
        if player.cave_progress.player_map:
            self.player_map = json.loads(player.cave_progress.player_map)
        else:
            self.__set_player_map()

    def start(self, player, action_time):
        if action_time < player.cave_progress.time:
            cave_time = player.cave_progress.time - action_time
            sec = cave_time
            minutes = sec // 60
            hour = minutes // 60
            time_mess = 'В пещеры можно отправиться раз в час.\n' + \
                        'До следующего раза: ' + \
                        str(hour % 24) + ' ч. ' + \
                        str(minutes % 60) + ' м. ' + \
                        str(sec % 60) + ' сек. ⏳'
            return time_mess
        mess = ''

        self.level = 1
        self.level_map = self.full_cave['1']['map']
        self.level_enter = self.full_cave['1']['enter']
        self.level_exit = self.full_cave['1']['exit']
        self.y = self.level_enter[0]
        self.x = self.level_enter[1]

        if not player.cave_progress.cave:
            player.cave_progress.cave = CaveMap.objects.get()
            self.__set_player_map()
            mess = 'Пещеры изменились!\n\n'

        self.player_map[str(self.level)]['map'][self.level_enter[0]][self.level_enter[1]] = 9
        player.cave_progress.y = self.y
        player.cave_progress.x = self.x
        player.cave_progress.level = 1
        player.cave_progress.time = action_time + 3600
        player.cave_progress.player_map = json.dumps(self.player_map)
        # TODO Вернуть сохранение времени входа
        player.cave_progress.save(update_fields=['level', 'cave', 'player_map', 'y', 'x'])
        player.place = 'cave_go'
        player.save(update_fields=['place'])
        mess += 'Вы зашли в пещеры!\n' + \
                'Вы сейчас на ' + str(player.cave_progress.level) + ' ур. пещер.\n' + \
                'Выберите в какую сторону идти\n'
        
        mess = self.draw_level(self.player_map) + mess
        return mess

    def draw_level(self, cave_map):
        lvl = str(self.level)
        ic = {
            'unknown': '🌫',
            'way': '🐾',
            'flower': '🍀',
            'chest': '🎁',
            'stop': '🚧',
            'enemy': '👻',
            'die': '☠',
            'exit': '🕳',
            'enter': '📍',
            'lord': '🤴',
            'used_flower': '🍁',
            'used_chest': '📦',
        }
        events = {
            -3: 'used_chest',
            -2: 'used_flower',
            0: 'unknown',
            1: 'way',
            2: 'flower',
            3: 'chest',
            5: 'stop',
            6: 'enemy',
            7: 'die',
            8: 'exit',
            9: 'enter',
            10: 'lord',
        }
        print('Enter - Y: ' + str(cave_map[lvl]['enter'][0]) + ' X: ' + str(cave_map[lvl]['enter'][1]))
        print('Exit - Y: ' + str(cave_map[lvl]['exit'][0]) + ' X: ' + str(cave_map[lvl]['exit'][1]))
        x_map = ''
        #cave_map[lvl]['map'][cave_map[lvl]['enter'][0]][cave_map[lvl]['enter'][1]] = 9
        #cave_map[lvl]['map'][cave_map[lvl]['exit'][0]][cave_map[lvl]['exit'][1]] = 8
        cave_map[lvl]['map'][self.y][self.x] = 10

        for x in range(len(cave_map[lvl]['map'][0])):
            x_map += '⬛'
        x_map += '⬛⬛\n'
        for y in range(len(cave_map[lvl]['map'])):
            x_map += '⬛'
            for x in range(len(cave_map[lvl]['map'][y])):
                x_map += ic[events[cave_map[lvl]['map'][y][x]]]
            x_map += '⬛\n'

        for x in range(len(cave_map[lvl]['map'][0])):
            x_map += '⬛'
        x_map += '⬛⬛\n\n'

        print(x_map)
        lvl_mess = 'Пещера - ' + lvl + ' ур.\n'
        return lvl_mess + x_map

    def get_event(self, y, x):
        return self.level_map[y][x]

    def __move_coords(self):
        if self.direction == 'top':
            self.y -= 1
            return True
        elif self.direction == 'right':
            self.x += 1
            return True
        elif self.direction == 'left':
            self.x -= 1
            return True
        elif self.direction == 'bottom':
            self.y += 1
            return True
        else:
            return False

    def check_command(self, command):
        # Проверяет команду перемещения и задаёт направление
        allow_command = (
            'север',
            'с',
            'восток',
            'в',
            'запад',
            'з',
            'юг',
            'ю',
        )
        part = command.split()
        if part[1] in allow_command:
            if part[1] in ('север', 'с'):
                if self.y > 0:
                    self.direction = 'top'
                    return True
            elif part[1] in ('восток', 'в'):
                if self.x < len(self.level_map[self.y]) - 1:
                    self.direction = 'right'
                    return True
            elif part[1] in ('запад', 'з'):
                if self.x > 0:
                    self.direction = 'left'
                    return True
            elif part[1] in ('юг', 'ю'):
                if self.y < len(self.level_map) - 1:
                    self.direction = 'bottom'
                    return True

            return False
        else:
            return False

    def check_direction(self):
        # Проверяет возможность перемещения в заданном направлении
        if self.direction == 'top':
            if self.y > 0:
                return True
        elif self.direction == 'right':
            if self.x < len(self.level_map[self.y]) - 1:
                return True
        elif self.direction == 'left':
            if self.x > 0:
                return True
        elif self.direction == 'bottom':
            if self.y < len(self.level_map) - 1:
                return True
        return False

    def __get_or_create_cave(self):
        try:
            cave_map = CaveMap.objects.get()
            self.full_cave = json.loads(cave_map.cave_map)
        except CaveMap.DoesNotExist:
            gen = CaveGenerator()
            full_cave = gen.generate()
            model_cave_map = CaveMap.objects.create()
            model_cave_map.cave_map = json.dumps(full_cave)
            model_cave_map.save()
            self.full_cave = full_cave


class CaveGenerator:

    def __init__(self):
        self.size = ()  # размеры пещеры
        self.enter = ()  # точка входа
        self.exit = ()  # точка выхода
        self.cave_map = []  # карта
        self.bad_points = []  # пустые клетки для плохих событий
        self.good_points = []  # пустые клетки для хороших событий
        self.full_map = {}  # итоговая карта

    def gen_null(self):
        self.size = ()
        self.enter = ()
        self.exit = ()
        self.cave_map = []
        self.bad_points = []
        self.good_points = []

    def generate(self):
        # максимум по ширине 8 символов, 2 из них рамка
        y =  random.randint(4, 6)
        x = random.randint(4, 8)
        for i in range(10):
            self.gen_null()
            self.enter = (0, 0)
            self.exit = (0, 0)
            self.size = (y, x)
            self.cave_map = [[0] * self.size[1] for i in range(self.size[0])]
            self.gen_enter_exit()
            self.find_path()
            self.path_to_map()
            self.gen_good_points()
            self.gen_good_events(i + 1)
            self.gen_bad_points()
            self.gen_bad_events(i + 1)
            self.full_map[str(i + 1)] = {}
            self.full_map[str(i + 1)]['map'] = self.cave_map
            self.full_map[str(i + 1)]['enter'] = self.enter
            self.full_map[str(i + 1)]['exit'] = self.exit
            self.full_map[str(i + 1)]['map'][self.exit[0]][self.exit[1]] = 8
            self.full_map[str(i + 1)]['map'][self.enter[0]][self.enter[1]] = 9
        return self.full_map

    def gen_enter_exit(self):
        directions = ['top', 'bottom', 'right', 'left']
        path = random.choice(directions)
        if path == 'top':
            self.enter = (self.size[0] - 1, random.randint(0, self.size[1] - 1))
            self.exit = (0, random.randint(0, self.size[1] - 1))
        elif path == 'bottom':
            self.enter = (0, random.randint(0, self.size[1] - 1))
            self.exit = (self.size[0] - 1, random.randint(0, self.size[1] - 1))
        elif path == 'right':
            self.enter = (random.randint(0, self.size[0] - 1), 0)
            self.exit = (random.randint(0, self.size[0] - 1), self.size[1] - 1)
        elif path == 'left':
            self.enter = (random.randint(0, self.size[0] - 1), self.size[1] - 1)
            self.exit = (random.randint(0, self.size[0] - 1), 0)

    def find_path(self):
        self.cave_map[self.enter[0]][self.enter[1]] = 1
        self.cave_map[self.exit[0]][self.exit[1]] = -1
        wave = 1
        for i in range(len(self.cave_map) * len(self.cave_map[0])):
            wave += 1
            for y in range(len(self.cave_map)):
                for x in range(len(self.cave_map[y])):
                    if self.cave_map[y][x] == wave - 1:
                        if y > 0 and self.cave_map[y - 1][x] == 0:
                            self.cave_map[y - 1][x] = wave
                        if y < (len(self.cave_map) - 1) and self.cave_map[y + 1][x] == 0:
                            self.cave_map[y + 1][x] = wave
                        if x > 0 and self.cave_map[y][x - 1] == 0:
                            self.cave_map[y][x - 1] = wave
                        if x < (len(self.cave_map[y]) - 1) and self.cave_map[y][x + 1] == 0:
                            self.cave_map[y][x + 1] = wave

                        if (abs(y - self.exit[0]) + abs(x - self.exit[1])) == 1:
                            self.cave_map[self.exit[0]][self.exit[1]] = wave
                            return True
        return False

    def path_to_map(self):
        y = self.exit[0]
        x = self.exit[1]
        wave = self.cave_map[y][x]
        while wave > 2:
            wave -= 1
            if y > 0 and self.cave_map[y-1][x] == wave:
                y -= 1
                self.cave_map[y][x] = 1
            elif y < (len(self.cave_map) - 1) and self.cave_map[y + 1][x] == wave:
                y += 1
                self.cave_map[y][x] = 1
            elif x > 0 and self.cave_map[y][x - 1] == wave:
                x -= 1
                self.cave_map[y][x] = 1
            elif x < (len(self.cave_map[y]) - 1) and self.cave_map[y][x + 1] == wave:
                x += 1
                self.cave_map[y][x] = 1

    def gen_good_points(self):
        self.cave_map[self.enter[0]][self.enter[1]] = 1
        self.cave_map[self.exit[0]][self.exit[1]] = 1
        for y in range(len(self.cave_map)):
            for x in range(len(self.cave_map[y])):
                if self.cave_map[y][x] != 1:
                    self.cave_map[y][x] = 0
                if y == self.enter[0] and x == self.enter[1]:
                    continue
                elif y == self.exit[0] and x == self.exit[1]:
                    continue
                point = (y, x)
                self.good_points.append(point)

    def gen_good_events(self, lvl):
        if lvl < 5:
            complexity = 1
        else:
            complexity = 2
        chests = 0
        flowers = 0
        count = len(self.good_points) // (5 - complexity )
        for c in range(count):
            if chests < count // 2:
                chests += 1
                point_i = random.randint(0, len(self.good_points) - 1)
                point = self.good_points.pop(point_i)
                self.cave_map[point[0]][point[1]] = 3
            else:
                flowers += 1
                point_i = random.randint(0, len(self.good_points) - 1)
                point = self.good_points.pop(point_i)
                self.cave_map[point[0]][point[1]] = 2

    def gen_bad_points(self):
        for y in range(len(self.cave_map)):
            for x in range(len(self.cave_map[y])):
                if self.cave_map[y][x] == 0:
                    point = (y, x)
                    self.bad_points.append(point)

    def gen_bad_events(self, lvl):
        if lvl < 5:
            complexity = 1
        else:
            complexity = 2
        count = len(self.bad_points) // (4 - complexity)
        enemy = 0
        for c in range(count):
            if enemy < complexity:
                event_num = random.choice((5, 6, 7))
            else:
                event_num = random.choice((5, 7))
            if event_num == 6:
                enemy += 1
            point_i = random.randint(0, len(self.bad_points) - 1)
            point = self.bad_points[point_i]
            self.cave_map[point[0]][point[1]] = event_num

    def draw_path(self):
        ic = {
            'unknown': '🌫',
            'way': '🐾',
            'flower': '🍀',
            'chest': '📦',
            'stop': '🚧',
            'enemy': '🦇',
            'die': '☠',
            'down': '🕳',
            'enter': '📍'
        }
        events = {
            0: 'unknown',
            1: 'way',
            2: 'flower',
            3: 'chest',
            4: 'stop',
            6: 'enemy',
            7: 'die',
            8: 'down',
            9: 'enter',
        }
        print('Enter - Y: ' + str(self.enter[0]) + ' X: ' + str(self.enter[1]))
        print('Exit - Y: ' + str(self.exit[0]) + ' X: ' + str(self.exit[1]))
        x_map = ''
        self.cave_map[self.enter[0]][self.enter[1]] = 9
        self.cave_map[self.exit[0]][self.exit[1]] = 8
        for y in range(len(self.cave_map)):
            for x in range(len(self.cave_map[y])):
                x_map += ic[events[self.cave_map[y][x]]] + ' '
            x_map += '\n'
        print(x_map)

        return x_map

