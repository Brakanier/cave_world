from .constant import *
from ..models.inventory import InventoryChest

import random
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def get_random_id():
    """ Get random int32 number (signed) """
    return random.getrandbits(31) * random.choice([-1, 1])


def amount(command):
    count = 1
    part = command.split()
    if len(part) == 2:
        if part[1].isdigit():
            count = int(part[1])
    if len(part) == 3:
        if part[2].isdigit():
            count = int(part[2])
    return count


def in_items(items, slug):
    for item in items:
        if item.slug == slug:
            return item
    return False


def pickaxe_info(items):
    if not in_items(items, 'stone_pickaxe'):
        message_pickaxe_stone = '◾ Каменная кирка ◾: ' + str(STONE_PICKAXE) + icon('stone') + '\n'
    else:
        message_pickaxe_stone = '◾ Каменная кирка ◾: Есть\n'
    if not in_items(items, 'iron_pickaxe'):
        message_pickaxe_iron = '◽ Железная кирка ◽: ' + str(IRON_PICKAXE) + icon('iron') + '\n'
    else:
        message_pickaxe_iron = '◽ Железная кирка ◽: Есть\n'
    if not in_items(items, 'diamond_pickaxe'):
        message_pickaxe_diamond = '💎 Алмазная кирка 💎: ' + str(DIAMOND_PICKAXE) + icon('diamond') + '\n'
    else:
        message_pickaxe_diamond = '💎 Алмазная кирка 💎: Есть\n'
    message = message_pickaxe_stone + message_pickaxe_iron + message_pickaxe_diamond
    return message


