
from ..models import Player

import random

from .CONSTANT import *
from .function import *


def find_enemy(vk, player, action_time, token):
    find_time = action_time - player.war.find_last_time
    if find_time >= FIND_TIME:
        enemy = Player.objects.filter(build__gate=True).exclude(user_id=player.user_id)

        defender = None

        def is_shield():
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
        find = True
        while not ready:
            defender = random.choice(enemy)
            ready = is_shield()
            # Условие выхода из цикла, если в enemy остался 1 элемент
            if ready == 'end':
                ready = True
                find = False

        if find:
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
        minutes = (FIND_TIME - find_time) // 60
        sec = (FIND_TIME - find_time) - (minutes * 60)
        message = 'Искать противника можно раз в 10 минут\n' + \
                  'До следующего поиска: ' + str(minutes) + ' м. ' + str(sec) + ' сек.'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def attack(vk, player, action_time, token):
    war_time = action_time - player.war.war_last_time
    if war_time >= WAR_TIME:
        if player.war.enemy_id:

            # Проверка противника на наличие щита

            defender = Player.objects.get(user_id=player.war.enemy_id)

            def is_shield():
                shield = defender.war.shield * SHIELD_X
                shield = shield + defender.war.war_last_time
                if shield >= action_time:
                    return True
                else:
                    return False
            if is_shield():
                message = 'Вы опоздали!\n' + \
                          'На ' + defender.nickname + ' уже напали!\n' + \
                          'Найдите нового противника!'
                player.war.enemy_id = None
                player.war.save()
            else:
                # Сражение

                # Атакующи
                attack_warrior_attack = player.army.warrior * player.army.warrior_attack
                attack_warrior_hp = player.army.warrior * player.army.warrior_hp
                attack_archer_attack = player.army.archer * player.army.archer_attack
                attack_archer_hp = player.army.archer * player.army.archer_hp
                attack_wizard_attack = player.army.wizard * player.army.wizard_attack
                attack_wizard_hp = player.army.wizard * player.army.wizard_hp
                attack_attack = attack_warrior_attack + attack_archer_attack + attack_wizard_attack
                attack_hp = attack_warrior_hp + attack_archer_hp + attack_wizard_hp
                attack_power = attack_attack + attack_hp

                # Защитник
                defender_warrior_attack = defender.army.warrior * defender.army.warrior_attack
                defender_warrior_hp = defender.army.warrior * defender.army.warrior_hp
                defender_archer_attack = defender.army.archer * defender.army.archer_attack
                defender_archer_hp = defender.army.archer * defender.army.archer_hp
                defender_wizard_attack = defender.army.wizard * defender.army.wizard_attack
                defender_wizard_hp = defender.army.wizard * defender.army.wizard_hp
                defender_attack = defender_warrior_attack + defender_archer_attack + defender_wizard_attack
                defender_hp = defender_warrior_hp + defender_archer_hp + defender_wizard_hp

                # Остатки армий

                attack_after_hp = attack_hp - defender_attack
                defender_after_hp = defender_hp - attack_hp

                attack_after_warrior = 0
                attack_after_archer = 0
                attack_after_wizard = 0
                if attack_hp > 0:
                    attack_after_warrior = (player.army.warrior / attack_hp) * max(attack_after_hp, 0)
                    attack_after_archer = (player.army.archer / attack_hp) * max(attack_after_hp, 0)
                    attack_after_wizard = (player.army.wizard / attack_hp) * max(attack_after_hp, 0)
                attack_lost_warrior = player.army.warrior - attack_after_warrior
                attack_lost_archer = player.army.archer - attack_after_archer
                attack_lost_wizard = player.army.wizard - attack_after_wizard

                defender_after_warrior = 0
                defender_after_archer = 0
                defender_after_wizard = 0
                if defender_hp > 0:
                    defender_after_warrior = (defender.army.warrior / defender_hp) * max(defender_after_hp, 0)
                    defender_after_archer = (defender.army.archer / defender_hp) * max(defender_after_hp, 0)
                    defender_after_wizard = (defender.army.wizard / defender_hp) * max(defender_after_hp, 0)
                defender_lost_warrior = defender.army.warrior - defender_after_warrior
                defender_lost_archer = defender.army.archer - defender_after_archer
                defender_lost_wizard = defender.army.wizard - defender_after_wizard
                defender_lost_army = defender_lost_warrior + defender_lost_archer + defender_lost_wizard

                if attack_attack >= defender_attack:

                    # Победа нападавшего

                    # Награда

                    reward = (attack_power // REWARD_Y)
                    reward_part = (reward // REWARD_PART)
                    reward_stone = min(defender.stock.wood, (reward_part * WOOD_PART))
                    reward_wood = min(defender.stock.wood, (reward_part * WOOD_PART))
                    reward_iron = min(defender.stock.iron, (reward_part * IRON_PART))
                    reward_gold = min(defender.stock.gold, (reward_part * GOLD_PART))
                    reward_diamond = min(defender.stock.diamond, (reward_part * DIAMOND_PART))
                    reward_skull = 1
                    reward_exp = defender_lost_army // REWARD_EXP_Y
                    player = exp(vk=vk, player=player, token=token, exp=reward_exp)

                    # Забираем у проигравшего

                    defender.stock.stone = defender.stock.stone - reward_stone
                    defender.stock.wood = defender.stock.wood - reward_wood
                    defender.stock.iron = defender.stock.iron - reward_iron
                    defender.stock.gold = defender.stock.gold - reward_gold
                    defender.stock.diamond = defender.stock.diamond - reward_diamond

                    # Выдаём победителю

                    player.stock.stone = player.stock.stone + reward_stone
                    player.stock.wood = player.stock.wood + reward_wood
                    player.stock.iron = player.stock.iron + reward_iron
                    player.stock.gold = player.stock.gold + reward_gold
                    player.stock.diamond = player.stock.diamond + reward_diamond
                    player.stock.skull = player.stock.skull + reward_skull

                    message = 'Вы напали на ' + defender.nickname + ' !' + \
                              '⚔ Победа ⚔\n' + \
                              '<Ваши потери>\n' + \
                              'Воины: ' + str(attack_lost_warrior) + '/' + str(player.army.warrior) + ' 🗡\n' + \
                              'Лучники: ' + str(attack_lost_archer) + '/' + str(player.army.archer) + ' 🏹\n' + \
                              'Маги:' + str(attack_lost_wizard) + '/' + str(player.army.wizard) + ' 🔮\n' + \
                              '<Потери врага>' + \
                              'Воины: ' + str(defender_lost_warrior) + '/' + str(defender.army.warrior) + ' 🗡\n' + \
                              'Лучники: ' + str(defender_lost_archer) + '/' + str(defender.army.archer) + ' 🏹\n' + \
                              'Маги:' + str(defender_lost_wizard) + '/' + str(defender.army.wizard) + ' 🔮\n' + \
                              '<Награда>\n' + \
                              'Дерево: ' + str(reward_wood) + ' 🌲\n' +\
                              'Камень: ' + str(reward_stone) + ' ◾\n' +\
                              'Железо: ' + str(reward_iron) + ' ◽\n' +\
                              'Золото: ' + str(reward_gold) + ' ✨\n' +\
                              'Алмазы: ' + str(reward_diamond) + ' 💎\n' +\
                              'Черепа: ' + str(reward_skull) + ' 💀\n' +\
                              'Опыт: ' + str(reward_exp) + ' 📚'

                    message_def = 'На вас напал ' + player.nickname + ' !' + \
                                  '⚔ Вы проиграли ⚔\n' + \
                                  '<Потери врага>' + \
                                  'Воины: ' + str(attack_lost_warrior) + '/' + str(player.army.warrior) + ' 🗡\n' + \
                                  'Лучники: ' + str(attack_lost_archer) + '/' + str(player.army.archer) + ' 🏹\n' + \
                                  'Маги:' + str(attack_lost_wizard) + '/' + str(player.army.wizard) + ' 🔮\n' + \
                                  '<Ваши потери>\n' + \
                                  'Воины: ' + str(defender_lost_warrior) + '/' + str(defender.army.warrior) + ' 🗡\n' + \
                                  'Лучники: ' + str(defender_lost_archer) + '/' + str(defender.army.archer) + ' 🏹\n' + \
                                  'Маги:' + str(defender_lost_wizard) + '/' + str(defender.army.wizard) + ' 🔮\n' + \
                                  '<Ресурсов украдено>\n' + \
                                  'Дерево: ' + str(reward_wood) + ' 🌲\n' + \
                                  'Камень: ' + str(reward_stone) + ' ◾\n' + \
                                  'Железо: ' + str(reward_iron) + ' ◽\n' + \
                                  'Золото: ' + str(reward_gold) + ' ✨\n' + \
                                  'Алмазы: ' + str(reward_diamond) + ' 💎\n' + \
                                  'Черепа: ' + str(reward_skull) + ' 💀\n' + \
                                  'Опыт: ' + str(reward_exp) + ' 📚'

                else:

                    # Поражение нападавшего

                    message = 'Вы напали на ' + defender.nickname + ' !' + \
                              '⚔ Поражение ⚔\n' + \
                              '<Ваши потери>\n' + \
                              'Воины: ' + str(attack_lost_warrior) + '/' + str(player.army.warrior) + ' 🗡\n' + \
                              'Лучники: ' + str(attack_lost_archer) + '/' + str(player.army.archer) + ' 🏹\n' + \
                              'Маги:' + str(attack_lost_wizard) + '/' + str(player.army.wizard) + ' 🔮\n' + \
                              '<Потери врага>' + \
                              'Воины: ' + str(defender_lost_warrior) + '/' + str(defender.army.warrior) + ' 🗡\n' + \
                              'Лучники: ' + str(defender_lost_archer) + '/' + str(defender.army.archer) + ' 🏹\n' + \
                              'Маги:' + str(defender_lost_wizard) + '/' + str(defender.army.wizard) + ' 🔮'

                    message_def = 'На вас напал ' + player.nickname + ' !' + \
                                  '⚔ Вы победили ⚔\n' + \
                                  '<Потери врага>' + \
                                  'Воины: ' + str(attack_lost_warrior) + '/' + str(player.army.warrior) + ' 🗡\n' + \
                                  'Лучники: ' + str(attack_lost_archer) + '/' + str(player.army.archer) + ' 🏹\n' + \
                                  'Маги:' + str(attack_lost_wizard) + '/' + str(player.army.wizard) + ' 🔮\n' + \
                                  '<Ваши потери>\n' + \
                                  'Воины: ' + str(defender_lost_warrior) + '/' + str(defender.army.warrior) + ' 🗡\n' + \
                                  'Лучники: ' + str(defender_lost_archer) + '/' + str(defender.army.archer) + ' 🏹\n' + \
                                  'Маги:' + str(defender_lost_wizard) + '/' + str(defender.army.wizard) + ' 🔮'

                # Сохранение

                player.army.warrior = attack_after_warrior // 1
                player.army.archer = attack_after_archer // 1
                player.army.wizard = attack_after_wizard // 1
                player.war.war_last_time = action_time
                player.war.shield = 0
                player.stock.save()
                player.army.save()
                player.war.save()
                player.save()

                defender.army.warrior = defender_after_warrior // 1
                defender.army.archer = defender_after_archer // 1
                defender.army.wizard = defender_after_wizard // 1
                defender.war.shield = 8
                defender.war.war_last_time = action_time
                defender.stock.save()
                defender.army.save()
                defender.war.save()

                vk.messages.send(
                    access_token=token,
                    user_id=str(defender.user_id),
                    keyboard=get_keyboard(player=defender),
                    message=message_def,
                    random_id=get_random_id()
                )

        else:
            message = 'Найдите противника для нападения!'
    else:
        minutes = (WAR_TIME - war_time) // 60
        sec = (WAR_TIME - war_time) - (minutes * 60)
        message = 'До нападения: ' + str(minutes) + ' м. ' + str(sec) + ' сек.'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
