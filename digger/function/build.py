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
    stone_need = player.stock.lvl * STOCK_X
    if player.stock.stone >= stone_need:
        player.stock.stone = player.stock.stone - stone_need
        player.stock.lvl = player.stock.lvl + 1
        player.stock.max = player.stock.lvl * STOCK_MAX_X
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


def build_citadel(vk, player, token):
    if not player.build.citadel:
        if player.stock.stone >= CITADEL_STONE and player.stock.iron >= CITADEL_IRON:
            player.stock.stone = player.stock.stone - CITADEL_STONE
            player.stock.iron = player.stock.iron - CITADEL_IRON
            player.build.citadel = True
            player.build.save()
            player.stock.save()
            message = 'Цитадель построена!\n' + \
                      'Осторожно!\n' + \
                      'Теперь на вас могут напасть!'
        else:
            message = 'Недостаточно ресурсов! \n' + \
                      'Нужно:\n' + \
                      'Камня: ' + str(CITADEL_STONE) + ' ◾\n' + \
                      'Железо: ' + str(CITADEL_IRON) + ' ◽\n'
    else:
        message = 'У вас уже есть Цитадель'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def build_tower(vk, player, token):
    need_stone = player.build.tower_lvl * TOWER_STONE
    need_wood = player.build.tower_lvl * TOWER_WOOD
    if player.stock.stone >= need_stone and player.stock.wood >= need_wood:
        player.stock.stone = player.stock.stone - need_stone
        player.stock.wood = player.stock.wood - need_wood
        player.build.tower_lvl = player.build.tower_lvl + 1
        player.stock.save()
        player.build.save()
        message = 'Башня улучшена! (' + str(player.build.tower_lvl) + ' ур.)'
    else:
        message = 'Недостаточно ресурсов! \n' + \
                  'Нужно:\n' + \
                  'Камня: ' + str(need_stone) + ' ◾\n' + \
                  'Дерева: ' + str(need_wood) + ' 🌲'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def build_wall(vk, player, token):
    need_stone = player.build.wall_lvl * WALL_STONE
    need_iron = player.build.wall_lvl * WALL_IRON
    if player.stock.stone >= need_stone and player.stock.wood >= need_iron:
        player.stock.stone = player.stock.stone - need_stone
        player.stock.iron = player.stock.iron - need_iron
        player.build.wall_lvl = player.build.wall_lvl + 1
        player.stock.save()
        player.build.save()
        message = 'Стена улучшена! (' + str(player.build.wall_lvl) + ' ур.)'
    else:
        message = 'Недостаточно ресурсов! \n' + \
                  'Нужно:\n' + \
                  'Камня: ' + str(need_stone) + ' ◾\n' + \
                  'Дерева: ' + str(need_iron) + ' ◽'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
