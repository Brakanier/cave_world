from .function import *
from .CONSTANT import *
import random


def cut_wood(player, action_time):
    player = energy(player=player, action_time=action_time)
    if player.energy >= DIG_ENERGY:
        wood_max = WOOD_MAX
        wood_min = WOOD_MIN
        if player.forge.pickaxe_diamond:
            wood_max = WOOD_MAX * 2
            wood_min = WOOD_MIN * 2
        if player.forge.pickaxe_skull:
            wood_max = WOOD_MAX * 3
            wood_min = WOOD_MIN * 3
        wood = random.randint(wood_min, wood_max)
        space = player.stock.max - player.stock.wood
        if space > 0:
            player.energy = player.energy - DIG_ENERGY
            wood = min(wood, space)
            player.stock.wood = player.stock.wood + wood
            player = exp(player=player, exp=DIG_ENERGY)
            message = 'Добыто  дерева: ' + str(wood) + ' 🌲\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
            player.stock.save()
        else:
            message = 'Склад заполнен'
    else:
        message = 'Недостаточно энергии'
    player.save()
    send(player=player, message=message)


def dig_stone(player, action_time):
    player = energy(player=player, action_time=action_time)
    if player.energy >= DIG_ENERGY:
        stone_max = STONE_MAX
        stone_min = STONE_MIN
        if player.forge.pickaxe_diamond:
            stone_max = STONE_MAX * 2
            stone_min = STONE_MIN * 2
        if player.forge.pickaxe_skull:
            stone_max = STONE_MAX * 3
            stone_min = STONE_MIN * 3
        stone = random.randint(stone_min, stone_max)
        space = player.stock.max - player.stock.stone
        if space > 0:
            player.energy = player.energy - DIG_ENERGY
            stone = min(stone, space)
            player.stock.stone = player.stock.stone + stone
            player = exp(player=player, exp=DIG_ENERGY)
            message = 'Добыто  камня: ' + str(stone) + ' ◾\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
            player.stock.save()
        else:
            message = 'Склад заполнен'
    else:
        message = 'Недостаточно энергии'
    player.save()
    send(player=player, message=message)


def dig_iron(player, action_time):
    player = energy(player=player, action_time=action_time)
    if player.energy >= DIG_ENERGY:
        iron_max = IRON_MAX
        iron_min = IRON_MIN
        if player.forge.pickaxe_diamond:
            iron_max = IRON_MAX * 2
            iron_min = IRON_MIN * 2
        if player.forge.pickaxe_skull:
            iron_max = IRON_MAX * 3
            iron_min = IRON_MIN * 3
        iron = random.randint(iron_min, iron_max)
        space = player.stock.max - player.stock.iron
        if space > 0:
            player.energy = player.energy - DIG_ENERGY
            iron = min(iron, space)
            player.stock.iron = player.stock.iron + iron
            player = exp(player=player, exp=DIG_ENERGY)
            message = 'Добыто железной руды: ' + str(iron) + ' ◽\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
            player.stock.save()
        else:
            message = 'Склад заполнен'
    else:
        message = 'Недостаточно энергии'
    player.save()
    send(player=player, message=message)


def dig_gold(player, action_time):
    player = energy(player=player, action_time=action_time)
    if player.energy >= DIG_ENERGY:
        gold_max = GOLD_MAX
        gold_min = GOLD_MIN
        if player.forge.pickaxe_diamond:
            gold_max = GOLD_MAX * 2
            gold_min = GOLD_MIN * 2
        if player.forge.pickaxe_skull:
            gold_max = GOLD_MAX * 3
            gold_min = GOLD_MIN * 3
        gold = random.randint(gold_min, gold_max)
        space = player.stock.max - player.stock.gold
        if space > 0:
            player.energy = player.energy - DIG_ENERGY
            gold = min(gold, space)
            player.stock.gold = player.stock.gold + gold
            player = exp(player=player, exp=DIG_ENERGY)
            message = 'Добыто золотой руды: ' + str(gold) + ' ✨\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
            player.stock.save()
        else:
            message = 'Склад заполнен'
    else:
        message = 'Недостаточно энергии'
    player.save()
    send(player=player, message=message)


def dig_diamond(player, action_time):
    player = energy(player=player, action_time=action_time)
    if player.energy >= DIG_ENERGY:
        diamond_max = DIAMOND_MAX
        diamond_min = DIAMOND_MIN
        if player.forge.pickaxe_diamond:
            diamond_max = DIAMOND_MAX * 2
            diamond_min = DIAMOND_MIN * 2
        if player.forge.pickaxe_skull:
            diamond_max = DIAMOND_MAX * 3
            diamond_min = DIAMOND_MIN * 3
        diamond = random.randint(diamond_min, diamond_max)
        space = player.stock.max - player.stock.diamond
        if space > 0:
            player.energy = player.energy - DIG_ENERGY
            diamond = min(diamond, space)
            player.stock.diamond = player.stock.diamond + diamond
            player = exp(player=player, exp=DIG_ENERGY)
            message = 'Добыто алмазов: ' + str(diamond) + ' 💎\n' + \
                      'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                      'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
            player.stock.save()
        else:
            message = 'Склад заполнен'
    else:
        message = 'Недостаточно энергии'
    player.save()
    send(player=player, message=message)


