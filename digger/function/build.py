from .function import *


def build_forge(vk, player, token):
    if not player.build.forge:
        if player.stock.stone >= FORGE_STONE:
            player.stock.stone = player.stock.stone - FORGE_STONE
            player.build.forge = True
            player.build.save()
            player.stock.save()
            message = 'Кузница построена'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                      'Нужно:\n' + \
                      'Камня: ' + str(FORGE_STONE) + ' ◾'
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
        if player.stock.stone >= TAVERN_STONE and player.stock.iron >= TAVERN_IRON:
            player.stock.stone = player.stock.stone - TAVERN_STONE
            player.stock.iron = player.stock.iron - TAVERN_IRON
            player.build.tavern = True
            player.build.save()
            player.stock.save()
            message = 'Таверна построена'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                      'Нужно:\n' + \
                      'Камня: ' + str(TAVERN_STONE) + ' ◾\n' + \
                      'Железо: ' + str(TAVERN_IRON) + ' ◽'
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
    stone_need = (player.stock.lvl * STOCK_X) + player.stock.need
    if player.stock.stone >= stone_need:
        player.stock.stone = player.stock.stone - stone_need
        player.stock.lvl = player.stock.lvl + 1
        player.stock.need = (player.stock.lvl * STOCK_X) + player.stock.need
        player.stock.max = (player.stock.lvl * STOCK_MAX_X) + player.stock.max
        player.stock.save()
        message = 'Склад улучшен! (' + str(player.stock.lvl) + ' ур.)'
    else:
        message = 'Недостаточно ресурсов! \n' + \
                  'Нужно:\n' + \
                  'Камня: ' + str(stone_need) + ' ◾\n'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def build_gate(vk, player, token):
    if not player.build.gate:
        if player.stock.stone >= GATE_STONE and player.stock.iron >= GATE_IRON and player.stock.diamond >= GATE_DIAMOND:
            player.stock.stone = player.stock.stone - GATE_STONE
            player.stock.iron = player.stock.iron - GATE_IRON
            player.stock.diamond = player.stock.diamond - GATE_DIAMOND
            player.build.gate = True
            player.build.save()
            player.stock.save()
            message = 'Врата построены!\n' + \
                      'Осторожно!\n' + \
                      'Теперь на вас могут напасть!'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                      'Нужно:\n' + \
                      'Камня: ' + str(GATE_STONE) + ' ◾\n' + \
                      'Железо: ' + str(GATE_IRON) + ' ◽\n' + \
                      'Алмазы: ' + str(GATE_DIAMOND) + ' 💎'
    else:
        message = 'У вас уже есть Врата'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def build_tower(vk, player, token):
    stone_need = (player.build.tower_lvl * TOWER_X) + player.build.tower_need
    wood_need = (player.build.tower_lvl * TOWER_X) + player.build.tower_need
    if player.build.tower_lvl == 0:
        stone_need = player.build.tower_need
        wood_need = player.build.tower_need
    if player.stock.stone >= stone_need and player.stock.wood >= wood_need:
        player.stock.stone = player.stock.stone - stone_need
        player.stock.wood = player.stock.wood - wood_need
        player.build.tower_lvl = player.build.tower_lvl + 1
        player.build.tower_need = (player.build.tower_lvl * TOWER_X) + player.build.tower_need
        player.stock.save()
        player.build.save()
        message = 'Башня улучшена! (' + str(player.build.tower_lvl) + ' ур.)'
    else:
        message = 'Недостаточно ресурсов! \n' + \
                  'Нужно:\n' + \
                  'Камня: ' + str(stone_need) + ' ◾\n' + \
                  'Дерева: ' + str(wood_need) + ' 🌲'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def build_wall(vk, player, token):
    stone_need = (player.build.wall_lvl * WALL_X) + player.build.wall_need
    if player.build.wall_lvl == 0:
        stone_need = player.build.wall_need
    if player.stock.stone >= stone_need:
        player.stock.stone = player.stock.stone - stone_need
        player.build.wall_lvl = player.build.wall_lvl + 1
        player.build.wall_need = (player.build.wall_lvl * WALL_X) + player.build.wall_need
        player.stock.save()
        player.build.save()
        message = 'Стена улучшена! (' + str(player.build.wall_lvl) + ' ур.)'
    else:
        message = 'Недостаточно ресурсов! \n' + \
                  'Нужно:\n' + \
                  'Камня: ' + str(stone_need) + ' ◾'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
