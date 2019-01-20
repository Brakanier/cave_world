from .function import *


def build_forge(vk, player, token):
    if not player.build.forge:
        player.build.forge = True
        player.build.save()
        message = 'Кузница построена'
    else:
        message = 'У вас уже есть Кузница'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def build_tavern(vk, player, token):
    if not player.build.tavern:
        player.build.tavern = True
        player.build.save()
        message = 'Таверна построена'
    else:
        message = 'У вас уже есть Таверна'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def build_stock(vk, player, token):
    stone_need = player.stock.need * player.stock.lvl
    if not player.stock.stone < stone_need:
        player.stock.stone = player.stock.stone - stone_need
        player.stock.lvl = player.stock.lvl + 1
        player.stock.stone_max = 100 * player.stock.lvl
        player.stock.ore_iron_max = 100 * player.stock.lvl
        player.stock.ore_gold_max = 100 * player.stock.lvl
        player.stock.ingot_iron_max = 100 * player.stock.lvl
        player.stock.ingot_gold_max = 100 * player.stock.lvl
        player.stock.diamond_max = 100 * player.stock.lvl
        player.stock.save()
        message = 'Склад улучшен! (' + str(player.stock.lvl) + ' ур.)'
    else:
        message = 'Вам не хватает ресурсов!'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
