from .constant import *
from ..models.inventory import InventoryChest


import random
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def get_random_id():
    """ Get random int32 number (signed) """
    return random.getrandbits(31) * random.choice([-1, 1])


def get_id(url):
    screen_name = url.split('/')[-1]
    vk = vk_connect()
    r = vk.utils.resolveScreenName(screen_name=screen_name)
    if r and r['type'] == 'user':
        user_id = int(r['object_id'])
    else:
        user_id = None

    return user_id


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
        message_pickaxe_stone += 'Открывает добычу Железа.\n\n'
    else:
        message_pickaxe_stone = '◾ Каменная кирка ◾: Есть\n'
    if not in_items(items, 'iron_pickaxe'):
        message_pickaxe_iron = '◽ Железная кирка ◽: ' + str(IRON_PICKAXE) + icon('iron') + '\n'
        message_pickaxe_iron += 'Открывает добычу Кристаллов.\n\n'
    else:
        message_pickaxe_iron = '◽ Железная кирка ◽: Есть\n'
    if not in_items(items, 'diamond_pickaxe'):
        message_pickaxe_diamond = '💎 Кристальная кирка 💎: ' + str(DIAMOND_PICKAXE) + icon('diamond') + '\n'
        message_pickaxe_diamond += 'Увеличивает добычу в 2 раза.\n\n'
    else:
        message_pickaxe_diamond = '💎 Кристальная кирка 💎: Есть\n'
    if not in_items(items, 'skull_pickaxe'):
        message_skull_diamond = '💀 Костяная кирка 💀: ' + str(SKULL_PICKAXE) + icon('skull') + '\n'
        message_skull_diamond += 'Увеличивает добычу в 3 раза.\n\n'
    else:
        message_skull_diamond = '💀 Костяная кирка 💀: Есть\n'

    message = message_pickaxe_stone + message_pickaxe_iron + message_pickaxe_diamond + message_skull_diamond
    return message


def energy(player, action_time):
    delta = action_time - player.last_energy_action
    delta = delta // 60
    if delta >= 6:
        energy_new = (delta // 6) * player.energy_regen
        energy_sum = energy_new + player.energy
        if player.energy < player.max_energy:
            player.energy = min(energy_sum, player.max_energy)
        player.last_energy_action = player.last_energy_action + (energy_new * 360)
    return player


def exp(player, chat_info, exp):
    current_exp = player.exp + exp
    if current_exp >= exp_need(player.lvl):
        more_exp = current_exp - exp_need(player.lvl)
        player.lvl = player.lvl + 1
        player.exp = more_exp
        player.energy += 20
        message = 'Поздравляю! Вы теперь ' + str(player.lvl) + ' ур.\n' + \
                  'Награда:\n' + \
                  'Энергия: + 20 ⚡\n'
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
    if message is None:
        return
    vk = vk_connect()
    if chat_info['user_id'] == chat_info['chat_id']:
        try:
            vk.messages.send(
                access_token=token(),
                peer_id=str(chat_info['user_id']),
                keyboard=keyboard,
                message=message,
                random_id=0,
                disable_mentions=1,
            )
        except:
            pass
    else:
        message = '[id' + str(chat_info['user_id']) + '|' + chat_info['nick'] + ']\n' + message
        try:
            vk.messages.send(
                access_token=token(),
                peer_id=str(chat_info['peer_id']),
                chat_id=str(chat_info['chat_id']),
                keyboard=keyboard_for_chat(),
                message=message,
                random_id=0,
                disable_mentions=1,
            )
        except:
            pass


def send_comment(post_id, comment_id, message):
    vk = vk_connect()
    vk.wall.createComment(
        owner_id=-176853872,
        post_id=post_id,
        from_group=1,
        reply_to_comment=comment_id,
        message=message,
    )


def coins(player, action_time):
    delta = action_time - player.fortune_time
    hours = delta // 3600
    if hours >= 10:
        coin_new = (hours // 10) * 1
        coin_sum = coin_new + player.fortune_coin
        if player.fortune_coin < 2:
            player.fortune_coin = min(coin_sum, 2)
        player.fortune_time = player.fortune_time + (coin_new * 3600 * 10)


def keyboard_for_chat():
    keyboard = VkKeyboard()

    keyboard.add_button('❓ Команды', color=VkKeyboardColor.DEFAULT, payload={"command": "команды"})
    keyboard.add_button('🤴 Лорд', color=VkKeyboardColor.DEFAULT, payload={"command": "профиль"})
    keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})

    return keyboard.get_keyboard()


