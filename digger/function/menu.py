from .function import *
from .CONSTANT import *


def profile(player, action_time):
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

    send(player=player, message=message, keyboard=get_keyboard(player=player, action_time=action_time))


def stock(player):
    message = 'Склад - ' + str(player.stock.lvl) + ' ур.' + '\n' + \
              'Дерево: ' + str(player.stock.wood) + '/' + str(player.stock.max) + ' 🌲\n' + \
              'Камень: ' + str(player.stock.stone) + '/' + str(player.stock.max) + ' ◾\n' + \
              'Железо: ' + str(player.stock.iron) + '/' + str(player.stock.max) + ' ◽\n' + \
              'Золото: ' + str(player.stock.gold) + '/' + str(player.stock.max) + ' ✨\n' + \
              'Алмазы: ' + str(player.stock.diamond) + '/' + str(player.stock.max) + ' 💎\n' + \
              'Черепа: ' + str(player.stock.skull) + ' 💀'
    send(player=player, message=message)


def cave_build(player):
    if not player.place == 'cave_build':
        player.place = 'cave_build'
        player.save()
    message_stock = 'Склад 🏤: ' + str(player.stock.lvl * STOCK_X) + ' ◾' + '\n'
    message_forge = 'Кузница ⚒: ' + str(FORGE_STONE) + ' ◾\n'
    message_tavern = 'Таверна 🍺: ' + str(TAVERN_STONE) + ' ◾ + ' + str(TAVERN_IRON) + ' ◽\n'
    message_citadel = 'Цитадель 🏰: ' + \
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
    send(player=player, message=message)


def land_build(player):
    if not player.place == 'land_build':
        player.place = 'land_build'
        player.save()
    # башня
    message_tower = 'Башня: ' + \
                    str(player.build.tower_lvl * TOWER_STONE) + ' ◾ + ' + \
                    str(player.build.tower_lvl * TOWER_WOOD) + ' 🌲\n'
    # стена
    message_wall = 'Стена: ' + \
                   str(player.build.wall_lvl * WALL_STONE) + ' ◾ + ' + \
                   str(player.build.wall_lvl * WALL_IRON) + ' ◽\n'
    message = 'Стоимость:\n'
    message = message + message_tower + message_wall
    send(player=player, message=message)


def forge_pickaxe(player):
    if not player.place == 'forge_pickaxe':
        player.place = 'forge_pickaxe'
        player.save()
    forge_pickaxe_info(player=player)


def forge_pickaxe_info(player):
    message = 'Стоимость крафта: \n'
    message_pickaxe_stone = '◾ Каменная кирка ◾: ' + str(STONE_PICKAXE) + ' ◾ + ' + str(CRAFT_ENEGRY) + ' ⚡\n'
    message_pickaxe_iron = '◽ Железная кирка ◽: ' + str(IRON_PICKAXE) + ' ◽ + ' + str(CRAFT_ENEGRY) + ' ⚡\n'
    message_pickaxe_diamond = '💎 Алмазная кирка 💎: ' + str(DIAMOND_PICKAXE) + ' 💎 + ' + str(CRAFT_ENEGRY) + ' ⚡\n'
    message_pickaxe_skull = '💀 Костяная кирка 💀: ' + str(SKULL_PICKAXE) + ' 💀 + ' + str(CRAFT_ENEGRY * 10) + ' ⚡\n'
    if not player.forge.pickaxe_stone:
        message = message + message_pickaxe_stone
    else:
        message = message + '◾ Каменная кирка ◾: ✔ \n'
    if not player.forge.pickaxe_iron:
        message = message + message_pickaxe_iron
    else:
        message = message + '◽ Железная кирка ◽: ✔ \n'
    if not player.forge.pickaxe_diamond:
        message = message + message_pickaxe_diamond
    else:
        message = message + '💎 Алмазная кирка 💎: ✔ \n'
    if not player.forge.pickaxe_skull:
        message = message + message_pickaxe_skull
    else:
        message = message + '💀 Костяная кирка 💀: ✔ \n'
    send(player=player, message=message)


def forge_kit(player):
    if not player.place == 'forge_kit':
        player.place = 'forge_kit'
        player.save()
    message = 'Стоимость крафта: \n'
    message_sword = '🗡 Меч: ' + \
                    str(SWORD_IRON) + ' ◽\n'
    message_bow = '🏹 Лук: ' + \
                  str(BOW_IRON) + ' ◽ + ' + \
                  str(BOW_WOOD) + ' 🌲\n'
    message_orb = '🔮 Сфера: ' + \
                  str(ORB_IRON) + ' ◽ + ' + \
                  str(ORB_WOOD) + ' 🌲 + ' + \
                  str(ORB_DIAMOND) + ' 💎\n'
    message = message + message_sword + message_bow + message_orb
    send(player=player, message=message)


def forge_kit_info(player):
    message = 'Арсенал:\n' + \
              'Мечи: ' + str(player.forge.sword) + ' 🗡\n' + \
              'Луки: ' + str(player.forge.bow) + ' 🏹\n' + \
              'Сферы: ' + str(player.forge.orb) + ' 🔮\n'
    send(player=player, message=message)


def army(player):
    message = 'Армия:\n' + \
              'Воины: ' + str(player.army.warrior) + ' 🗡👥\n' + \
              'Лучники: ' + str(player.army.archer) + ' 🏹👥\n' + \
              'Маги: ' + str(player.army.wizard) + ' 🔮👥\n' + \
              'Всего: ' + str(player.army.warrior + player.army.archer + player.army.wizard) + ' ⚔👥\n'
    if player.build.citadel:
        tower_and_wall = 'Башня: ' + str(player.build.tower_lvl) + ' ур.\n' + \
                         'Стена: ' + str(player.build.wall_lvl) + ' ур.'
        message = message + tower_and_wall
    send(player=player, message=message)


def shield_info(player, action_time):
    shield = player.war.shield * SHIELD_X
    time = action_time - player.war.defend_last_time
    if time < shield:
        hour = (shield - time) // 3600
        minutes = ((shield - time) - (hour * 3600)) // 60
        sec = (shield - time) - (minutes * 60) - (hour * 3600)
        message = 'Щит действует еще: ' + str(hour) + ' ч. ' + str(minutes) + ' м. ' + str(sec) + ' сек. ⏳'
    else:
        message = 'У вас нет щита!'
    send(player=player, message=message)