def craft_pickaxe_stone(player, action_time):
    if not player.forge.pickaxe_stone:
        player = energy(player=player, action_time=action_time)
        if player.energy >= CRAFT_ENEGRY:
            if player.stock.stone >= STONE_PICKAXE:
                player.energy = player.energy - CRAFT_ENEGRY
                player.stock.stone = player.stock.stone - STONE_PICKAXE
                player.forge.pickaxe_stone = True
                player = exp(player=player, exp=CRAFT_ENEGRY)
                player.stock.save()
                player.forge.save()
                message = 'Поздравляю!\n' + \
                          'Вы скрафтили ◾ Каменную Кирку ◾\n' + \
                          'Теперь вы можете добывать железо и золото в шахте.\n' + \
                          'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
            else:
                message = 'Недостаточно камня'
        else:
            message = 'Недостаточно энергии'
        player.save()
    else:
        message = 'У вас уже есть ◾ Каменная Кирка ◾'
    send(player=player, message=message)


def craft_pickaxe_iron(player, action_time):
    if not player.forge.pickaxe_iron:
        player = energy(player=player, action_time=action_time)
        if player.energy >= CRAFT_ENEGRY:
            if player.stock.iron >= IRON_PICKAXE:
                player.energy = player.energy - CRAFT_ENEGRY
                player.stock.iron = player.stock.iron - IRON_PICKAXE
                player.forge.pickaxe_iron = True
                player = exp(player=player, exp=CRAFT_ENEGRY)
                player.stock.save()
                player.forge.save()
                message = 'Поздравляю!\n' \
                          'Вы скрафтили ◽ Железную Кирку ◽\n' \
                          'Теперь вы можете добывать алмазы в шахте.\n' + \
                          'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
            else:
                message = 'Недостаточно железа'
        else:
            message = 'Недостаточно энергии'
        player.save()
    else:
        message = 'У вас уже есть ◽ Железная Кирка ◽'
    send(player=player, message=message)


def craft_pickaxe_diamond(player, action_time):
    if not player.forge.pickaxe_diamond:
        player = energy(player=player, action_time=action_time)
        if player.energy >= CRAFT_ENEGRY:
            if player.stock.diamond >= DIAMOND_PICKAXE:
                player.energy = player.energy - CRAFT_ENEGRY
                player.stock.diamond = player.stock.diamond - DIAMOND_PICKAXE
                player.forge.pickaxe_diamond = True
                player = exp(player=player, exp=CRAFT_ENEGRY)
                player.stock.save()
                player.forge.save()
                message = 'Поздравляю!\n' \
                          'Вы скрафтили 💎 Алмазную Кирку 💎\n' \
                          'Количество добываемых ресурсов увеличено (x2).\n' + \
                          'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
            else:
                message = 'Недостаточно алмазов'
        else:
            message = 'Недостаточно энергии'
        player.save()
    else:
        message = 'У вас уже есть 💎 Алмазная Кирка 💎'
    send(player=player, message=message)


def craft_pickaxe_skull(player, action_time):
    if not player.forge.pickaxe_skull:
        player = energy(player=player, action_time=action_time)
        if player.energy >= (CRAFT_ENEGRY * 10):
            if player.stock.skull >= SKULL_PICKAXE:
                player.energy = player.energy - (CRAFT_ENEGRY * 10)
                player.stock.diamond = player.stock.skull - SKULL_PICKAXE
                player.forge.pickaxe_skull = True
                player = exp(player=player, exp=(CRAFT_ENEGRY * 10))
                player.stock.save()
                player.forge.save()
                message = 'Поздравляю!\n' \
                          'Вы скрафтили 💀 Костяную Кирку 💀\n' \
                          'Количество добываемых ресурсов увеличено (x3).\n' + \
                          'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n' + \
                          'Опыт: ' + str(player.exp) + '/' + str(player.exp_need) + ' 📚'
            else:
                message = 'Недостаточно черепов'
        else:
            message = 'Недостаточно энергии'
        player.save()
    else:
        message = 'У вас уже есть 💀 Костяная Кирка 💀'
    send(player=player, message=message)


def craft_sword(player, amount=1):
    if player.stock.iron >= (SWORD_IRON * amount):
        player.stock.iron = player.stock.iron - (SWORD_IRON * amount)
        player.forge.sword = player.forge.sword + amount
        player.stock.save()
        player.forge.save()
        message = 'Вы скрафтили ' + str(amount) + ' 🗡'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Для ' + str(amount) + ' 🗡 нужно:\n' + \
                  'Железо: ' + str(SWORD_IRON * amount) + ' ◽'
    send(player=player, message=message)


