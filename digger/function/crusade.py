
import random

from .CONSTANT import *
from .function import *


def crusade(player, action_time):
    player.place = 'crusade'
    player.save()
    message = "Вы собираетесь в поход. Советую освободить место на складе!"
    send(player=player, message=message, keyboard=get_keyboard(player=player, action_time=action_time))


def crusade_home(player):
    player.place = 'land'
    player.save()
    message = 'Вы успешно окончили свой поход и вернулись домой!'
    send(player=player, message=message)


def crusade_exit(player):
    player.place = 'land'
    player.army.warrior = round(player.army.warrior * 0.9)
    player.army.archer = round(player.army.archer * 0.9)
    player.army.wizard = round(player.army.wizard * 0.9)
    player.army.save()
    player.save()
    message = 'Вы сбежали с поля боя!\n' + \
              'Часть вашей армии осталось прикрывать отход...'
    send(player=player, message=message)


def crusade_wildman(player, action_time):
    time = action_time - player.crusade.crusade_last_time
    if time <= CRUSADE_TIME:
        hour = (CRUSADE_TIME - time) // 3600
        minutes = ((CRUSADE_TIME - time) - (hour * 3600)) // 60
        sec = (CRUSADE_TIME - time) - (minutes * 60) - (hour * 3600)
        message = 'Вы отдыхаете, еще: ' + str(hour) + ' ч. ' + str(minutes) + ' м. ' + str(sec) + ' сек.'
    else:
        player.crusade.crusade_last_time = action_time
        player.place = 'crusade_wildman'
        player.crusade.enemy = 'wildman'
        player.crusade.enemy_army = random.randint(1, CRUSADE_MAX)
        player.crusade.save()
        player.save()
        message = 'Вас заметили Дикари!\n' + \
                  'Количество: ' + str(player.crusade.enemy_army) + '\n' + \
                  'Выши действия?'

    send(player=player, message=message)


def crusade_rogue(player):
    player.place = 'crusade_rogue'
    player.crusade.enemy = 'rogue'
    player.crusade.enemy_army = random.randint(1, CRUSADE_MAX)
    player.crusade.save()
    player.save()
    message = 'Вас заметили Разбойники!\n' + \
              'Количество: ' + str(player.crusade.enemy_army) + '\n' + \
              'Выши действия?'
    send(player=player, message=message)


def crusade_golem(player):
    player.place = 'crusade_golem'
    golem_type = random.choice(GOLEM_TYPE)
    player.crusade.enemy = golem_type
    player.crusade.enemy_army = random.randint(1, CRUSADE_MAX)
    player.crusade.save()
    player.save()

    name = 'Големы'
    if golem_type == 'golem_s':
        name = 'Каменные Големы'
    elif golem_type == 'golem_i':
        name = 'Железные Големы'
    elif golem_type == 'golem_g':
        name = 'Золотые Големы'
    elif golem_type == 'golem_d':
        name = 'Алмазные Големы'

    message = 'Вас заметили ' + name + '!\n' + \
              'Количество: ' + str(player.crusade.enemy_army) + '\n' + \
              'Выши действия?'
    send(player=player, message=message)


def crusade_elemental(player):
    player.place = 'crusade_elemental'
    player.crusade.enemy = 'elemental'
    player.crusade.enemy_army = random.randint(1, CRUSADE_MAX)
    player.crusade.save()
    player.save()
    message = 'Вас заметили Элементали!\n' + \
              'Количество: ' + str(player.crusade.enemy_army) + '\n' + \
              'Выши действия?'
    send(player=player, message=message)


