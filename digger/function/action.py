from .function import *
import random


def dig_stone(vk, player, action_time, token):
    need_energy = 1
    player = energy(player=player, action_time=action_time)
    if player.energy >= need_energy:
        max_chance = 109
        chance = random.randint(10, max_chance)
        stone = chance//10
        space = player.stock.stone_max - player.stock.stone
        if not space == 0:
            player.energy = player.energy - need_energy
            stone = min(stone, space)
            player.stock.stone = player.stock.stone + stone
            player = exp(vk=vk, player=player, token=token, exp=need_energy)
            message = 'Добыто  камня: ' + str(stone) + ' 🎞\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need)
            player.stock.save()
        else:
            message = 'Склад заполнен'
    else:
        message = 'Недостаточно энергии'
    player.save()
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def dig_iron(vk, player, action_time, token):
    need_energy = 2
    player = energy(player=player, action_time=action_time)
    if player.energy >= need_energy:
        max_chance = 69
        chance = random.randint(10, max_chance)
        iron = chance//10
        space_iron = player.stock.iron_max - player.stock.iron
        if not space_iron == 0:
            player.energy = player.energy - need_energy
            iron = min(iron, space_iron)
            player.stock.iron = player.stock.iron + iron
            player = exp(vk=vk, player=player, token=token, exp=need_energy)
            message = 'Добыто железной руды: ' + str(iron) + ' ◽\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need)
            player.stock.save()
        else:
            message = 'Склад заполнен'
    else:
        message = 'Недостаточно энергии'
    player.save()
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def dig_gold(vk, player, action_time, token):
    need_energy = 2
    player = energy(player=player, action_time=action_time)
    if player.energy >= need_energy:
        max_chance = 69
        chance = random.randint(10, max_chance)
        gold = chance//10
        space_gold = player.stock.gold_max - player.stock.gold
        if not space_gold == 0:
            player.energy = player.energy - need_energy
            gold = min(gold, space_gold)
            player.stock.gold = player.stock.gold + gold
            player = exp(vk=vk, player=player, token=token, exp=need_energy)
            message = 'Добыто золотой руды: ' + str(gold) + ' ✨\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need)
            player.stock.save()
        else:
            message = 'Склад заполнен'
    else:
        message = 'Недостаточно энергии'
    player.save()
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def dig_diamond(vk, player, action_time, token):
    need_energy = 3
    player = energy(player=player, action_time=action_time)
    if player.energy >= need_energy:
        max_chance = 39
        chance = random.randint(10, max_chance)
        diamond = chance//10
        space_diamond = player.stock.diamond_max - player.stock.diamond
        if not space_diamond == 0:
            player.energy = player.energy - need_energy
            diamond = min(diamond, space_diamond)
            player.stock.diamond = player.stock.diamond + diamond
            player = exp(vk=vk, player=player, token=token, exp=need_energy)
            message = 'Добыто алмазов: ' + str(diamond) + ' 💎\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need)
            player.stock.save()
        else:
            message = 'Склад заполнен'
    else:
        message = 'Недостаточно энергии'
    player.save()
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def craft_pickaxe_stone(vk, player, action_time, token):
    need_energy = 1
    need_stone = 50
    if not player.forge.pickaxe_stone:
        player = energy(player=player, action_time=action_time)
        if player.energy >= need_energy:
            if player.stock.stone >= need_stone:
                player.energy = player.energy - need_energy
                player.stock.stone = player.stock.stone - need_stone
                player.forge.pickaxe_stone = True
                player = exp(vk=vk, player=player, token=token, exp=need_energy)
                player.stock.save()
                player.forge.save()
                message = 'Поздравляю!\n' \
                          'Вы скрафтили Каменную кирку.\n' \
                          'Теперь вы можете добывать железо и золото в шахте.\n' + \
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need)
            else:
                message = 'Недостаточно камня'
        else:
            message = 'Недостаточно энергии'
        player.save()
    else:
        message = 'У вас уже есть каменная кирка'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def craft_pickaxe_iron(vk, player, action_time, token):
    need_energy = 5
    need_iron = 50
    if not player.forge.pickaxe_iron:
        player = energy(player=player, action_time=action_time)
        if player.energy >= need_energy:
            if player.stock.iron >= need_iron:
                player.energy = player.energy - need_energy
                player.stock.iron = player.stock.iron - need_iron
                player.forge.pickaxe_iron = True
                player = exp(vk=vk, player=player, token=token, exp=need_energy)
                player.stock.save()
                player.forge.save()
                message = 'Поздравляю!\n' \
                          'Вы скрафтили Железную кирку.\n' \
                          'Теперь вы можете добывать алмазы в шахте.\n' + \
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need)
            else:
                message = 'Недостаточно камня'
        else:
            message = 'Недостаточно энергии'
        player.save()
    else:
        message = 'У вас уже есть каменная кирка'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
