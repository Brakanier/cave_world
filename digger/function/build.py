from .function import *


def build_forge(vk, player, token):
    if not player.build.forge:
        if player.stock.stone >= player.forge.need:
            player.stock.stone = player.stock.stone - player.forge.need
            player.build.forge = True
            player.build.save()
            player.stock.save()
            message = 'Кузница построена'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                      'Нужно:\n' + \
                      'Камня: ' + str(player.forge.need) + ' ◾'
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
        if player.stock.stone >= player.tavern.need_stone and player.stock.iron >= player.tavern.need_iron:
            player.stock.stone = player.stock.stone - player.tavern.need_stone
            player.stock.iron = player.stock.iron - player.tavern.need_iron
            player.build.tavern = True
            player.build.save()
            player.stock.save()
            message = 'Таверна построена'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                      'Нужно:\n' + \
                      'Камня: ' + str(player.tavern.need_stone) + ' ◾\n' + \
                      'Железо: ' + str(player.tavern.need_iron) + ' ◽'
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
        player.stock.wood_max = 100 * player.stock.lvl
        player.stock.stone_max = 100 * player.stock.lvl
        player.stock.iron_max = 100 * player.stock.lvl
        player.stock.gold_max = 100 * player.stock.lvl
        player.stock.diamond_max = 100 * player.stock.lvl
        player.stock.save()
        message = 'Склад улучшен! (' + str(player.stock.lvl) + ' ур.)'
    else:
        message = 'Недостаточно ресурсов! \n' + \
                  'Нужно:\n' + \
                  'Камня: ' + str(player.stock.need) + ' ◾\n'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def build_gate(vk, player, token):
    need_stone = 300
    need_iron = 200
    need_diamond = 100
    if not player.build.gate:
        if player.stock.stone >= need_stone and player.stock.iron >= need_iron and player.stock.diamond >= need_diamond:
            player.stock.stone = player.stock.stone - need_stone
            player.stock.iron = player.stock.iron - need_iron
            player.stock.diamond = player.stock.diamond - need_diamond
            player.build.gate = True
            player.build.save()
            player.stock.save()
            message = 'Врата построены!\n' + \
                      'Осторожно!\n' + \
                      'Теперь на вас могут напасть!'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                      'Нужно:\n' + \
                      'Камня: ' + str(need_stone) + ' ◾\n' + \
                      'Железо: ' + str(need_iron) + ' ◽\n' + \
                      'Алмазы: ' + str(need_diamond) + ' 💎'
    else:
        message = 'У вас уже есть Врата'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