def crusade_attack(player):
    if player.crusade.enemy == '':
        message = 'Вы не в походе!'
    else:
        enemy_hp = 0
        enemy_attack = 0
        if player.crusade.enemy == 'wildman':
            enemy_attack = player.crusade.enemy_army * WILDMAN_ATTACK
            enemy_hp = player.crusade.enemy_army * WILDMAN_HP
        elif player.crusade.enemy == 'rogue':
            enemy_attack = player.crusade.enemy_army * ROGUE_ATTACK
            enemy_hp = player.crusade.enemy_army * ROGUE_HP
        elif player.crusade.enemy == 'golem_s' or 'golem_i' or 'golem_g' or 'golem_d':
            enemy_attack = player.crusade.enemy_army * GOLEM_ATTACK
            enemy_hp = player.crusade.enemy_army * GOLEM_HP
        elif player.crusade.enemy == 'elemental':
            enemy_attack = player.crusade.enemy_army * ELEMENTAL_ATTACK
            enemy_hp = player.crusade.enemy_army * ELEMENTAL_HP

        enemy_power = enemy_attack + enemy_hp

        # Армия игрока

        player_warrior_attack = player.army.warrior * WARRIOR_ATTACK
        player_warrior_hp = player.army.warrior * WARRIOR_HP
        player_archer_attack = player.army.archer * ARCHER_ATTACK
        player_archer_hp = player.army.archer * ARCHER_HP
        player_wizard_attack = player.army.wizard * WIZARD_ATTACK
        player_wizard_hp = player.army.wizard * WIZARD_HP
        player_attack = player_warrior_attack + player_archer_attack + player_wizard_attack
        player_hp = player_warrior_hp + player_archer_hp + player_wizard_hp

        # TOWER BUFF

        player_tower = player.build.tower_lvl * TOWER_BUFF * player_attack
        player_attack = player_attack + player_tower

        player_after_hp = player_hp - enemy_attack

        player_after_warrior = 0
        player_after_archer = 0
        player_after_wizard = 0
        if player_hp > 0 and player_after_hp > 0:
            player_after_warrior = ((player_warrior_hp / player_hp) * player_after_hp) // WARRIOR_HP
            player_after_archer = ((player_archer_hp / player_hp) * player_after_hp) // ARCHER_HP
            player_after_wizard = ((player_wizard_hp / player_hp) * player_after_hp) // WIZARD_HP
        player_lost_warrior = round(player.army.warrior - player_after_warrior)
        player_lost_archer = round(player.army.archer - player_after_archer)
        player_lost_wizard = round(player.army.wizard - player_after_wizard)

        if player_attack >= enemy_hp:

            # Победа Игрока

            wood = 0
            stone = 0
            iron = 0
            gold = 0
            diamond = 0

            if player.crusade.enemy == 'wildman':
                wood = round(enemy_power * CRUSADE_REWARD_X2 / 2)
                stone = round(enemy_power * CRUSADE_REWARD_X3 / 2)
            elif player.crusade.enemy == 'rogue':
                iron = round(enemy_power * CRUSADE_REWARD_X2 / 2)
                gold = round(enemy_power * CRUSADE_REWARD_X2 / 2)
            elif player.crusade.enemy == 'golem_s':
                stone = round(enemy_power * CRUSADE_REWARD_X1)
            elif player.crusade.enemy == 'golem_i':
                iron = round(enemy_power * CRUSADE_REWARD_X2)
            elif player.crusade.enemy == 'golem_g':
                gold = round(enemy_power * CRUSADE_REWARD_X2)
            elif player.crusade.enemy == 'golem_d':
                diamond = round(enemy_power * CRUSADE_REWARD_X1)
            elif player.crusade.enemy == 'elemental':
                wood = round(enemy_power * CRUSADE_REWARD_X2 / 4)
                stone = round(enemy_power * CRUSADE_REWARD_X3 / 4)
                iron = round(enemy_power * CRUSADE_REWARD_X2 / 4)
                gold = round(enemy_power * CRUSADE_REWARD_X2 / 4)
                diamond = round(enemy_power * CRUSADE_REWARD_X1 / 4)

            reward_exp = round(enemy_power / CRUSADE_REWARD_EXP)

            player.stock.wood = player.stock.wood + min(wood, player.stock.max - player.stock.wood)
            player.stock.stone = player.stock.stone + min(stone, player.stock.max - player.stock.stone)
            player.stock.iron = player.stock.iron + min(iron, player.stock.max - player.stock.iron)
            player.stock.gold = player.stock.gold + min(gold, player.stock.max - player.stock.gold)
            player.stock.diamond = player.stock.diamond + min(diamond, player.stock.max - player.stock.diamond)

            player = exp(player=player, exp=reward_exp)

            end = 'Лорд, продолжаем поход или возвращаемся домой?'

            if player.place == 'crusade_wildman':
                player.place = 'crusade_wildman_after'
            elif player.place == 'crusade_rogue':
                player.place = 'crusade_rogue_after'
            elif player.place == 'crusade_golem':
                player.place = 'crusade_golem_after'
            elif player.place == 'crusade_elemental':
                player.place = 'land'
                end = 'Вы успешно окончили свой поход и вернулись домой!'

            message = '⚔ Победа ⚔\n' + \
                      '[Ваши потери]\n' + \
                      'Воины: ' + str(player_lost_warrior) + ' / ' + str(player.army.warrior) + ' 🗡\n' + \
                      'Лучники: ' + str(player_lost_archer) + ' / ' + str(player.army.archer) + ' 🏹\n' + \
                      'Маги: ' + str(player_lost_wizard) + ' / ' + str(player.army.wizard) + ' 🔮\n' + \
                      '[Награда]\n' + \
                      'Дерево: ' + str(wood) + ' 🌲\n' + \
                      'Камень: ' + str(stone) + ' ◾\n' + \
                      'Железо: ' + str(iron) + ' ◽\n' + \
                      'Золото: ' + str(gold) + ' ✨\n' + \
                      'Алмазы: ' + str(diamond) + ' 💎\n' + \
                      'Опыт: ' + str(reward_exp) + ' 📚\n\n' + \
                      end

        else:

            # Поражение

            player.place = 'land'
            message = '⚔ Поражение ⚔\n' + \
                      '[Ваши потери]\n' + \
                      'Воины: ' + str(player_lost_warrior) + ' / ' + str(player.army.warrior) + ' 🗡\n' + \
                      'Лучники: ' + str(player_lost_archer) + ' / ' + str(player.army.archer) + ' 🏹\n' + \
                      'Маги: ' + str(player_lost_wizard) + ' / ' + str(player.army.wizard) + ' 🔮\n' + \
                      'Разбитая армия вернулась домой!'

        player.army.warrior = round(player_after_warrior)
        player.army.archer = round(player_after_archer)
        player.army.wizard = round(player_after_wizard)
        player.crusade.enemy = ''
        player.crusade.enemy_army = 0
        player.army.save()
        player.stock.save()
        player.crusade.save()
        player.save()
    send(player=player, message=message)