def energy(player, action_time):
    delta = action_time - player.last_energy_action
    delta = delta // 60
    if delta >= 6:
        energy_new = (delta // 6) * player.energy_regen
        energy_sum = energy_new + player.energy
        player.energy = min(energy_sum, player.max_energy)
        player.last_energy_action = player.last_energy_action + (energy_new * 360)
    return player


def exp(player, chat_info, exp):
    current_exp = player.exp + exp
    if current_exp >= exp_need(player.lvl):
        more_exp = current_exp - exp_need(player.lvl)
        player.lvl = player.lvl + 1
        player.exp = more_exp
        player.energy = player.max_energy
        message = 'Поздравляю! Вы теперь ' + str(player.lvl) + ' ур.\n' + \
                  'Энергия: ' + str(player.energy) + '/' + str(player.max_energy) + ' ⚡\n'
        send(chat_info, message)
    else:
        player.exp = current_exp
    return player


def new_content(lvl):
    new_content_message = {
        2: icon('craft') + 'Кузница',
        3: icon('craft') + icon('stone') + ' Каменная кирка',
        4: icon('craft') + icon('iron') + ' Железная кирка',
        5: icon('build') + 'Цитадель',
        6: icon('build') + 'Казармы',
        7: icon('build') + 'Таверна',
        9: icon('craft') + icon('diamond') + ' Кристальная кирка',
        10: icon('build') + 'Стрельбище\n' + icon('build') + 'Башня\n' + icon('build') + 'Стена\n' + icon('stone') + 'Каменоломня\n' + icon('wood') + 'Лесопилка\n' + icon('iron') + 'Рудник\n' + icon('diamond') + 'Прииск\n' + icon('war') + 'Нападения на игроков',
        15: icon('build') + 'Башня магов',
    }
    try:
        message = new_content_message[lvl]
    except:
        return False
    return message


def send(chat_info, message, keyboard=None):
    if not message == 'пусто':
        vk = vk_connect()
        if chat_info['user_id'] == chat_info['chat_id']:
            vk.messages.send(
                access_token=token(),
                peer_id=str(chat_info['user_id']),
                keyboard=keyboard,
                message=message,
                random_id=get_random_id()
            )
        else:
            message = '@id' + str(chat_info['user_id']) + '(' + chat_info['nick'] + ')\n' + message
            vk.messages.send(
                access_token=token(),
                peer_id=str(chat_info['peer_id']),
                chat_id=str(chat_info['chat_id']),
                keyboard=keyboard_for_chat(),
                message=message,
                random_id=get_random_id()
            )


def keyboard_for_chat():
    keyboard = VkKeyboard()

    keyboard.add_button('🤴 Лорд', color=VkKeyboardColor.DEFAULT, payload={"command": "профиль"})
    keyboard.add_button('❓ Команды', color=VkKeyboardColor.DEFAULT, payload={"command": "!команды"})
    keyboard.add_button('🎁 Бонус', color=VkKeyboardColor.POSITIVE, payload={"command": "бонус"})

    return keyboard.get_keyboard()


def count_users_chat(chat_info):
    vk = vk_connect()
    users = vk.messages.getConversationMembers(
        access_token=token(),
        peer_id=str(chat_info['peer_id']),
        group_id='176853872',
    )
    return users['count']


def vk_connect():
    vk_session = vk_api.VkApi(token=token())
    vk = vk_session.get_api()
    return vk


def token():
    return '92ea5a422d8e327dbe40934fbeefd4ec722786ce5b63b1db627cc29e2180c45e01dc4eb273910b4b0a30c'


def commands():
    message = 'Список команд:\n' + \
              icon('stock') + ' Ресурсы:\n' + \
              '&#12288;' + icon('stone') + ' Камень [кол-во] - Добывает камень\n' + \
              '&#12288;' + icon('wood') + ' Дерево [кол-во] - Добывает дерево\n' + \
              '&#12288;' + icon('iron') + ' Железо [кол-во] - Добывает железо\n' + \
              '&#12288;' + icon('diamond') + ' Кристаллы [кол-во] - Добывает кристаллы\n' + \
              '&#12288;' + icon('stock') + ' Склад - Посмотреть склад\n' + \
              '\n' + icon('build') + 'Строительство:\n' + \
              '&#12288;' + icon('build') + ' Строить подземелье - Меню строительства в подземелье\n' + \
              '&#12288;' + icon('build') + ' Строить земли - Меню строительства в землях\n' + \
              '&#12288;' + icon('build') + ' Строить [здание] - Построить или улучшить здание\n' + \
              '&#12288;' + icon('build') + ' Список зданий:\n' + \
              '&#12288;&#12288;' + icon('stock') + ' Склад\n' + \
              '&#12288;&#12288;' + icon('craft') + ' Кузница\n' + \
              '&#12288;&#12288;' + icon('tavern') + ' Таверна\n' + \
              '&#12288;&#12288;' + icon('citadel') + ' Цитадель\n' + \
              '&#12288;&#12288;' + icon('sword') + ' Казармы - открывает найм воинов\n' + \
              '&#12288;&#12288;' + icon('target') + ' Стрельбище - открывает найм лучников\n' + \
              '&#12288;&#12288;' + icon('orb') + ' Башня Магов - открывает найм магов\n' + \
              '&#12288;&#12288;' + icon('build') + ' Башня\n' + \
              '&#12288;&#12288;' + icon('build') + ' Стена\n' + \
              '&#12288;&#12288;' + icon('stone') + ' Каменоломня - Добывает камень раз в час\n' + \
              '&#12288;&#12288;' + icon('wood') + ' Лесопилка - Добывает дерево раз в час\n' + \
              '&#12288;&#12288;' + icon('iron') + ' Рудник - Добывает железо раз в час\n' + \
              '&#12288;&#12288;' + icon('diamond') + ' Прииск - Добывает кристаллы раз в час\n' + \
              '\n' + icon('war') + ' Война:\n' + \
              '&#12288;' + icon('sword') + ' Воин [кол-во] - Нанимает воинов\n' + \
              '&#12288;' + icon('bow') + ' Лучник [кол-во] - Нанимает лучников\n' + \
              '&#12288;' + icon('orb') + ' Маг [кол-во] - Нанимает магов\n' + \
              '&#12288;' + icon('war') + ' Армия - Посмотреть свою армию\n' + \
              '&#12288;' + icon('shield') + ' Щит - Проверить наличие щита от нападений\n' + \
              '&#12288;' + icon('search') + ' Поиск - Поиск противника для нападения\n' + \
              '&#12288;' + icon('war') + ' Атака - Напасть на противника\n' + \
              '\n' + icon('craft') + ' Кузница:\n' + \
              '&#12288;' + icon('craft') + ' Ковать [предмет] - Ковать предметы в кузнице\n' + \
              '&#12288;' + icon('craft') + ' Список предметов:\n' + \
              '&#12288;' + icon('get') + icon('stone') + ' Каменная кирка\n' + \
              '&#12288;' + icon('get') + icon('iron') + ' Железная кирка\n' + \
              '&#12288;' + icon('get') + icon('diamond') + ' Кристальная кирка\n' + \
              '\n' + icon('bonus') + icon('cube') + ' Сундуки:\n' + \
              '&#12288;' + icon('bonus') + icon('cube') + ' Открыть [название сундука] - открывает сундук\n' + \
              '&#12288;' + icon('bonus') + icon('cube') + ' Сундуки - Показывает список ваших сундуков\n' + \
              '\n' + icon('other') + ' Разное:\n' + \
              '&#12288;' + icon('citadel') + ' Здания - Информация о ваших зданиях\n' + \
              '&#12288;' + icon('bonus') + ' Бонус - получить ежедневный бонус\n' + \
              '&#12288;' + icon('lvl') + ' Топ лвл - посмотреть топ игроков по уровням\n' + \
              '&#12288;' + icon('profile') + ' Профиль - посмотреть профиль\n' + \
              '&#12288;' + icon('cube') + ' Кости [ресурс] [кол-во] - сыграть в кости\n' + \
              '&#12288;' + icon('other') + ' Репорт [текст] - Написать админам\n'
    return message


def icon(name):
    icons = {
        'wood': ' 🌲',
        'stone': ' ◾',
        'iron': ' ◽',
        'gold': ' ✨',
        'diamond': ' 💎',
        'sword': ' 🗡',
        'bow': ' 🏹',
        'orb': ' 🔮',
        'exp': ' 📚',
        'search': ' 🔎',
        'energy': ' ⚡',
        'get': ' ⛏',
        'build': ' 🔨',
        'skull': ' 💀',
        'craft': ' ⚒',
        'stock': ' 🏤',
        'tavern': ' 🍺',
        'bonus': ' 🎁',
        'enemy': ' 👾',
        'lvl': ' 👑',
        'lose': ' ☠',
        'time': ' ⏳',
        'mans': ' 👥',
        'profile': ' 🤴',
        'war': ' ⚔',
        'target': ' 🎯',
        'citadel': ' 🏰',
        'other': ' 💬',
        'shield': ' 🛡',
        'help': ' ❓',
        'cube': ' 🎲',
    }
    return icons[name]


def exp_need(lvl):
    need = {
        1: 10,
        2: 14,
        3: 17,
        4: 20,
        5: 24,
        6: 29,
        7: 33,
        8: 38,
        9: 48,
        10: 68,
        11: 69,
        12: 71,
        13: 74,
        14: 78,
        15: 83,
        16: 89,
        17: 96,
        18: 104,
        19: 113,
        20: 123,
        21: 134,
        22: 146,
        23: 159,
        24: 173,
        25: 188,
        26: 204,
        27: 221,
        28: 239,
        29: 258,
        30: 278,
        31: 299,
        32: 321,
        33: 344,
        34: 368,
        35: 393,
        36: 398,
        37: 403,
        38: 408,
        39: 413,
        40: 418,
        41: 423,
        42: 428,
        43: 433,
        44: 438,
        45: 443,
        46: 448,
        47: 453,
        48: 458,
        49: 463,
        50: 2000,
    }
    return need[lvl]


def get_keyboard(player, action_time=0):
    keyboard = VkKeyboard()

    if player.place == 'reg':
        name = player.last_name + ' ' + player.first_name
        keyboard.add_button(name, color=VkKeyboardColor.DEFAULT)

    # Профиль

    if player.place == 'profile':
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "земли"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "подземелье"})
        keyboard.add_line()
        keyboard.add_button('Инфо', color=VkKeyboardColor.DEFAULT, payload={"command": "профиль"})
        keyboard.add_button('🔝 Топ 🔝', color=VkKeyboardColor.DEFAULT, payload={"command": "топ"})
        keyboard.add_button('⚔ Армия', color=VkKeyboardColor.DEFAULT, payload={"command": "армия"})
        keyboard.add_line()
        keyboard.add_button('Инвентарь', color=VkKeyboardColor.DEFAULT, payload={"command": "инвентарь"})
        keyboard.add_line()
        color = VkKeyboardColor.POSITIVE
        if action_time - player.bonus_time <= BONUS_TIME:
            color = VkKeyboardColor.NEGATIVE
        keyboard.add_button('🎁 Бонус', color=color, payload={"command": "бонус"})

    if player.place == 'inventory':
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "земли"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "подземелье"})
        keyboard.add_line()
        keyboard.add_button('🎁 Сундуки 🎁', color=VkKeyboardColor.DEFAULT, payload={"command": "сундуки"})
        # keyboard.add_button('Трофей', color=VkKeyboardColor.DEFAULT, payload={"command": "трофеи"})

    if player.place == 'chests':
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "земли"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "подземелье"})

        chests = player.inventory.chests.all()
        for chest in chests:
            title = str(chest.chest.title) + ' - ' + str(chest.count) + ' шт.'
            command = 'открыть ' + str(chest.chest.title)
            keyboard.add_line()
            keyboard.add_button(title, color=VkKeyboardColor.POSITIVE, payload={"command": command})

    if player.place == 'top':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "подземелье"})
        keyboard.add_line()
        keyboard.add_button('👑 По уровню 👑', color=VkKeyboardColor.DEFAULT, payload={"command": "топ лвл"})
        # keyboard.add_line()
        # keyboard.add_button('⚔ По нападениям ⚔', color=VkKeyboardColor.DEFAULT, payload={"command": "top_attack"})
        # keyboard.add_line()
        # keyboard.add_button('🛡 По оборонам 🛡', color=VkKeyboardColor.DEFAULT, payload={"command": "top_defend"})

    # Земли

    elif player.place == 'land':
        if player.build.citadel and player.lvl >= 10:
            keyboard.add_button('⚔ Война', color=VkKeyboardColor.DEFAULT, payload={"command": "война"})
        if player.build.barracks or player.build.archery or player.build.magic:
            keyboard.add_button('🎯 Нанять', color=VkKeyboardColor.DEFAULT, payload={"command": "нанять"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "подземелье"})
        keyboard.add_line()
        keyboard.add_button('🔨 Здания', color=VkKeyboardColor.DEFAULT, payload={"command": "строить земли"})
        keyboard.add_button('🌲 ⛏ Рубить', color=VkKeyboardColor.POSITIVE, payload={"command": "дерево"})
        keyboard.add_line()
        keyboard.add_button('🤴 Лорд', color=VkKeyboardColor.DEFAULT, payload={"command": "профиль"})
        keyboard.add_button('❓ Команды', color=VkKeyboardColor.DEFAULT, payload={"command": "!команды"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})

    # Найм

    elif player.place == 'army':
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "земли"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})
        keyboard.add_line()
        if player.build.barracks:
            keyboard.add_button('🗡 Воин', color=VkKeyboardColor.POSITIVE, payload={"command": "воин"})
        if player.build.archery:
            keyboard.add_button('🏹 Лучник', color=VkKeyboardColor.POSITIVE, payload={"command": "лучник"})
        if player.build.magic:
            keyboard.add_button('🔮 Маг', color=VkKeyboardColor.POSITIVE, payload={"command": "маг"})

    # Земли - Строительство

    elif player.place == 'land_build':
        tower_lvl_up = '🔨 Башня ' + str(player.build.tower_lvl + 1) + ' ур.'
        wall_lvl_up = '🔨 Стена ' + str(player.build.wall_lvl + 1) + ' ур.'
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "земли"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})
        if player.build.citadel:
            if not player.build.barracks:
                keyboard.add_line()
                keyboard.add_button('🗡 Казармы 🗡', color=VkKeyboardColor.DEFAULT, payload={"command": "строить казармы"})
            if not player.build.archery:
                keyboard.add_line()
                keyboard.add_button('🏹 Стрельбище 🏹', color=VkKeyboardColor.DEFAULT, payload={"command": "строить стрельбище"})
            if not player.build.magic:
                keyboard.add_line()
                keyboard.add_button('🔮 Башня магов 🔮', color=VkKeyboardColor.DEFAULT, payload={"command": "строить башня магов"})
        keyboard.add_line()
        keyboard.add_button(tower_lvl_up, color=VkKeyboardColor.POSITIVE, payload={"command": "строить башня"})
        keyboard.add_button(wall_lvl_up, color=VkKeyboardColor.POSITIVE, payload={"command": "строить стена"})
        if player.lvl >= 10:
            stone_mine = '🔨◾ Каменоломня ' + str(player.build.stone_mine_lvl + 1) + ' ур.'
            wood_mine = '🔨🌲 Лесопилка ' + str(player.build.wood_mine_lvl + 1) + ' ур.'
            iron_mine = '🔨◽ Рудник ' + str(player.build.iron_mine_lvl + 1) + ' ур.'
            diamond_mine = '🔨💎 Прииск ' + str(player.build.diamond_mine_lvl + 1) + ' ур.'
            keyboard.add_line()
            keyboard.add_button(stone_mine, color=VkKeyboardColor.POSITIVE, payload={"command": "строить каменоломня"})
            keyboard.add_line()
            keyboard.add_button(wood_mine, color=VkKeyboardColor.POSITIVE, payload={"command": "строить лесопилка"})
            keyboard.add_line()
            keyboard.add_button(iron_mine, color=VkKeyboardColor.POSITIVE, payload={"command": "строить рудник"})
            keyboard.add_line()
            keyboard.add_button(diamond_mine, color=VkKeyboardColor.POSITIVE, payload={"command": "строить прииск"})

    # Подземелье

    elif player.place == 'cave':
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "земли"})
        keyboard.add_button('Шахта', color=VkKeyboardColor.PRIMARY, payload={"command": "шахта"})
        keyboard.add_line()
        keyboard.add_button('🔨 Здания', color=VkKeyboardColor.DEFAULT, payload={"command": "строить подземелье"})
        if player.build.forge:
            keyboard.add_button('⚒ Кузница', color=VkKeyboardColor.DEFAULT, payload={"command": "кузница"})
        if player.build.tavern:
            keyboard.add_button('🍺 Таверна', color=VkKeyboardColor.DEFAULT, payload={"command": "таверна"})
        keyboard.add_line()
        keyboard.add_button('🤴 Лорд', color=VkKeyboardColor.DEFAULT, payload={"command": "профиль"})
        keyboard.add_button('❓ Команды', color=VkKeyboardColor.DEFAULT, payload={"command": "!команды"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})

    # Подземелье - Строительство

    elif player.place == 'cave_build':
        stock_lvl_up = '🔨 🏤 Склад ' + str(player.build.stock.lvl + 1) + ' ур.'
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "подземелье"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})
        keyboard.add_line()
        keyboard.add_button(stock_lvl_up, color=VkKeyboardColor.POSITIVE, payload={"command": "строить склад"})
        if not player.build.citadel:
            keyboard.add_button('🔨 🏰 Цитадель', color=VkKeyboardColor.POSITIVE, payload={"command": "строить цитадель"})
        if not player.build.forge or not player.build.tavern:
            keyboard.add_line()
        if not player.build.forge:
            keyboard.add_button('🔨 ⚒ Кузница', color=VkKeyboardColor.POSITIVE, payload={"command": "строить кузница"})
        if not player.build.tavern:
            keyboard.add_button('🔨 🍺 Таверна', color=VkKeyboardColor.POSITIVE, payload={"command": "строить таверна"})

    # Шахта

    elif player.place == 'mine':
        stone = in_items(player.inventory.items.all(), 'stone_pickaxe')
        iron = in_items(player.inventory.items.all(), 'iron_pickaxe')
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "подземелье"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})
        keyboard.add_line()
        keyboard.add_button('◾⛏ Добыть камень', color=VkKeyboardColor.POSITIVE, payload={"command": "камень"})
        keyboard.add_button('◾⛏ x5', color=VkKeyboardColor.POSITIVE, payload={"command": "камень 5"})
        if stone:
            keyboard.add_line()
            keyboard.add_button('◽⛏ Добыть железо', color=VkKeyboardColor.POSITIVE, payload={"command": "железо"})
            keyboard.add_button('◽⛏ x5', color=VkKeyboardColor.POSITIVE, payload={"command": "железо 5"})
        if iron:
            keyboard.add_line()
            keyboard.add_button('💎⛏ Добыть кристаллы', color=VkKeyboardColor.POSITIVE, payload={"command": "кристаллы"})
            keyboard.add_button('💎⛏ x5', color=VkKeyboardColor.POSITIVE, payload={"command": "кристаллы 5"})

    # Кузница

    elif player.place == 'forge':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "подземелье"})
        keyboard.add_line()
        keyboard.add_button('⚒ ⛏ Кирки', color=VkKeyboardColor.DEFAULT, payload={"command": "кирки"})

    # Кузница - крафт кирок

    elif player.place == 'forge_pickaxe':
        stone = in_items(player.inventory.items.all(), 'stone_pickaxe')
        iron = in_items(player.inventory.items.all(), 'iron_pickaxe')
        diamond = in_items(player.inventory.items.all(), 'diamond_pickaxe')
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "подземелье"})
        keyboard.add_button('⛏ Кирки', color=VkKeyboardColor.DEFAULT, payload={"command": "кирки"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})
        if not stone or not iron:
            keyboard.add_line()
            if not iron:
                keyboard.add_button('⛏ ◽ Железная', color=VkKeyboardColor.POSITIVE,
                                    payload={"command": "ковать железная кирка"})
            if not stone:
                keyboard.add_button('⛏ ◾ Каменная', color=VkKeyboardColor.POSITIVE,
                                    payload={"command": "ковать каменная кирка"})
        if not diamond:
            keyboard.add_line()
            keyboard.add_button('⛏ 💎 Кристальная', color=VkKeyboardColor.POSITIVE,
                                payload={"command": "ковать кристальная кирка"})

    # Таверна

    elif player.place == 'tavern':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "подземелье"})
        keyboard.add_line()
        keyboard.add_button('🎲 Кости 🎲', color=VkKeyboardColor.POSITIVE, payload={"command": "кости"})
        # keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})
        # keyboard.add_button('⚔ Арсенал', color=VkKeyboardColor.DEFAULT, payload={"command": "forge_kit_info"})

    # Война

    elif player.place == 'war':
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "земли"})
        keyboard.add_button('⚔👥 Армия', color=VkKeyboardColor.DEFAULT, payload={"command": "армия"})
        if player.lvl >= 10:
            keyboard.add_line()
            keyboard.add_button('🔎 Поиск', color=VkKeyboardColor.POSITIVE, payload={"command": "поиск"})
            keyboard.add_button('⚔ Напасть', color=VkKeyboardColor.NEGATIVE, payload={"command": "атака"})
            keyboard.add_line()
            keyboard.add_button('🛡 Щит ⏳', color=VkKeyboardColor.DEFAULT, payload={"command": "щит"})

    return keyboard.get_keyboard()
