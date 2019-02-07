
from ..models import Player

import random

from .CONSTANT import *
from .function import *


def find_enemy(vk, player, action_time, token):
    find_time = action_time - player.war.find_last_time
    if find_time >= FIND_TIME:
        enemy = Player.objects.filter(build__gate=True).exclude(user_id=player.user_id)

        def check_shield():
            shield = defender.war.shield * SHIELD_X
            shield = shield + defender.war.war_last_time
            if shield >= action_time:
                if len(enemy) > 1:
                    index = enemy.index(defender)
                    print(index)
                    enemy.pop(index)
                    return False
                return 'end'
            else:
                return True

        ready = False
        while not ready:
            defender = random.choice(enemy)
            ready = check_shield()
            # Условие выхода из цикла, если в enemy остался 1 элемент
            if ready == 'end':
                ready = True
                defender = False

        if defender:
            player.war.enemy_id = defender.user_id
            player.war.find_last_time = action_time
            player.war.save()
            message = 'Найден противник!\n' + \
                      'Ник: ' + defender.nickname + '\n' + \
                      'Уровень: ' + str(defender.lvl) + ' 👑\n' + \
                      'Успейте напасть, пока вас не опередили!'
        else:
            message = 'Противник не найден'
    else:
        min = find_time//60
        sec = find_time - (min * 60)
        message = 'Искать противника можно раз в 10 минут\n' + \
                  'До следующего поиска: ' + str(min) + ' м. ' + str(sec) + ' сек.'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