def chat_list():
    mess = 'Список бесед с ботом:\n' + \
           '1) Игровая беседа #1 - https://vk.me/join/AJQ1d3CbaQ5UNU4dBAao3OhI \n'
    return mess


def count_users_chat(chat_info):
    vk = vk_connect()
    users = vk.messages.getConversationMembers(
        access_token=token(),
        peer_id=str(chat_info['peer_id']),
        group_id='176853872',
    )
    return users['count']


def is_admin(user_id, chat_info):
    vk = vk_connect()
    members = vk.messages.getConversationMembers(
        access_token=token(),
        peer_id=chat_info['peer_id'],
        group_id='176853872',
    )
    admins_ids = (member['member_id'] for member in members['items'] if 'is_admin' in member)
    if user_id in admins_ids:
        is_admin = True
    else:
        is_admin = False

    return is_admin


def vk_connect():
    vk_session = vk_api.VkApi(token=token())
    vk = vk_session.get_api()
    return vk


def token():
    return '92ea5a422d8e327dbe40934fbeefd4ec722786ce5b63b1db627cc29e2180c45e01dc4eb273910b4b0a30c'


def commands(player):

    # РЕСУРСЫ

    res = '\n⬇ РЕСУРСЫ ⬇\n\n'
    stock = icon('stock') + ' Склад - Посмотреть склад\n'
    stone = icon('stone') + ' Камень [кол-во] - Добывает камень\n'
    wood = icon('wood') + ' Дерево [кол-во] - Добывает дерево\n'
    iron = icon('iron') + ' Железо [кол-во] - Добывает железо\n'
    diamond = icon('diamond') + ' Кристаллы [кол-во] - Добывает кристаллы\n'

    if not in_items(player.inventory.items.all(), 'stone_pickaxe'):
        iron = ''
    if not in_items(player.inventory.items.all(), 'iron_pickaxe'):
        diamond = ''

    # Здания

    builds = '\n⬇ ЗДАНИЯ ⬇\n\n' + icon('citadel') + ' Здания - информация о ваших зданиях\n'
    build = icon('build') + ' Строить - список доступных зданий для постройки\n'
    build_stock = icon('stock') + ' Строить Склад - больше места\n'
    build_forge = icon('craft') + ' Строить Кузница - позволяет ковать инструменты\n'
    build_tavern = icon('tavern') + ' Строить Таверна - открывает игру в "Кости"\n'
    build_market = icon('gold') + ' Строить Рынок - купить/продать/отправить ресурсы\n'
    build_citadel = icon('citadel') + ' Строить Цитадель - открывает доступ к новым зданиям\n'
    build_barracks = icon('sword') + ' Строить Казармы - открывает найм Воинов\n'
    build_archery = icon('target') + ' Строить Стрельбище - открывает найм Лучников\n'
    build_magic = icon('orb') + ' Строить Башня Магов - открывает найм Магов\n'
    build_wall = icon('build') + ' Строить Стена - улучшает защиту\n'
    build_tower = icon('build') + ' Строить Башня - улучшает атаку\n'
    build_stone_mine = icon('stone') + ' Строить Каменоломня - добывает Камень раз в час\n'
    build_wood_mine = icon('wood') + ' Строить Лесопилка - добывает Дерево раз в час\n'
    build_iron_mine = icon('iron') + ' Строить Рудник - добывает Железо раз в час\n'
    build_diamond_mine = icon('diamond') + ' Строить Прииск - добывает Кристаллы раз в час\n'

    if player.build.forge:
        build_forge = ''
    if player.build.tavern:
        build_tavern = ''
    if player.build.market_lvl >= 10:
        build_market = ''
    if player.build.barracks:
        build_barracks = ''
    if player.build.archery:
        build_archery = ''
    if player.build.magic:
        build_magic = ''
    if player.build.citadel:
        build_citadel = ''
    else:
        build_barracks = ''
        build_archery = ''
        build_magic = ''
        build_wall = ''
        build_tower = ''
        build_stone_mine = ''
        build_wood_mine = ''
        build_iron_mine = ''
        build_diamond_mine = ''

    # КРАФТ

    forge = '\n⬇ КУЗНИЦА ⬇\n\n' + icon('craft') + ' Кузница - крафт инфо\n'
    pickaxes = icon('craft') + ' Кирки - список кирок\n'
    craft_stone = icon('get') + icon('stone') + ' Ковать Каменная кирка\n'
    craft_iron = icon('get') + icon('iron') + ' Ковать Железная кирка\n'
    craft_diamond = icon('get') + icon('diamond') + ' Ковать Кристальная кирка\n'

    if not player.build.forge:
        forge = ''
        pickaxes = ''
        craft_stone = ''
        craft_iron = ''
        craft_diamond = ''

    if in_items(player.inventory.items.all(), 'stone_pickaxe'):
        craft_stone = ''
    if in_items(player.inventory.items.all(), 'iron_pickaxe'):
        craft_iron = ''
    if in_items(player.inventory.items.all(), 'diamond_pickaxe'):
        craft_diamond = ''
    if in_items(player.inventory.items.all(), 'stone_pickaxe') and in_items(player.inventory.items.all(), 'iron_pickaxe') and in_items(player.inventory.items.all(), 'diamond_pickaxe'):
        forge = ''
        pickaxes = ''

    # ВОЙНА

    war = '\n⬇ СРАЖЕНИЯ ⬇\n\n' + icon('war') + ' Война - война инфо\n'
    war_search = icon('search') + ' Поиск - поиск противника\n'
    war_scouting = icon('search') + ' Разведка - информация о противнике (10' + icon('diamond') + ')\n'
    war_attack = icon('war') + ' Атака - атака противника\n'
    war_shield = icon('shield') + ' Щит - наличие щита\n'
    buy_info = icon('target') + ' Найм - стоимость найма\n'
    warrior = icon('sword') + ' Воин [кол-во] - нанимает Воинов\n'
    archer = icon('bow') + ' Лучник [кол-во] - нанимает Лучников\n'
    wizard = icon('orb') + ' Маг [кол-во] - нанимает Магов\n'
    army = icon('war') + ' Армия - ваша армия\n'
    buy_equally = ''

    if player.build.barracks and player.build.archery and player.build.magic:
        buy_equally = icon('war') + ' Нанять макс - нанимает на все ресурсы поровну\n'

    if player.lvl < 10:
        war_search = ''
        war_scouting = ''
        war_attack = ''
        war_shield = ''
        if not player.build.citadel:
            war = ''
            buy_info = ''
            warrior = ''
            archer = ''
            wizard = ''
            army = ''
    if not player.build.barracks:
        warrior = ''
    if not player.build.archery:
        archer = ''
    if not player.build.magic:
        wizard = ''

    # СУНДУКИ

    chests = '\n⬇ СУНДУКИ ⬇\n\n' + icon('bonus') + icon('cube') + ' Сундуки - список ваших сундуков\n'
    open_chest = icon('bonus') + icon('cube') + ' Открыть [название сундука] - открывает сундук\n'

    # РАЗНОЕ

    caves = icon('web') + ' Пещеры - Исследование пещер\n'

    hunt = icon('target') + ' Охота - информация об охоте\n'
    market = icon('gold') + ' Рынок - купить/продать ресурсы\n'
    bones = icon('cube') + ' Кости [ресурс] [кол-во] - сыграть в кости\n'

    if player.build.market_lvl == 0:
        market = ''
    if not player.build.tavern:
        bones = ''
    if not player.build.citadel:
        caves = ''

    message = 'Список доступных команд:\n' + \
              res + \
              stock + \
              stone + \
              wood + \
              iron + \
              diamond + \
              builds + \
              build + \
              build_stock + \
              build_forge + \
              build_tavern + \
              build_market + \
              build_citadel + \
              build_barracks + \
              build_archery + \
              build_magic + \
              build_wall + \
              build_tower + \
              build_stone_mine + \
              build_wood_mine + \
              build_iron_mine + \
              build_diamond_mine + \
              forge + \
              pickaxes + \
              craft_stone + \
              craft_iron + \
              craft_diamond + \
              war + \
              war_search + \
              war_scouting + \
              war_attack + \
              war_shield + \
              buy_info + \
              warrior + \
              archer + \
              wizard + \
              buy_equally + \
              army + \
              chests + \
              open_chest + \
              '\n⬇ РАЗНОЕ ⬇\n\n' + \
              hunt + \
              caves + \
              bones + \
              market + \
              icon('skull') + ' Алтарь - дары Хранителю Подземелья\n' + \
              icon('bonus') + ' Бонус - получить ежедневный бонус\n' + \
              icon('lvl') + ' Топ - посмотреть топ игроков\n' + \
              icon('profile') + ' Лорд - посмотреть свой профиль\n' + \
              icon('other') + ' Ник [новый ник] - сменить ник\n' + \
              '❤ ' + 'Донат - поддержка проекта\n' + \
              icon('help') + ' Помощь - подробное описание всех команд\n' + \
              '⚙ ' + '!команды - управление беседой\n' + \
              icon('other') + ' Репорт [текст] - написать админам\n' + \
              '\nКоманды открываются с уровнем и постройкой зданий!\n' + \
              '\nЕсли вам что-то непонятно, воспользуйтесь командой "Репорт"'
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
        'web': ' 🕸',
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
        11: 79,
        12: 91,
        13: 104,
        14: 118,
        15: 133,
        16: 149,
        17: 166,
        18: 184,
        19: 203,
        20: 223,
        21: 244,
        22: 266,
        23: 289,
        24: 313,
        25: 338,
        26: 364,
        27: 391,
        28: 419,
        29: 448,
        30: 478,
        31: 509,
        32: 541,
        33: 574,
        34: 608,
        35: 643,
        36: 679,
        37: 716,
        38: 754,
        39: 793,
        40: 833,
        41: 874,
        42: 916,
        43: 959,
        44: 1003,
        45: 1048,
        46: 1094,
        47: 1141,
        48: 1189,
        49: 1238,
        50: 1288,
        51: 1339,
        52: 1391,
        53: 1444,
        54: 1498,
        55: 1553,
        56: 1609,
        57: 1666,
        58: 1724,
        59: 1783,
        60: 3000,
    }
    return need[lvl]


