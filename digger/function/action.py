from .function import *
from .CONSTANT import *
import random


def cut_wood(vk, player, action_time, token):
    player = energy(player=player, action_time=action_time)
    if player.energy >= DIG_ENERGY:
        wood_max = WOOD_MAX
        wood_min = WOOD_MIN
        if player.forge.pickaxe_diamond:
            wood_max = WOOD_MAX * 2
            wood_min = WOOD_MIN * 2
        wood = random.randint(wood_min, wood_max)
        space = player.stock.max - player.stock.wood
        if space > 0:
            player.energy = player.energy - DIG_ENERGY
            wood = min(wood, space)
            player.stock.wood = player.stock.wood + wood
            player = exp(vk=vk, player=player, token=token, exp=DIG_ENERGY)
            message = 'Добыто  дерева: ' + str(wood) + ' 🌲\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
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


def dig_stone(vk, player, action_time, token):
    player = energy(player=player, action_time=action_time)
    if player.energy >= DIG_ENERGY:
        stone_max = STONE_MAX
        stone_min = STONE_MIN
        if player.forge.pickaxe_diamond:
            stone_max = STONE_MAX * 2
            stone_min = STONE_MIN * 2
        stone = random.randint(stone_min, stone_max)
        space = player.stock.max - player.stock.stone
        if space > 0:
            player.energy = player.energy - DIG_ENERGY
            stone = min(stone, space)
            player.stock.stone = player.stock.stone + stone
            player = exp(vk=vk, player=player, token=token, exp=DIG_ENERGY)
            message = 'Добыто  камня: ' + str(stone) + ' ◾\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
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
    player = energy(player=player, action_time=action_time)
    if player.energy >= DIG_ENERGY:
        iron_max = IRON_MAX
        iron_min = IRON_MIN
        if player.forge.pickaxe_diamond:
            iron_max = IRON_MAX * 2
            iron_min = IRON_MIN * 2
        iron = random.randint(iron_min, iron_max)
        space = player.stock.max - player.stock.iron
        if space > 0:
            player.energy = player.energy - DIG_ENERGY
            iron = min(iron, space)
            player.stock.iron = player.stock.iron + iron
            player = exp(vk=vk, player=player, token=token, exp=DIG_ENERGY)
            message = 'Добыто железной руды: ' + str(iron) + ' ◽\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
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
    player = energy(player=player, action_time=action_time)
    if player.energy >= DIG_ENERGY:
        gold_max = GOLD_MAX
        gold_min = GOLD_MIN
        if player.forge.pickaxe_diamond:
            gold_max = GOLD_MAX * 2
            gold_min = GOLD_MIN * 2
        gold = random.randint(gold_min, gold_max)
        space = player.stock.max - player.stock.gold
        if space > 0:
            player.energy = player.energy - DIG_ENERGY
            gold = min(gold, space)
            player.stock.gold = player.stock.gold + gold
            player = exp(vk=vk, player=player, token=token, exp=DIG_ENERGY)
            message = 'Добыто золотой руды: ' + str(gold) + ' ✨\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
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
    player = energy(player=player, action_time=action_time)
    if player.energy >= DIG_ENERGY:
        diamond_max = DIAMOND_MAX
        diamond_min = DIAMOND_MIN
        if player.forge.pickaxe_diamond:
            diamond_max = DIAMOND_MAX * 2
            diamond_min = DIAMOND_MIN * 2
        diamond = random.randint(diamond_min, diamond_max)
        space = player.stock.max - player.stock.diamond
        if space > 0:
            player.energy = player.energy - DIG_ENERGY
            diamond = min(diamond, space)
            player.stock.diamond = player.stock.diamond + diamond
            player = exp(vk=vk, player=player, token=token, exp=DIG_ENERGY)
            message = 'Добыто алмазов: ' + str(diamond) + ' 💎\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
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
    if not player.forge.pickaxe_stone:
        player = energy(player=player, action_time=action_time)
        if player.energy >= CRAFT_ENEGRY:
            if player.stock.stone >= STONE_PICKAXE:
                player.energy = player.energy - CRAFT_ENEGRY
                player.stock.stone = player.stock.stone - STONE_PICKAXE
                player.forge.pickaxe_stone = True
                player = exp(vk=vk, player=player, token=token, exp=CRAFT_ENEGRY)
                player.stock.save()
                player.forge.save()
                message = 'Поздравляю!\n' \
                          'Вы скрафтили Каменную кирку.\n' \
                          'Теперь вы можете добывать железо и золото в шахте.\n' + \
                          'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
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
    if not player.forge.pickaxe_iron:
        player = energy(player=player, action_time=action_time)
        if player.energy >= CRAFT_ENEGRY:
            if player.stock.iron >= IRON_PICKAXE:
                player.energy = player.energy - CRAFT_ENEGRY
                player.stock.iron = player.stock.iron - IRON_PICKAXE
                player.forge.pickaxe_iron = True
                player = exp(vk=vk, player=player, token=token, exp=CRAFT_ENEGRY)
                player.stock.save()
                player.forge.save()
                message = 'Поздравляю!\n' \
                          'Вы скрафтили Железную кирку.\n' \
                          'Теперь вы можете добывать алмазы в шахте.\n' + \
                          'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
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
    if not player.forge.pickaxe_diamond:
        player = energy(player=player, action_time=action_time)
        if player.energy >= CRAFT_ENEGRY:
            if player.stock.diamond >= DIAMOND_PICKAXE:
                player.energy = player.energy - CRAFT_ENEGRY
                player.stock.diamond = player.stock.diamond - DIAMOND_PICKAXE
                player.forge.pickaxe_diamond = True
                player = exp(vk=vk, player=player, token=token, exp=CRAFT_ENEGRY)
                player.stock.save()
                player.forge.save()
                message = 'Поздравляю!\n' \
                          'Вы скрафтили Алмазную кирку.\n' \
                          'Количество добываемых ресурсов увеличено (x2).\n' + \
                          'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
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
    player = energy(player=player, action_time=action_time)
    if player.energy >= CRAFT_ENEGRY:
        if player.stock.iron >= SWORD_IRON:
            player.energy = player.energy - CRAFT_ENEGRY
            player.stock.iron = player.stock.iron - SWORD_IRON
            player = exp(vk=vk, player=player, token=token, exp=CRAFT_ENEGRY)
            player.forge.sword = player.forge.sword + 1
            player.stock.save()
            player.forge.save()
            message = 'Вы скрафтили Меч 🗡\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
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
    player = energy(player=player, action_time=action_time)
    if player.energy >= CRAFT_ENEGRY:
        if player.stock.iron >= BOW_IRON and player.stock.wood >= BOW_WOOD:
            player.energy = player.energy - CRAFT_ENEGRY
            player.stock.iron = player.stock.iron - BOW_IRON
            player.stock.wood = player.stock.wood - BOW_WOOD
            player = exp(vk=vk, player=player, token=token, exp=CRAFT_ENEGRY)
            player.forge.bow = player.forge.bow + 1
            player.stock.save()
            player.forge.save()
            message = 'Вы скрафтили Лук 🏹\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
        else:
            message = 'Недостаточно ресурсов!\n' + \
                      'Нужно:\n' + \
                      'Железо: ' + str(BOW_IRON) + ' ◽\n' + \
                      'Дерево: ' + str(BOW_WOOD) + ' 🌲'
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
    player = energy(player=player, action_time=action_time)
    if player.energy >= CRAFT_ENEGRY:
        if player.stock.iron >= ORB_IRON and player.stock.wood >= ORB_WOOD and player.stock.diamond >= ORB_DIAMOND:
            player.energy = player.energy - CRAFT_ENEGRY
            player.stock.iron = player.stock.iron - ORB_IRON
            player.stock.wood = player.stock.wood - ORB_WOOD
            player.stock.diamond = player.stock.diamond - ORB_DIAMOND
            player = exp(vk=vk, player=player, token=token, exp=CRAFT_ENEGRY)
            player.forge.orb = player.forge.orb + 1
            player.stock.save()
            player.forge.save()
            message = 'Вы скрафтили Сферу 🔮\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
        else:
            message = 'Недостаточно ресурсов!\n' + \
                      'Нужно:\n' + \
                      'Железо: ' + str(ORB_IRON) + ' ◽\n' + \
                      'Дерево: ' + str(ORB_WOOD) + ' 🌲\n' + \
                      'Алмазы: ' + str(ORB_DIAMOND) + ' 💎'
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
    if player.forge.sword >= WEAPON and player.stock.gold >= PRICE_GOLD:
        player.stock.gold = player.stock.gold - PRICE_GOLD
        player.forge.sword = player.forge.sword - WEAPON
        player.army.warrior = player.army.warrior + 1
        player.stock.save()
        player.forge.save()
        player.army.save()
        message = 'Вы наняли Воина!'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Нужно:\n' + \
                  'Золото: ' + str(PRICE_GOLD) + ' ✨\n' + \
                  'Мечи: ' + str(WEAPON) + ' 🗡\n'
    player.save()
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def buy_archer(vk, player, token):
    if player.forge.bow >= WEAPON and player.stock.gold >= PRICE_GOLD:
        player.stock.gold = player.stock.gold - PRICE_GOLD
        player.forge.bow = player.forge.bow - WEAPON
        player.army.archer = player.army.archer + 1
        player.stock.save()
        player.forge.save()
        player.army.save()
        message = 'Вы наняли Лучника!'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Нужно:\n' + \
                  'Золото: ' + str(PRICE_GOLD) + ' ✨\n' + \
                  'Луки: ' + str(WEAPON) + ' 🏹\n'
    player.save()
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )


def buy_wizard(vk, player, token):
    if player.forge.orb >= WEAPON and player.stock.gold >= PRICE_GOLD:
        player.stock.gold = player.stock.gold - PRICE_GOLD
        player.forge.orb = player.forge.orb - WEAPON
        player.army.wizard = player.army.wizard + 1
        player.stock.save()
        player.forge.save()
        player.army.save()
        message = 'Вы наняли Мага!'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Нужно:\n' + \
                  'Золото: ' + str(PRICE_GOLD) + ' ✨\n' + \
                  'Сферы: ' + str(WEAPON) + ' 🔮\n'
    player.save()
    vk.messages.send(
        access_token=token,
        user_id=str(player.user_id),
        keyboard=get_keyboard(player=player),
        message=message,
        random_id=get_random_id()
    )
