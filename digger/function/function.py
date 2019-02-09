import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from .CONSTANT import *


def get_random_id():
    """ Get random int32 number (signed) """
    return random.getrandbits(31) * random.choice([-1, 1])


def energy(player, action_time):
    delta = action_time - player.last_energy_action
    delta = delta//60
    if delta >= 5:
        energy_new = (delta//5) * player.energy_regen
        energy_max = energy_new + player.energy
        player.energy = min(energy_max, player.max_energy)
        player.last_energy_action = player.last_energy_action + (energy_new*300)
    return player


def exp(vk, player, token, exp):
    current_exp = player.exp + exp
    if current_exp >= player.exp_need:
        more_exp = current_exp - player.exp_need
        player.lvl = player.lvl + 1
        player.exp = more_exp
        player.exp_need = ((player.lvl ** LVL_Z)*LVL_X) - player.exp_need
        player.max_energy = 10 + (player.lvl * 2)
        player.energy = player.max_energy
        message = 'Поздравляю! Вы теперь ' + str(player.lvl) + ' ур.\n' + \
                  'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n'
        vk.messages.send(
            access_token=token,
            user_id=str(player.user_id),
            keyboard=get_keyboard(player=player),
            message=message,
            random_id=get_random_id()
        )
    else:
        player.exp = current_exp
    return player


def get_keyboard(player, action_time=0):
    keyboard = VkKeyboard()

    if player.place == 'reg':
        name = player.last_name + ' ' + player.first_name
        keyboard.add_button(name, color=VkKeyboardColor.DEFAULT)

    # Профиль

    if player.place == 'profile':
        if player.build.gate:
            keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_line()
        keyboard.add_button('Инфо', color=VkKeyboardColor.DEFAULT, payload={"command": "profile"})
        keyboard.add_button('⚔ Армия', color=VkKeyboardColor.DEFAULT, payload={"command": "army"})
        keyboard.add_line()
        color = VkKeyboardColor.POSITIVE
        if action_time - player.bonus_time <= BONUS_TIME:
            color = VkKeyboardColor.NEGATIVE
        keyboard.add_button('🎁 Бонус', color=color, payload={"command": "bonus"})

    # Земли

    elif player.place == 'land':
        keyboard.add_button('⚔ Война', color=VkKeyboardColor.NEGATIVE, payload={"command": "war"})
        keyboard.add_button('🎯 Поход', color=VkKeyboardColor.NEGATIVE, payload={"command": "crusade"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_line()
        keyboard.add_button('🔨 Здания', color=VkKeyboardColor.DEFAULT, payload={"command": "land_build"})
        keyboard.add_button('🌲 ⛏ Рубить', color=VkKeyboardColor.POSITIVE, payload={"command": "cut_wood"})
        keyboard.add_line()
        keyboard.add_button('🤴 Персонаж', color=VkKeyboardColor.DEFAULT, payload={"command": "profile"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})

    # Земли - Строительство

    elif player.place == 'land_build':
        tower_lvl_up = '🔨 Башня ' + str(player.build.tower_lvl + 1) + ' ур.'
        wall_lvl_up = '🔨 Стена ' + str(player.build.wall_lvl + 1) + ' ур.'
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})
        keyboard.add_line()
        keyboard.add_button(tower_lvl_up, color=VkKeyboardColor.POSITIVE, payload={"command": "build_tower"})
        keyboard.add_button(wall_lvl_up, color=VkKeyboardColor.POSITIVE, payload={"command": "build_wall"})

    # Подземелье

    elif player.place == 'cave':
        if player.build.gate:
            keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('Шахта', color=VkKeyboardColor.PRIMARY, payload={"command": "mine"})
        keyboard.add_line()
        keyboard.add_button('🔨 Здания', color=VkKeyboardColor.DEFAULT, payload={"command": "cave_build"})
        if player.build.forge:
            keyboard.add_button('⚒ Кузница', color=VkKeyboardColor.DEFAULT, payload={"command": "forge"})
        if player.build.tavern:
            keyboard.add_button('⚔ Таверна', color=VkKeyboardColor.DEFAULT, payload={"command": "tavern"})
        keyboard.add_line()
        keyboard.add_button('🤴 Персонаж', color=VkKeyboardColor.DEFAULT, payload={"command": "profile"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})

    # Подземелье - Строительство

    elif player.place == 'cave_build':
        stock_lvl_up = '🔨 🏤 Склад ' + str(player.stock.lvl + 1) + ' ур.'
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})
        keyboard.add_line()
        keyboard.add_button(stock_lvl_up, color=VkKeyboardColor.POSITIVE, payload={"command": "build_stock"})
        if not player.build.gate:
            keyboard.add_button('🔨 Врата', color=VkKeyboardColor.POSITIVE, payload={"command": "build_gate"})
        if not player.build.forge or not player.build.tavern:
            keyboard.add_line()
        if not player.build.forge:
            keyboard.add_button('🔨 ⚒ Кузница', color=VkKeyboardColor.POSITIVE, payload={"command": "build_forge"})
        if not player.build.tavern:
            keyboard.add_button('🔨 🍺 Таверна', color=VkKeyboardColor.POSITIVE, payload={"command": "build_tavern"})

    # Шахта

    elif player.place == 'mine':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})
        keyboard.add_line()
        keyboard.add_button('◾⛏ Добыть камень', color=VkKeyboardColor.POSITIVE, payload={"command": "dig_stone"})
        if player.forge.pickaxe_iron or player.forge.pickaxe_diamond or player.forge.pickaxe_skull:
            keyboard.add_button('💎⛏ Добыть алмазы', color=VkKeyboardColor.POSITIVE, payload={"command": "dig_diamond"})
        if player.forge.pickaxe_stone:
            keyboard.add_line()
            keyboard.add_button('◽⛏ Добыть железо', color=VkKeyboardColor.POSITIVE, payload={"command": "dig_iron"})
            keyboard.add_button('✨⛏ Добыть золото', color=VkKeyboardColor.POSITIVE, payload={"command": "dig_gold"})

    # Кузница

    elif player.place == 'forge':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_line()
        keyboard.add_button('⚒ ⛏ Кирки', color=VkKeyboardColor.DEFAULT, payload={"command": "forge_pickaxe"})
        keyboard.add_button('⚒ ⚔ Арсенал', color=VkKeyboardColor.DEFAULT, payload={"command": "forge_kit"})

    # Кузница - крафт наборов

    elif player.place == 'forge_kit':
        keyboard.add_button('Кузница', color=VkKeyboardColor.PRIMARY, payload={"command": "forge"})
        keyboard.add_button('⚔ Арсенал', color=VkKeyboardColor.DEFAULT, payload={"command": "forge_kit_info"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})
        keyboard.add_line()
        keyboard.add_button('⚒ 🗡 Меч', color=VkKeyboardColor.POSITIVE, payload={"command": "craft_sword"})
        keyboard.add_button('⚒ 🏹 Лук', color=VkKeyboardColor.POSITIVE, payload={"command": "craft_bow"})
        keyboard.add_line()
        keyboard.add_button('⚒ 🔮 Сфера', color=VkKeyboardColor.POSITIVE, payload={"command": "craft_orb"})

    # Кузница - крафт кирок

    elif player.place == 'forge_pickaxe':
        keyboard.add_button('Кузница', color=VkKeyboardColor.PRIMARY, payload={"command": "forge"})
        keyboard.add_button('⛏ Кирки', color=VkKeyboardColor.DEFAULT, payload={"command": "forge_pickaxe_info"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})
        if not player.forge.pickaxe_iron or not player.forge.pickaxe_stone:
            keyboard.add_line()
            if not player.forge.pickaxe_iron:
                keyboard.add_button('⛏ ◽ Железная', color=VkKeyboardColor.POSITIVE, payload={"command": "craft_pickaxe_iron"})
            if not player.forge.pickaxe_stone:
                keyboard.add_button('⛏ ◾ Каменная', color=VkKeyboardColor.POSITIVE, payload={"command": "craft_pickaxe_stone"})
        if not player.forge.pickaxe_skull or not player.forge.pickaxe_diamond:
            keyboard.add_line()
            if not player.forge.pickaxe_skull:
                keyboard.add_button('⛏ 💀 Костяная', color=VkKeyboardColor.POSITIVE, payload={"command": "craft_pickaxe_skull"})
            if not player.forge.pickaxe_diamond:
                keyboard.add_button('⛏ 💎 Алмазная', color=VkKeyboardColor.POSITIVE, payload={"command": "craft_pickaxe_diamond"})

    # Таверна

    elif player.place == 'tavern':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})
        keyboard.add_button('⚔ Арсенал', color=VkKeyboardColor.DEFAULT, payload={"command": "forge_kit_info"})
        keyboard.add_line()
        keyboard.add_button('🍺 🗡 Воин', color=VkKeyboardColor.POSITIVE, payload={"command": "buy_warrior"})
        keyboard.add_button('🍺 🏹 Лучник', color=VkKeyboardColor.POSITIVE, payload={"command": "buy_archer"})
        keyboard.add_line()
        keyboard.add_button('🍺 🔮 Маг', color=VkKeyboardColor.POSITIVE, payload={"command": "buy_wizard"})
        keyboard.add_line()
        keyboard.add_button('⚔ Армия', color=VkKeyboardColor.DEFAULT, payload={"command": "army"})

    # Война

    elif player.place == 'war':
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('⚔ Армия', color=VkKeyboardColor.DEFAULT, payload={"command": "army"})
        keyboard.add_line()
        keyboard.add_button('🔎 Поиск', color=VkKeyboardColor.POSITIVE, payload={"command": "find_enemy"})
        keyboard.add_button('⚔ Напасть', color=VkKeyboardColor.NEGATIVE, payload={"command": "attack"})
        keyboard.add_line()
        keyboard.add_button('🛡 Щит ⏳', color=VkKeyboardColor.DEFAULT, payload={"command": "shield_info"})

    return keyboard.get_keyboard()