def get_keyboard(player, action_time=0):
    keyboard = VkKeyboard()

    if player.place == 'reg':
        name = player.last_name + ' ' + player.first_name
        keyboard.add_button(name, color=VkKeyboardColor.DEFAULT)
        keyboard.add_button(name, color=VkKeyboardColor.DEFAULT)

    # Профиль

    if player.place == 'profile':
        if player.lvl >= 3:
            keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('💬 Инфо 💬', color=VkKeyboardColor.DEFAULT, payload={"command": "профиль"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_line()
        keyboard.add_button('🔝 Топ 🔝', color=VkKeyboardColor.DEFAULT, payload={"command": "топ"})
        keyboard.add_button('Инвентарь', color=VkKeyboardColor.DEFAULT, payload={"command": "inventory"})
        keyboard.add_line()
        keyboard.add_button('❤ Донат ❤', color=VkKeyboardColor.DEFAULT, payload={"command": "донат"})
        keyboard.add_line()
        keyboard.add_button('💬 Беседы 💬', color=VkKeyboardColor.DEFAULT, payload={"command": "беседы"})
        color = VkKeyboardColor.POSITIVE
        if action_time - player.bonus_time <= BONUS_TIME:
            color = VkKeyboardColor.NEGATIVE
        keyboard.add_button('🎁 Бонус', color=color, payload={"command": "бонус"})

    if player.place == 'inventory':
        keyboard.add_button('⬅ Назад', color=VkKeyboardColor.DEFAULT, payload={"command": "лорд"})
        if player.lvl >= 3:
            keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_line()
        keyboard.add_button('🎁 Сундуки 🎁', color=VkKeyboardColor.DEFAULT, payload={"command": "сундуки"})
        # keyboard.add_button('Трофей', color=VkKeyboardColor.DEFAULT, payload={"command": "трофеи"})

    if player.place == 'chests':
        keyboard.add_button('⬅ Назад', color=VkKeyboardColor.DEFAULT, payload={"command": "inventory"})
        if player.lvl >= 3:
            keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})

        chests = player.inventory.chests.all()
        for chest in chests:
            title = str(chest.chest.title) + ' - ' + str(chest.count) + ' шт.'
            command = 'открыть ' + str(chest.chest.title)
            if chest.count > 0:
                keyboard.add_line()
                keyboard.add_button(title, color=VkKeyboardColor.POSITIVE, payload={"command": command})

    if player.place == 'top':
        if player.lvl >= 3:
            keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_line()
        keyboard.add_button('👑 По уровню 👑', color=VkKeyboardColor.DEFAULT, payload={"command": "топ лвл"})
        keyboard.add_button('🔨 По зданиям 🔨', color=VkKeyboardColor.DEFAULT, payload={"command": "топ здания"})
        keyboard.add_line()
        keyboard.add_button('⚔ По атакам ⚔', color=VkKeyboardColor.DEFAULT, payload={"command": "топ атака"})
        keyboard.add_button('🛡 По оборонам 🛡', color=VkKeyboardColor.DEFAULT, payload={"command": "топ защита"})
        keyboard.add_line()
        keyboard.add_button('💀 По черепам 💀', color=VkKeyboardColor.DEFAULT, payload={"command": "топ череп"})
        keyboard.add_button('✨ По золоту ✨', color=VkKeyboardColor.DEFAULT, payload={"command": "топ золото"})
        '''
        keyboard.add_line()
        keyboard.add_button('🕸 По пещерам 🕸', color=VkKeyboardColor.DEFAULT, payload={"command": "топ пещеры"})
        '''

    # Земли

    elif player.place == 'land':
        keyboard.add_button('🏰 Цитадель 🏰', color=VkKeyboardColor.PRIMARY, payload={"command": "цитадель"})
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        if player.build.citadel:
            keyboard.add_line()
            keyboard.add_button('🔨 Строить', color=VkKeyboardColor.DEFAULT, payload={"command": "build_land"})
            keyboard.add_button('🏰 Здания', color=VkKeyboardColor.DEFAULT, payload={"command": "здания"})
        if player.build.market_lvl > 0:
            keyboard.add_button('✨ Рынок', color=VkKeyboardColor.DEFAULT, payload={"command": "рынок"})
        keyboard.add_line()
        keyboard.add_button('🌲 ⛏ Рубить', color=VkKeyboardColor.POSITIVE, payload={"command": "дерево"})
        keyboard.add_button('🌲 ⛏ х5', color=VkKeyboardColor.POSITIVE, payload={"command": "дерево 5"})
        keyboard.add_line()
        keyboard.add_button('🤴 Лорд', color=VkKeyboardColor.DEFAULT, payload={"command": "профиль"})
        keyboard.add_button('❓ Команды', color=VkKeyboardColor.DEFAULT, payload={"command": "команды"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})

    # Цитадель

    elif player.place == 'citadel':
        if player.build.barracks or player.build.archery or player.build.magic:
            keyboard.add_button('🎯 Нанять', color=VkKeyboardColor.DEFAULT, payload={"command": "найм"})
        keyboard.add_button('💬 Инфо', color=VkKeyboardColor.DEFAULT, payload={"command": "цитадель"})
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_line()
        keyboard.add_button('🎯 Охота 🎯', color=VkKeyboardColor.DEFAULT, payload={"command": "охота"})
        if player.lvl >= 10:
            keyboard.add_line()
            find_time = action_time - player.war.find_last_time
            if find_time >= FIND_TIME:
                color = VkKeyboardColor.POSITIVE
            else:
                color = VkKeyboardColor.NEGATIVE
            keyboard.add_button('🔎 Поиск', color=color, payload={"command": "поиск"})

            war_time = action_time - player.war.war_last_time
            attack_color = VkKeyboardColor.NEGATIVE
            if war_time >= WAR_TIME and player.war.enemy_id:
                attack_color = VkKeyboardColor.POSITIVE
            keyboard.add_button('⚔ Напасть', color=attack_color, payload={"command": "атака"})
            if player.war.enemy_id:
                keyboard.add_line()
                keyboard.add_button('🔎 Разведка (10 💎)', color=VkKeyboardColor.POSITIVE,
                                    payload={"command": "разведка"})

    # Охота

    elif player.place == 'hunt':
        keyboard.add_button('⬅ Назад', color=VkKeyboardColor.DEFAULT, payload={"command": "цитадель"})
        keyboard.add_button('💬 Инфо', color=VkKeyboardColor.DEFAULT, payload={"command": "охота"})
        if player.war.warrior or player.war.archer or player.war.wizard:
            keyboard.add_line()
            keyboard.add_button('🗡 Воины', color=VkKeyboardColor.POSITIVE, payload={"command": "охота воин"})
            keyboard.add_button('🏹 Лучники', color=VkKeyboardColor.POSITIVE, payload={"command": "охота лучник"})
            keyboard.add_button('🔮 Маги', color=VkKeyboardColor.POSITIVE, payload={"command": "охота маг"})
        keyboard.add_line()
        keyboard.add_button('⚔ Армия', color=VkKeyboardColor.DEFAULT, payload={"command": "армия"})

    # Найм

    elif player.place == 'army':
        keyboard.add_button('⬅ Назад', color=VkKeyboardColor.PRIMARY, payload={"command": "цитадель"})
        keyboard.add_button('💬 Инфо', color=VkKeyboardColor.DEFAULT, payload={"command": "найм"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})
        if player.build.barracks or player.build.archery or player.build.magic:
            keyboard.add_line()
            if player.build.barracks:
                keyboard.add_button('🗡 Воин', color=VkKeyboardColor.POSITIVE, payload={"command": "воин"})
            if player.build.archery:
                keyboard.add_button('🏹 Лучник', color=VkKeyboardColor.POSITIVE, payload={"command": "лучник"})
            if player.build.magic:
                keyboard.add_button('🔮 Маг', color=VkKeyboardColor.POSITIVE, payload={"command": "маг"})
            keyboard.add_line()
            if player.build.barracks:
                keyboard.add_button('🗡 х5', color=VkKeyboardColor.POSITIVE, payload={"command": "воин 5"})
            if player.build.archery:
                keyboard.add_button('🏹 х5', color=VkKeyboardColor.POSITIVE, payload={"command": "лучник 5"})
            if player.build.magic:
                keyboard.add_button('🔮 х5', color=VkKeyboardColor.POSITIVE, payload={"command": "маг 5"})
        if player.build.barracks and player.build.archery and player.build.magic:
            keyboard.add_line()
            keyboard.add_button('Нанять макс. поровну 🗡=🏹=🔮', color=VkKeyboardColor.POSITIVE, payload={"command": "нанять макс"})
        keyboard.add_line()
        keyboard.add_button('⚔ Армия', color=VkKeyboardColor.DEFAULT, payload={"command": "армия"})

    # Земли - Строительство

    elif player.place == 'land_build':
        tower_lvl_up = '🔨 Башня ' + str(player.build.tower_lvl + 1) + ' ур.'
        wall_lvl_up = '🔨 Стена ' + str(player.build.wall_lvl + 1) + ' ур.'
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('💬 Инфо', color=VkKeyboardColor.DEFAULT, payload={"command": "build_land"})
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
        if player.build.tower_lvl < 30 or player.build.wall_lvl < 30:
            keyboard.add_line()
            if player.build.tower_lvl < 30:
                keyboard.add_button(tower_lvl_up, color=VkKeyboardColor.POSITIVE, payload={"command": "строить башня"})
            if player.build.wall_lvl < 30:
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
        if player.lvl >= 3:
            keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('Шахта', color=VkKeyboardColor.PRIMARY, payload={"command": "mine"})
        keyboard.add_line()
        keyboard.add_button('🔨 Строить', color=VkKeyboardColor.DEFAULT, payload={"command": "build_cave"})
        if player.build.forge:
            keyboard.add_button('⚒ Кузница', color=VkKeyboardColor.DEFAULT, payload={"command": "кузница"})
        if player.lvl >= 5 or player.build.tavern:
            keyboard.add_line()
            keyboard.add_button('🕸 Пещеры', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры войти"})
            if player.build.tavern:
                keyboard.add_button('🍺 Таверна', color=VkKeyboardColor.DEFAULT, payload={"command": "таверна"})
            if player.lvl >= 5:
                keyboard.add_button('💀 Алтарь 💀', color=VkKeyboardColor.DEFAULT, payload={"command": "алтарь"})
        keyboard.add_line()
        keyboard.add_button('🤴 Лорд', color=VkKeyboardColor.DEFAULT, payload={"command": "профиль"})
        if player.lvl >= 5:
            keyboard.add_button('❓ Команды', color=VkKeyboardColor.DEFAULT, payload={"command": "команды"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})

    # Подземелье - Строительство

    elif player.place == 'cave_build':
        stock_lvl_up = '🔨 🏤 Склад ' + str(player.build.stock.lvl + 1) + ' ур.'
        market_lvl_up = '🔨 ✨ Рынок ' + str(player.build.market_lvl + 1) + ' ур.'
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_button('💬 Инфо', color=VkKeyboardColor.DEFAULT, payload={"command": "build_cave"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})
        if player.build.stock.lvl < 80 or not player.build.citadel:
            keyboard.add_line()
        if player.build.stock.lvl < 80:
            keyboard.add_button(stock_lvl_up, color=VkKeyboardColor.POSITIVE, payload={"command": "строить склад"})
        if not player.build.citadel:
            keyboard.add_button('🔨 🏰 Цитадель', color=VkKeyboardColor.POSITIVE, payload={"command": "строить цитадель"})
        if not player.build.forge or not player.build.tavern:
            keyboard.add_line()
        if not player.build.forge:
            keyboard.add_button('🔨 ⚒ Кузница', color=VkKeyboardColor.POSITIVE, payload={"command": "строить кузница"})
        if not player.build.tavern:
            keyboard.add_button('🔨 🍺 Таверна', color=VkKeyboardColor.POSITIVE, payload={"command": "строить таверна"})
        if player.build.market_lvl < 20:
            keyboard.add_line()
            keyboard.add_button(market_lvl_up, color=VkKeyboardColor.POSITIVE, payload={"command": "строить рынок"})

    # Шахта

    elif player.place == 'mine':
        stone = in_items(player.inventory.items.all(), 'stone_pickaxe')
        iron = in_items(player.inventory.items.all(), 'iron_pickaxe')
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
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
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_line()
        keyboard.add_button('⚒ ⛏ Кирки', color=VkKeyboardColor.DEFAULT, payload={"command": "кирки"})

    # Кузница - крафт кирок

    elif player.place == 'forge_pickaxe':
        items = player.inventory.items.all()
        stone = in_items(items, 'stone_pickaxe')
        iron = in_items(items, 'iron_pickaxe')
        diamond = in_items(items, 'diamond_pickaxe')
        skull = in_items(items, 'skull_pickaxe')
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
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
        if not diamond or not skull:
            keyboard.add_line()
            if not diamond:
                keyboard.add_button('⛏ 💎 Кристальная', color=VkKeyboardColor.POSITIVE,
                                    payload={"command": "ковать кристальная кирка"})
            if not skull:
                keyboard.add_button('⛏ 💀 Костяная', color=VkKeyboardColor.POSITIVE,
                                    payload={"command": "ковать костяная кирка"})

    # Таверна

    elif player.place == 'tavern':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_line()
        keyboard.add_button('🎲 Кости 🎲', color=VkKeyboardColor.POSITIVE, payload={"command": "кости"})
        # keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "stock"})
        # keyboard.add_button('⚔ Арсенал', color=VkKeyboardColor.DEFAULT, payload={"command": "forge_kit_info"})

    # Война

    elif player.place == 'war':
        keyboard.add_button('⬅ Назад', color=VkKeyboardColor.DEFAULT, payload={"command": "цитадель"})
        keyboard.add_button('💬 Инфо', color=VkKeyboardColor.DEFAULT, payload={"command": "война"})
        if player.lvl >= 10:
            find_time = action_time - player.war.find_last_time
            if find_time >= FIND_TIME:
                color = VkKeyboardColor.POSITIVE
            else:
                color = VkKeyboardColor.NEGATIVE
            keyboard.add_line()
            keyboard.add_button('🔎 Поиск', color=color, payload={"command": "поиск"})
            war_time = action_time - player.war.war_last_time
            attack_color = VkKeyboardColor.NEGATIVE
            if war_time >= WAR_TIME:
                if player.war.enemy_id:
                    attack_color = VkKeyboardColor.POSITIVE
            keyboard.add_button('⚔ Напасть', color=attack_color, payload={"command": "атака"})
            if player.war.enemy_id:
                keyboard.add_line()
                keyboard.add_button('🔎 Разведка (10 💎)', color=VkKeyboardColor.POSITIVE, payload={"command": "разведка"})
            keyboard.add_line()
            keyboard.add_button('🛡 Щит ⏳', color=VkKeyboardColor.DEFAULT, payload={"command": "щит"})
            keyboard.add_button('⚔👥 Армия', color=VkKeyboardColor.DEFAULT, payload={"command": "армия"})

    # Рынок

    elif player.place == 'market':
        keyboard.add_button('Земли', color=VkKeyboardColor.PRIMARY, payload={"command": "land"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})
        keyboard.add_line()
        keyboard.add_button('◾ Камень ◾', color=VkKeyboardColor.POSITIVE, payload={"command": "рынок камень"})
        keyboard.add_button('🌲 Дерево 🌲', color=VkKeyboardColor.POSITIVE, payload={"command": "рынок дерево"})
        keyboard.add_line()
        keyboard.add_button('◽ Железо ◽', color=VkKeyboardColor.POSITIVE, payload={"command": "рынок железо"})
        keyboard.add_button('💎 Кристаллы 💎', color=VkKeyboardColor.POSITIVE, payload={"command": "рынок кристаллы"})
        keyboard.add_line()
        keyboard.add_button('💀 Черепа 💀', color=VkKeyboardColor.POSITIVE, payload={"command": "рынок череп"})
        keyboard.add_line()
        keyboard.add_button('✨ Мои лоты ✨', color=VkKeyboardColor.DEFAULT, payload={"command": "мои лоты"})

    # Пещеры

    elif player.place == 'cave_go':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_button('💬 Инфо 💬', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры инфо"})
        keyboard.add_line()
        keyboard.add_button('⬆ На Север ⬆', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры север"})
        keyboard.add_line()
        keyboard.add_button('⬅ На Запад', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры запад"})
        keyboard.add_button('На Восток ➡', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры восток"})
        keyboard.add_line()
        keyboard.add_button('⬇ На Юг ⬇', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры юг"})
    elif player.place == 'cave_up':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_button('💬 Инфо 💬', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры инфо"})
        keyboard.add_line()
        keyboard.add_button('⬆ На Север ⬆', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры север"})
        keyboard.add_line()
        keyboard.add_button('⬅ На Запад', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры запад"})
        keyboard.add_button('На Восток ➡', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры восток"})
        keyboard.add_line()
        keyboard.add_button('⬇ На Юг ⬇', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры юг"})
        keyboard.add_line()
        keyboard.add_button('⏫ Вверх ⏫', color=VkKeyboardColor.POSITIVE, payload={"command": "пещеры вверх"})
    elif player.place == 'cave_down':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_button('💬 Инфо 💬', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры инфо"})
        keyboard.add_line()
        keyboard.add_button('⬆ На Север ⬆', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры север"})
        keyboard.add_line()
        keyboard.add_button('⬅ На Запад', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры запад"})
        keyboard.add_button('На Восток ➡', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры восток"})
        keyboard.add_line()
        keyboard.add_button('⬇ На Юг ⬇', color=VkKeyboardColor.DEFAULT, payload={"command": "пещеры юг"})
        keyboard.add_line()
        keyboard.add_button('⏬ Вниз ⏬', color=VkKeyboardColor.POSITIVE, payload={"command": "пещеры вниз"})

    # Алтарь

    elif player.place == 'altar':
        keyboard.add_button('Подземелье', color=VkKeyboardColor.PRIMARY, payload={"command": "cave"})
        keyboard.add_line()
        keyboard.add_button('🤴 Ник - 5 💀', color=VkKeyboardColor.POSITIVE, payload={"command": "алтарь ник"})
        keyboard.add_button('🛡 Щит - 20 💀', color=VkKeyboardColor.POSITIVE, payload={"command": "алтарь щит"})
        keyboard.add_line()
        keyboard.add_button('⚔ Атака - 5 💀', color=VkKeyboardColor.POSITIVE, payload={"command": "алтарь атака"})
        keyboard.add_button('🎯 Разведка - 5 💀', color=VkKeyboardColor.POSITIVE, payload={"command": "алтарь разведка"})
        keyboard.add_line()
        keyboard.add_button('💬 Инфо 💬', color=VkKeyboardColor.DEFAULT, payload={"command": "алтарь"})
        keyboard.add_button('🏤 Склад', color=VkKeyboardColor.DEFAULT, payload={"command": "склад"})

    return keyboard.get_keyboard()
