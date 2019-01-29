from .function import *
import random


def dig_stone(vk, player, action_time, token):
    need_energy = 1
    player = energy(player=player, action_time=action_time)
    if player.energy >= need_energy:
        max_chance = 109
        if player.forge.pickaxe_diamond:
            max_chance = 209
        chance = random.randint(10, max_chance)
        stone = chance//10
        space = player.stock.stone_max - player.stock.stone
        if not space == 0:
            player.energy = player.energy - need_energy
            stone = min(stone, space)
            player.stock.stone = player.stock.stone + stone
            player = exp(vk=vk, player=player, token=token, exp=need_energy)
            message = 'Добыто  камня: ' + str(stone) + ' ◾\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 🌟'
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
        if player.forge.pickaxe_diamond:
            max_chance = 129
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
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 🌟'
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
        if player.forge.pickaxe_diamond:
            max_chance = 129
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
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 🌟'
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
        if player.forge.pickaxe_diamond:
            max_chance = 69
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
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 🌟'
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
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 🌟'
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
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 🌟'
            else:
                message = 'Недостаточно железа'
        else:
            message = 'Недостаточно энергии'
        player.save()
    else:
        message = 'У вас уже есть железная кирка'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def craft_pickaxe_diamond(vk, player, action_time, token):
    need_energy = 10
    need_diamond = 50
    if not player.forge.pickaxe_diamond:
        player = energy(player=player, action_time=action_time)
        if player.energy >= need_energy:
            if player.stock.diamond >= need_diamond:
                player.energy = player.energy - need_energy
                player.stock.diamond = player.stock.diamond - need_diamond
                player.forge.pickaxe_diamond = True
                player = exp(vk=vk, player=player, token=token, exp=need_energy)
                player.stock.save()
                player.forge.save()
                message = 'Поздравляю!\n' \
                          'Вы скрафтили Алмазную кирку.\n' \
                          'Количество добываемых ресурсов увеличено.\n' + \
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 🌟'
            else:
                message = 'Недостаточно алмазов'
        else:
            message = 'Недостаточно энергии'
        player.save()
    else:
        message = 'У вас уже есть алмазная кирка'
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def craft_sword(vk, player, action_time, token):
    need_energy = 1
    need_iron = 5
    player = energy(player=player, action_time=action_time)
    if player.energy >= need_energy:
        if player.stock.iron >= need_iron:
            player.energy = player.energy - need_energy
            player.stock.iron = player.stock.iron - need_iron
            player = exp(vk=vk, player=player, token=token, exp=need_energy)
            player.forge.sword = player.forge.sword + 1
            player.stock.save()
            player.forge.save()
            message = 'Вы скрафтили Меч 🗡\n' \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 🌟'
        else:
            message = 'Недостаточно железа'
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


def craft_bow(vk, player, action_time, token):
    need_energy = 2
    need_iron = 5
    need_wood = 5
    player = energy(player=player, action_time=action_time)
    if player.energy >= need_energy:
        if player.stock.iron >= need_iron and player.stock.wood >= need_wood:
            player.energy = player.energy - need_energy
            player.stock.iron = player.stock.iron - need_iron
            player.stock.wood = player.stock.wood - need_wood
            player = exp(vk=vk, player=player, token=token, exp=need_energy)
            player.forge.bow = player.forge.bow + 1
            player.stock.save()
            player.forge.save()
            message = 'Вы скрафтили Лук 🏹\n' \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 🌟'
        else:
            message = 'Недостаточно ресурсов!\n' + \
                      'Нужно:\n' + \
                      'Железо: ' + str(need_iron) + ' ◽\n' + \
                      'Дерево: ' + str(need_wood) + ' 🌲'
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


def craft_orb(vk, player, action_time, token):
    need_energy = 3
    need_iron = 5
    need_wood = 5
    need_diamond = 5
    player = energy(player=player, action_time=action_time)
    if player.energy >= need_energy:
        if player.stock.iron >= need_iron and player.stock.wood >= need_wood and player.stock.diamond >= need_diamond:
            player.energy = player.energy - need_energy
            player.stock.iron = player.stock.iron - need_iron
            player.stock.wood = player.stock.wood - need_wood
            player.stock.diamond = player.stock.diamond - need_diamond
            player = exp(vk=vk, player=player, token=token, exp=need_energy)
            player.forge.orb = player.forge.orb + 1
            player.stock.save()
            player.forge.save()
            message = 'Вы скрафтили Сферу 🔮\n' \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 🌟'
        else:
            message = 'Недостаточно ресурсов!\n' + \
                      'Нужно:\n' + \
                      'Железо: ' + str(need_iron) + ' ◽\n' + \
                      'Дерево: ' + str(need_wood) + ' 🌲\n' + \
                      'Алмазы: ' + str(need_diamond) + ' 💎'
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


def buy_warrior(vk, player, token):
    need_sword = 1
    need_gold = 20
    if player.forge.sword >= need_sword and player.stock.gold >= need_gold:
        player.stock.gold = player.stock.gold - need_gold
        player.forge.sword = player.forge.sword - need_sword
        player.army.warrior = player.army.warrior + 1
        player.stock.save()
        player.forge.save()
        player.army.save()
        message = 'Вы наняли Воина!'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Нужно:\n' + \
                  'Золото: ' + str(need_gold) + ' ✨\n' + \
                  'Мечи: ' + str(need_sword) + ' 🗡\n'
    player.save()
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def buy_archer(vk, player, token):
    need_bow = 1
    need_gold = 20
    if player.forge.bow >= need_bow and player.stock.gold >= need_gold:
        player.stock.gold = player.stock.gold - need_gold
        player.forge.bow = player.forge.bow - need_bow
        player.army.archer = player.army.archer + 1
        player.stock.save()
        player.forge.save()
        player.army.save()
        message = 'Вы наняли Лучника!'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Нужно:\n' + \
                  'Золото: ' + str(need_gold) + ' ✨\n' + \
                  'Луки: ' + str(need_bow) + ' 🏹\n'
    player.save()
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def buy_wizard(vk, player, token):
    need_orb = 1
    need_gold = 20
    if player.forge.orb >= need_orb and player.stock.gold >= need_gold:
        player.stock.gold = player.stock.gold - need_gold
        player.forge.orb = player.forge.orb - need_orb
        player.army.wizard = player.army.wizard + 1
        player.stock.save()
        player.forge.save()
        player.army.save()
        message = 'Вы наняли Мага!'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Нужно:\n' + \
                  'Золото: ' + str(need_gold) + ' ✨\n' + \
                  'Сферы: ' + str(need_orb) + ' 🔮\n'
    player.save()
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
