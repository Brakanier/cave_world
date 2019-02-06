from .function import *
from .CONSTANT import *


def profile(vk, player, action_time, token):
    if not player.place == 'profile':
        player.place = 'profile'

    player = energy(player=player, action_time=action_time)
    player.save()
    message = 'Ник: ' + player.nickname + "\n" + \
              'Имя: ' + player.first_name + "\n" + \
              'Фамилия: ' + player.last_name + "\n" + \
              'Уровень: ' + str(player.lvl) + " 👑\n" + \
              'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + "  📚\n" + \
              'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡'

    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def stock(vk, player, token):
    message = 'Склад - ' + str(player.stock.lvl) + ' ур.' + '\n' + \
              'Дерево: ' + str(player.stock.wood) + '/' + str(player.stock.wood_max) + ' 🌲\n' + \
              'Камень: ' + str(player.stock.stone) + '/' + str(player.stock.stone_max) + ' ◾\n' + \
              'Железо: ' + str(player.stock.iron) + '/' + str(player.stock.iron_max) + ' ◽\n' + \
              'Золото: ' + str(player.stock.gold) + '/' + str(player.stock.gold_max) + ' ✨\n' + \
              'Алмазы: ' + str(player.stock.diamond) + '/' + str(player.stock.diamond_max) + ' 💎\n' + \
              'Черепа: ' + str(player.stock.skull) + ' 💀'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def cave_build(vk, player, token):
    if not player.place == 'cave_build':
        player.place = 'cave_build'
        player.save()
    message_stock = 'Склад: ' + str(player.stock.lvl * player.stock.need) + ' ◾' + '\n'
    message_forge = 'Кузница: ' + str(player.forge.need) + ' ◾\n'
    message_tavern = 'Таверна: ' + str(player.tavern.need_stone) + ' ◾ + ' + str(player.tavern.need_iron) + ' ◽\n'
    message_gate = 'Врата: 300 ◾ + 200 ◽ + 100 💎'
    message = 'Стоимость:' + '\n'
    message = message + message_stock
    if not player.build.forge:
        message = message + message_forge
    if not player.build.tavern:
        message = message + message_tavern
    if not player.build.gate:
        message = message + message_gate
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def land_build(vk, player, token):
    if not player.place == 'land_build':
        player.place = 'land_build'
        player.save()
    # башня
    message_tower = 'Башня: ' + \
                    str(player.build.tower_lvl * player.build.tower_need_stone) + \
                    ' ◾ + ' + \
                    str(player.build.tower_lvl * player.build.tower_need_wood) + \
                    ' 🌲\n'
    if player.build.tower_lvl == 0:
        message_tower = 'Башня: ' + \
                        str(player.build.tower_need_stone) + \
                        ' ◾ + ' + \
                        str(player.build.tower_need_wood) + \
                        ' 🌲\n'
    # стена
    message_wall = 'Стена: ' + str(player.build.wall_lvl * player.build.wall_need_stone) + ' ◾\n'
    if player.build.wall_lvl == 0:
        message_wall = 'Стена: ' + str(player.build.wall_need_stone) + ' ◾'
    message = 'Стоимость:' + '\n'
    message = message + message_tower + message_wall
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def forge_pickaxe(vk, player, token):
    if not player.place == 'forge_pickaxe':
        player.place = 'forge_pickaxe'
        player.save()
    forge_pickaxe_info(vk=vk, player=player, token=token)


def forge_pickaxe_info(vk, player, token):
    message = 'Стоимость крафта: \n'
    message_pickaxe_stone = 'Каменная кирка: 50 ◾ + 1 ⚡\n'
    message_pickaxe_iron = 'Железная кирка: 50 ◽ + 5 ⚡\n'
    message_pickaxe_diamond = 'Алмазная кирка: 50 💎 + 10 ⚡\n'
    message_pickaxe_skull = 'Костяная кирка: 50 💀 + 20 ⚡\n'
    if not player.forge.pickaxe_stone:
        message = message + message_pickaxe_stone
    else:
        message = message + 'Каменная кирка: есть \n'
    if not player.forge.pickaxe_iron:
        message = message + message_pickaxe_iron
    else:
        message = message + 'Железная кирка: есть \n'
    if not player.forge.pickaxe_diamond:
        message = message + message_pickaxe_diamond
    else:
        message = message + 'Алмазная кирка: есть \n'
    if not player.forge.pickaxe_skull:
        message = message + message_pickaxe_skull
    else:
        message = message + 'Костяная кирка: есть \n'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def forge_kit(vk, player, token):
    if not player.place == 'forge_kit':
        player.place = 'forge_kit'
        player.save()
    message = 'Стоимость крафта: \n'
    message_sword = 'Меч 🗡: 5 ◽ + 1 ⚡\n'
    message_bow = 'Лук 🏹: 5 ◽ + 5 🌲 + 2 ⚡\n'
    message_orb = 'Сфера 🔮: 5 ◽ + 5 🌲 + 5 💎 + 3 ⚡\n'
    message = message + message_sword + message_bow + message_orb
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def forge_kit_info(vk, player, token):
    message = 'Арсенал:\n' + \
              'Мечи: ' + str(player.forge.sword) + ' 🗡\n' + \
              'Луки: ' + str(player.forge.bow) + ' 🏹\n' + \
              'Сферы: ' + str(player.forge.orb) + ' 🔮\n'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def army(vk, player, token):
    message = 'Армия:\n' + \
              'Воины: ' + str(player.army.warrior) + ' 🗡\n' + \
              'Лучники: ' + str(player.army.archer) + ' 🏹\n' + \
              'Маги: ' + str(player.army.wizard) + ' 🔮\n' + \
              'Всего: ' + str(player.army.warrior + player.army.archer + player.army.wizard) + ' ⚔'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
