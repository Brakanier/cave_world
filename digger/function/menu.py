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
              'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
              'Успешных нападений: ' + str(player.win) + ' ⚔\n' + \
              'Успешных оборон: ' + str(player.defend) + ' 🛡\n'

    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player, action_time=action_time),
        message=message,
        random_id=get_random_id()
    )


def stock(vk, player, token):
    message = 'Склад - ' + str(player.stock.lvl) + ' ур.' + '\n' + \
              'Дерево: ' + str(player.stock.wood) + '/' + str(player.stock.max) + ' 🌲\n' + \
              'Камень: ' + str(player.stock.stone) + '/' + str(player.stock.max) + ' ◾\n' + \
              'Железо: ' + str(player.stock.iron) + '/' + str(player.stock.max) + ' ◽\n' + \
              'Золото: ' + str(player.stock.gold) + '/' + str(player.stock.max) + ' ✨\n' + \
              'Алмазы: ' + str(player.stock.diamond) + '/' + str(player.stock.max) + ' 💎\n' + \
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
    message_stock = 'Склад: ' + str(player.stock.lvl * STOCK_X) + ' ◾' + '\n'
    message_forge = 'Кузница: ' + str(FORGE_STONE) + ' ◾\n'
    message_tavern = 'Таверна: ' + str(TAVERN_STONE) + ' ◾ + ' + str(TAVERN_IRON) + ' ◽\n'
    message_citadel = 'Цитадель: ' + \
                      str(CITADEL_STONE) + ' ◾ + ' + \
                      str(CITADEL_IRON) + ' ◽\n'
    message = 'Стоимость:' + '\n'
    message = message + message_stock
    if not player.build.forge:
        message = message + message_forge
    if not player.build.tavern:
        message = message + message_tavern
    if not player.build.citadel:
        message = message + message_citadel
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
                    str(player.build.tower_lvl * TOWER_STONE) + ' ◾ + ' + \
                    str(player.build.tower_lvl * TOWER_WOOD) + ' 🌲\n'
    # стена
    message_wall = 'Стена: ' + \
                   str(player.build.tower_lvl * WALL_STONE) + ' ◾ + ' + \
                   str(player.build.tower_lvl * WALL_IRON) + ' ◽\n'
    message = 'Стоимость:\n'
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
    message_pickaxe_stone = 'Каменная кирка: ' + str(STONE_PICKAXE) + ' ◾ + ' + str(CRAFT_ENEGRY) + ' ⚡\n'
    message_pickaxe_iron = 'Железная кирка: ' + str(IRON_PICKAXE) + ' ◽ + ' + str(CRAFT_ENEGRY) + ' ⚡\n'
    message_pickaxe_diamond = 'Алмазная кирка: ' + str(DIAMOND_PICKAXE) + ' 💎 + ' + str(CRAFT_ENEGRY) + ' ⚡\n'
    message_pickaxe_skull = 'Костяная кирка: ' + str(SKULL_PICKAXE) + ' 💀 + ' + str(CRAFT_ENEGRY) + ' ⚡\n'
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
    message_sword = 'Меч 🗡: ' + \
                    str(SWORD_IRON) + ' ◽\n'
    message_bow = 'Лук 🏹: ' + \
                  str(BOW_IRON) + ' ◽ + ' + \
                  str(BOW_WOOD) + ' 🌲\n'
    message_orb = 'Сфера 🔮: ' + \
                  str(ORB_IRON) + ' ◽ + ' + \
                  str(ORB_WOOD) + ' 🌲 + ' + \
                  str(ORB_DIAMOND) + ' 💎\n'
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


def army(vk, player, token, action_time):
    message = 'Армия:\n' + \
              'Воины: ' + str(player.army.warrior) + ' 🗡\n' + \
              'Лучники: ' + str(player.army.archer) + ' 🏹\n' + \
              'Маги: ' + str(player.army.wizard) + ' 🔮\n' + \
              'Всего: ' + str(player.army.warrior + player.army.archer + player.army.wizard) + ' ⚔\n' + \
              'Башня: ' + str(player.build.tower_lvl) + ' ур.\n' + \
              'Стена: ' + str(player.build.wall_lvl) + ' ур.\n'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player, action_time=action_time),
        message=message,
        random_id=get_random_id()
    )


def shield_info(vk, player, action_time, token):
    shield = player.war.shield * SHIELD_X
    time = action_time - player.war.defend_last_time
    if time < shield:
        hour = (shield - time) // 3600
        minutes = ((shield - time) - (hour * 3600)) // 60
        sec = (shield - time) - (minutes * 60) - (hour * 3600)
        message = 'Щит действует еще: ' + str(hour) + ' ч. ' + str(minutes) + ' м. ' + str(sec) + ' сек. ⏳'
    else:
        message = 'У вас нет щита!'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
