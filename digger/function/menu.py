from .function import *


def profile(vk, player, action_time, token):
    if not player.place == 'profile':
        player.place = 'profile'

    player = energy(player=player, action_time=action_time)
    player.save()
    message = 'Ник: ' + player.nickname + "\n" + \
              'Имя: ' + player.first_name + "\n" + \
              'Фамилия: ' + player.last_name + "\n" + \
              'Уровень: ' + str(player.lvl) + "\n" + \
              'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + "\n" + \
              'Энергия: ' + str(player.energy) + '/' + str(player.max_energy)

    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def stock(vk, player, token):

    message = 'Склад - ' + str(player.stock.lvl) + ' ур.' + '\n' + \
              'Камень: ' + str(player.stock.stone) + '/' + str(player.stock.stone_max) + ' 🎞\n' + \
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
    message_stock = 'Склад: ' + str(player.stock.lvl * player.stock.need) + ' камня' + '\n'
    message_forge = 'Кузница: ' + '\n'
    message_tavern = 'Таверна: ' + '\n'
    message_lift = 'Лифт: ' + '\n'
    message = 'Стоимость:' + '\n'
    message = message + message_stock
    if not player.build.forge:
        message = message + message_forge
    if not player.build.tavern:
        message = message + message_tavern
    if not player.build.lift:
        message = message + message_lift
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
    message = 'Стоимость крафта: \n'
    message_pickaxe_stone = 'Каменная кирка: 50 камня \n'
    message_pickaxe_iron = 'Железная кирка: 50 железа \n'
    message_pickaxe_diamond = 'Алмазная кирка: 50 алмазов \n'
    message_pickaxe_skull = 'Костяная кирка: 50 черепов \n'
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
    message_kit_warrior = 'Набор воина: 5 железа \n'
    message_kit_archer = 'Набор лучника: 5 железа, 5 дерева \n'
    message_kit_wizard = 'Набор мага: 5 железа, 5 дерева. 5 алмазов \n'
    message = message + message_kit_warrior + message_kit_archer + message_kit_wizard
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
