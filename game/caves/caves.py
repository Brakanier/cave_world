import random


class CaveManager():

    def __init__(self):
        pass


class CaveGenerator():

    def __init__(self, y=5, x=5):
        self.size = (y, x)
        self.y = y
        self.x = x
        self.cave_map = [[0] * self.size[1] for i in range(self.size[0])]
        self.first_points = [[y, x] for y in range(self.size[0]) for x in range(self.size[1])]
        self.second_points = self.first_points.copy()
        self.enter = (0, 0)
        self.exit = (0, 0)

    def gen_enter_exit(self):
        self.enter = self.first_points.pop(random.randint(0, len(self.first_points) - 1))
        self.exit = self.first_points.pop(random.randint(0, len(self.first_points) - 1))
        if self.enter != self.exit:
            self.cave_map[self.enter[0]][self.enter[1]] = 1
            self.cave_map[self.exit[0]][self.enter[1]] = -1
        else:
            self.gen_enter_exit()

    def find_path(self):
        wave = 1
        for i in range(len(self.cave_map) * len(self.cave_map[0])):
            wave += 1
            for y in range(len(self.cave_map)):
                for x in range(len(self.cave_map[y])):
                    if self.cave_map[y][x] == -2:
                        continue
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

    def draw_path(self):
        print('Enter - Y: ' + str(self.enter[0]) + ' X: ' + str(self.enter[1]))
        print('Exit - Y: ' + str(self.exit[0]) + ' X: ' + str(self.exit[1]))
        x_map = ''
        for y in range(len(self.cave_map)):
            for x in range(len(self.cave_map[y])):
                x_map += ' ' + str(self.cave_map[y][x]) + ' '
            x_map += '\n'
        print(x_map)
        return x_map