def craft_bow(player, amount=1):
    if player.stock.iron >= (BOW_IRON * amount) \
            and player.stock.wood >= (BOW_WOOD * amount):
        player.stock.iron = player.stock.iron - (BOW_IRON * amount)
        player.stock.wood = player.stock.wood - (BOW_WOOD * amount)
        player.forge.bow = player.forge.bow + amount
        player.stock.save()
        player.forge.save()
        message = 'Вы скрафтили ' + str(amount) + ' 🏹'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Для ' + str(amount) + ' 🏹 нужно:\n' + \
                  'Железо: ' + str(BOW_IRON * amount) + ' ◽\n' + \
                  'Дерево: ' + str(BOW_WOOD * amount) + ' 🌲'
    send(player=player, message=message)


def craft_orb(player, amount=1):
    if player.stock.iron >= (ORB_IRON * amount) \
            and player.stock.wood >= (ORB_WOOD * amount) \
            and player.stock.diamond >= (ORB_DIAMOND * amount):
        player.stock.iron = player.stock.iron - (ORB_IRON * amount)
        player.stock.wood = player.stock.wood - (ORB_WOOD * amount)
        player.stock.diamond = player.stock.diamond - (ORB_DIAMOND * amount)
        player.forge.orb = player.forge.orb + amount
        player.stock.save()
        player.forge.save()
        message = 'Вы скрафтили ' + str(amount) + ' 🔮\n'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Для ' + str(amount) + ' 🔮 нужно:\n' + \
                  'Железо: ' + str(ORB_IRON * amount) + ' ◽\n' + \
                  'Дерево: ' + str(ORB_WOOD * amount) + ' 🌲\n' + \
                  'Алмазы: ' + str(ORB_DIAMOND * amount) + ' 💎'
    player.save()
    send(player=player, message=message)


def buy_warrior(player, amount=1):
    if player.forge.sword >= (WEAPON * amount) \
            and player.stock.gold >= (PRICE_GOLD * amount):
        player.stock.gold = player.stock.gold - (PRICE_GOLD * amount)
        player.forge.sword = player.forge.sword - (WEAPON * amount)
        player.army.warrior = player.army.warrior + amount
        player.stock.save()
        player.forge.save()
        player.army.save()
        message = 'Вы наняли ' + str(amount) + ' 🗡'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Для ' + str(amount) + ' 🗡👥 нужно:\n' + \
                  'Золото: ' + str(PRICE_GOLD * amount) + ' ✨\n' + \
                  'Мечи: ' + str(WEAPON * amount) + ' 🗡'
    player.save()
    send(player=player, message=message)


def buy_archer(player, amount=1):
    if player.forge.bow >= (WEAPON * amount) \
            and player.stock.gold >= (PRICE_GOLD * amount):
        player.stock.gold = player.stock.gold - (PRICE_GOLD * amount)
        player.forge.bow = player.forge.bow - (WEAPON * amount)
        player.army.archer = player.army.archer + amount
        player.stock.save()
        player.forge.save()
        player.army.save()
        message = 'Вы наняли ' + str(amount) + ' 🏹'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Для ' + str(amount) + ' 🏹👥 нужно:\n' + \
                  'Золото: ' + str(PRICE_GOLD * amount) + ' ✨\n' + \
                  'Луки: ' + str(WEAPON * amount) + ' 🏹\n'
    player.save()
    send(player=player, message=message)


def buy_wizard(player, amount=1):
    if player.forge.orb >= (WEAPON * amount) and player.stock.gold >= (PRICE_GOLD * amount):
        player.stock.gold = player.stock.gold - (PRICE_GOLD * amount)
        player.forge.orb = player.forge.orb - (WEAPON * amount)
        player.army.wizard = player.army.wizard + amount
        player.stock.save()
        player.forge.save()
        player.army.save()
        message = 'Вы наняли ' + str(amount) + ' 🔮'
    else:
        message = 'Недостаточно ресурсов!\n' + \
                  'Для ' + str(amount) + ' 🔮👥 нужно:\n' + \
                  'Золото: ' + str(PRICE_GOLD * amount) + ' ✨\n' + \
                  'Сферы: ' + str(WEAPON * amount) + ' 🔮\n'
    player.save()
    send(player=player, message=message)


def bonus(player, action_time):
    time = action_time - player.bonus_time
    if time > BONUS_TIME:
        player.bonus_time = action_time
        player.stock.stone = player.stock.stone + BONUS_STONE
        player.stock.iron = player.stock.iron + BONUS_IRON
        player.stock.gold = player.stock.gold + BONUS_GOLD
        player.stock.save()
        player.save()
        message = 'Вы получили ежедневный бонус!\n+ ' + \
                  str(BONUS_STONE) + ' ◾\n + ' + \
                  str(BONUS_IRON) + ' ◽\n + ' + \
                  str(BONUS_GOLD) + ' ✨'
    else:
        hour = (BONUS_TIME - time) // 3600
        minutes = ((BONUS_TIME - time) - (hour * 3600)) // 60
        sec = (BONUS_TIME - time) - (minutes * 60) - (hour * 3600)
        message = 'До бонуса: ' + str(hour) + ' ч. ' + str(minutes) + ' м. ' + str(sec) + ' сек.'
    send(player=player, message=message)
