from .function import *


def profile(vk, player, token):
    message = 'Имя: ' + player.first_name + "\n" + \
              'Фамилия: ' + player.last_name + "\n" + \
              'ID: ' + str(player.user_id) + "\n" + \
              'Местоположение: ' + player.place
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def stock(vk, player, token):

    message = 'Склад - ' + str(player.stock.lvl) + ' ур.' + '\n' + \
              'Камень: ' + str(player.stock.stone) + '/' + str(player.stock.stone_max) + '\n' + \
              'Железная руда: ' + str(player.stock.ore_iron) + '/' + str(player.stock.ore_iron_max) + '\n' + \
              'Золотая руда: ' + str(player.stock.ore_gold) + '/' + str(player.stock.ore_gold_max) + '\n' + \
              'Слитки железа: ' + str(player.stock.ingot_iron) + '/' + str(player.stock.ingot_iron_max) + '\n' + \
              'Слитки золота: ' + str(player.stock.ingot_gold) + '/' + str(player.stock.ingot_gold_max) + '\n' + \
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
    message_furnace = 'Плавильня: ' + '\n'
    message_forge = 'Кузница: ' + '\n'
    message_tavern = 'Таверна: ' + '\n'
    message_lift = 'Лифт: ' + '\n'
    message = 'Стоимость:' + '\n'
    message = message + message_stock
    message = message + message_furnace
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
