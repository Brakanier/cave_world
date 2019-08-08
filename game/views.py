from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import threading
import re
import json
import logging
from decouple import config
from datetime import datetime

from .models.build import Build, Stock
from .models.player import Player
from .models.war import War
from .models.inventory import Inventory
from .models.market import Product
from .models.cave import CaveMap, CaveProgress
from .models.promocode import PromoCode

from .fortune.fortune import Fortune
from .caves.caves import CaveGenerator, CaveManager

from .actions.functions import *
from .actions.chests import *
from .actions.altar import *
from system.models import Registration, Chat, Report

from .actions.statistic import *

secret_token = config('SECRET_TOKEN')
confirmation_token = '1f0c6305'


@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        if data['secret'] == secret_token:
            if data['type'] == 'confirmation':
                return HttpResponse(confirmation_token, content_type="text/plain", status=200)
            if data['type'] == 'wall_reply_new':
                comments_action(data['object'])
                return HttpResponse('ok', content_type="text/plain", status=200)
            elif data['type'] == 'message_new':
                from_id = data['object']['from_id']
                peer_id = data['object']['peer_id']
                if from_id < 0:
                    return HttpResponse('ok', content_type="text/plain", status=200)
                elif from_id == peer_id:
                    chat_info = {
                        'user_id': from_id,
                        'peer_id': from_id,
                        'chat_id': from_id
                    }
                    new_enter(chat_info, data)
                else:
                    chat_info = {
                        'user_id': from_id,
                        'peer_id': peer_id,
                        'chat_id': peer_id - 2000000000,
                        'nick': 'Новый игрок',
                    }
                    new_enter(chat_info, data)

                return HttpResponse('ok', content_type="text/plain", status=200)
            return HttpResponse('Ошибка - неверный type')
        else:
            return HttpResponse('Ошибка - неверный secret key')
    else:
        return HttpResponse('Сайт находится в разработке!')


def new_enter(chat_info, data):
    # Вход
    # Если игрок есть то сразу выполняет команды
    # Если игрока нет, то определяет надо ли регистрировать
    # Или это ввели ник
    try:
        player = Player.objects.get(user_id=chat_info['user_id'])

        action_time = data['object']['date']
        if 'payload' in data['object']:
            payload = json.loads(data['object']['payload'])
            if 'command' in payload:
                action(payload['command'], player, action_time, chat_info)
        else:
            text = data['object']['text']
            if text:
                action(text, player, action_time, chat_info)

    except Player.DoesNotExist:
        text = data['object']['text']

        if Registration.objects.filter(user_id=chat_info['user_id']).exists():

            create_models(chat_info, text)

        elif start_in(chat_info, text):
            Registration.objects.create(user_id=chat_info['user_id'])
            mess = 'Добро пожаловать в Cave World!\n' \
                   'Введите игровой ник:'
            send(chat_info, mess)


def start_in(chat_info, text):
    # Определяет начинать регистрацию или нет
    start_reg = True

    if chat_info['user_id'] != chat_info['peer_id']:

        start = ['start', 'старт', 'начать', 'рег', 'регистрация']

        if text.lower() in start:
            start_reg = True
        else:
            start_reg = False

    return start_reg


def create_models(chat_info, nick):
    # Создает все модели для игрока и саму модель игрока.
    try:

        war = War.objects.create(user_id=chat_info['user_id'])
        stock = Stock.objects.create(user_id=chat_info['user_id'])
        build = Build.objects.create(user_id=chat_info['user_id'], stock=stock)
        inventory = Inventory.objects.create(user_id=chat_info['user_id'])

    except:

        war = War.objects.get(user_id=chat_info['user_id'])
        build = Build.objects.get(user_id=chat_info['user_id'])
        inventory = Inventory.objects.get(user_id=chat_info['user_id'])

    try:

        vk = vk_connect()
        user = vk.users.get(user_ids=str(chat_info['user_id']))
        user = user[0]
        if user['first_name']:
            first_name = user['first_name']
        else:
            first_name = ''
        if user['last_name']:
            last_name = user['last_name']
        else:
            last_name = ''

        player = Player.objects.create(user_id=chat_info['user_id'],
                                       place='cave',
                                       nickname=nick,
                                       first_name=first_name,
                                       last_name=last_name,
                                       build=build,
                                       war=war,
                                       inventory=inventory,
                                       chat_id=chat_info['peer_id'],
                                       )

        mess = 'Ваш ник - ' + player.nickname + '\n'
        mess += 'Напиши "команды", чтобы узнать доступные команды.' + '\n' + \
                'Команды и кнопки открываются с уровнем и постройкой зданий!' + '\n'

        send(chat_info, mess, get_keyboard(player))

    except:

        chat_info['nick'] = "Новый игрок"
        mess = "Ник занят или слишком длинный!"
        send(chat_info, mess)


def add_update_chat(chat_info):

    count = 0
    try:
        count = count_users_chat(chat_info)
    except vk_api.ApiError as e:
        pass
        #print(e)

    if count == 0:
        is_admin = False
    else:
        is_admin = True

    try:
        Chat.objects.create(peer_id=chat_info['peer_id'], count_users=count, is_admin=is_admin)
    except:
        Chat.objects.filter(peer_id=chat_info['peer_id']).update(count_users=count, is_admin=is_admin)


def action(command, player, action_time, chat_info):
    answer = None
    chat_info['nick'] = player.nickname
    stat = {
        'category': '',
        'action': '',
        'label': '',
        'value': 1,
    }

    if command.lower() == 'ник' or command.lower() == 'ник время':
        answer = player.check_change_nickname_time(action_time)
    elif re.match(r'ник ', command.lower()):
        part = command.split()
        if len(part) >= 2:
            nick = command[4:]
            answer = player.change_nickname(nick, action_time)
        else:
            answer = "Вы не указали ник!\nНик [новый ник]"

    command = command.lower()

    # Меню

    if re.match(r'донат', command):
        answer = 'Вы можете поддержать проект по ссылке:\n' + \
                 'https://vk.com/app6471849_-176853872\n\n' + \
                 'За поддержку проекта вы попадете в виджет на странице группы и получите черепа:\n 1 рубль = 1 💀'

    elif command == 'команды':
        answer = commands(player)
        stat['category'] = 'Menu'
        stat['action'] = 'Help'
        stat['label'] = 'Помощь'
    elif command == 'помощь':
        answer = "Описание всех команд:\n" + "https://vk.com/@cave_world_bot-cave-world-opisanie-komand"
    elif command == 'бонус':
        answer = player.bonus(action_time)
        stat['category'] = 'Menu'
        stat['action'] = 'Bonus'
        stat['label'] = 'Бонус'
    elif command == 'профиль' or command == 'лорд':
        answer = player.profile(action_time)
        stat['category'] = 'Menu'
        stat['action'] = 'Profile'
        stat['label'] = 'Профиль'
    elif command == 'inventory':
        answer = player.go_inventory()
        stat['category'] = 'Menu'
        stat['action'] = 'Inventory'
        stat['label'] = 'Инвентарь'
    elif command == 'сундуки':
        answer = player.go_chests()
        stat['category'] = 'Menu'
        stat['action'] = 'Chests'
        stat['label'] = 'Сундуки'
    elif command == 'топ':
        answer = player.top()
        stat['category'] = 'Menu'
        stat['action'] = 'Top'
        stat['label'] = 'Топ'
    elif command == 'топ лвл' or command == 'топ уровень':
        answer = player.top_lvl()
        stat['category'] = 'Menu'
        stat['action'] = 'Top_Lvl'
        stat['label'] = 'Топ_Уровень'
    elif re.match(r'топ череп', command):
        answer = player.top_skull()
        stat['category'] = 'Menu'
        stat['action'] = 'Top_Skull'
        stat['label'] = 'Топ_Череп'
    elif re.match(r'топ атак', command):
        answer = player.top_attack()
    elif re.match(r'топ защит', command):
        answer = player.top_defend()
    elif re.match(r'топ золот', command):
        answer = player.top_gold()
    elif command in ('топ здания', 'топ строителей'):
        answer = player.top_build()
    elif re.match(r'топ пещер', command):
        answer = player.top_cave()
    elif command == 'склад' or command == 'ресурсы':
        answer = player.build.stock.stock(player.build, action_time)
        stat['category'] = 'Menu'
        stat['action'] = 'Stock'
        stat['label'] = 'Склад'
    elif command == 'build_cave':
        stat['category'] = 'Menu'
        stat['action'] = 'Build_Cave'
        stat['label'] = 'Строить_Подземелье'
        answer = player.cave_build()
    elif command == 'build_land':
        answer = player.land_build()
        stat['category'] = 'Menu'
        stat['action'] = 'Build_Land'
        stat['label'] = 'Строить_Земли'
    elif command == 'здания':
        stat['category'] = 'War'
        stat['action'] = 'Builds'
        stat['label'] = 'Военные_Здания'
        answer = player.build.build_info()
    elif command == 'строить' or command == 'построить':
        stat['category'] = 'Text'
        stat['action'] = 'Build'
        stat['label'] = 'Строить'
        answer = 'Здания Подземелья:\n'
        answer += player.cave_build()
        if player.build.citadel:
            answer += '\nЗдания Земель:\n'
            answer += player.land_build()

    # Таверна
    # TODO рефакторинг очень надо
    elif re.match(r'кости', command):
        if chat_info['peer_id'] != chat_info['user_id']:
            try:
                chat = Chat.objects.get(peer_id=chat_info['peer_id'])
                bones = chat.bones_on
            except Chat.DoesNotExist:
                bones = True
        else:
            bones = True
        if re.search(r'дерево', command) and bones:
            count = amount(command)
            if count > 0:
                answer = player.build.tavern_bones(action_time, 'wood', count)
            else:
                answer = "Вы пытаетесь сыграть на 0 ресурса!"
        elif re.search(r'камень', command) and bones:
            count = amount(command)
            if count > 0:
                answer = player.build.tavern_bones(action_time, 'stone', count)
            else:
                answer = "Вы пытаетесь сыграть на 0 ресурса!"
        elif re.search(r'железо', command) and bones:
            count = amount(command)
            if count > 0:
                answer = player.build.tavern_bones(action_time, 'iron', count)
            else:
                answer = "Вы пытаетесь сыграть на 0 ресурса!"
        elif re.search(r'кристаллы', command) and bones:
            count = amount(command)
            if count > 0:
                answer = player.build.tavern_bones(action_time, 'diamond', count)
            else:
                answer = "Вы пытаетесь сыграть на 0 ресурса!"
        elif re.search(r'золото', command) and bones:
            count = amount(command)
            if count > 1000:
                answer = "Максимальная ставка золотом 1000!"
            elif 0 < count <= 1000:
                answer = player.build.tavern_bones(action_time, 'gold', count)
            else:
                answer = "Вы пытаетесь сыграть на 0 ресурса!"
        elif not bones:
            answer = 'Кости запрещены администратором беседы.'
        else:
            answer = player.bones()

    # Строительство

    elif command == 'строить склад' or command == 'улучшить склад':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Stock'
        stat['label'] = 'Строить_Склад'
        answer = player.build.build_stock(action_time)
    elif re.match(r'строить кузниц', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Forge'
        stat['label'] = 'Строить_Кузница'
        answer = player.build.build_forge(action_time)
    elif re.match(r'строить таверн', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Tavern'
        stat['label'] = 'Строить_Таверна'
        answer = player.build.build_tavern(action_time)
    elif command == 'строить цитадель':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Citadel'
        stat['label'] = 'Строить_Цитадель'
        answer = player.build.build_citadel(action_time)
    elif re.match(r'строить казарм', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Barracks'
        stat['label'] = 'Строить_Казармы'
        answer = player.build.build_barracks(action_time)
    elif re.match(r'строить стрельбищ', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Archery'
        stat['label'] = 'Строить_Стрельбище'
        answer = player.build.build_archery(action_time)
    elif command == 'строить башня магов' or command == 'строить башню магов':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Magic'
        stat['label'] = 'Строить_Магия'
        answer = player.build.build_magic(action_time)
    elif re.match(r'строить башн', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Tower'
        stat['label'] = 'Строить_Башня'
        answer = player.build.build_tower(action_time)
    elif re.match(r'строить стен', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Wall'
        stat['label'] = 'Строить_Стена'
        answer = player.build.build_wall(action_time)
    elif re.match(r'строить лесопилк', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Woodmine'
        stat['label'] = 'Строить_Лесопилка'
        answer = player.build.build_wood_mine(action_time, player.lvl)
    elif re.match(r'строить каменоломн', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Stonemine'
        stat['label'] = 'Строить_Каменоломня'
        answer = player.build.build_stone_mine(action_time, player.lvl)
    elif re.match(r'строить рудник', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Ironmine'
        stat['label'] = 'Строить_Рудник'
        answer = player.build.build_iron_mine(action_time, player.lvl)
    elif re.match(r'строить прииск', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Diamondmine'
        stat['label'] = 'Строить_Прииск'
        answer = player.build.build_diamond_mine(action_time, player.lvl)

    # Добыча

    elif re.match(r'камень', command):
        stat['category'] = 'Get'
        stat['action'] = 'Get_Stone'
        stat['label'] = 'Добыть_Камень'
        stat['value'] = amount(command)
        count = amount(command)
        if count > 0:
            answer = player.get_stone(action_time, chat_info, count)
    elif re.match(r'дерево', command):
        stat['category'] = 'Get'
        stat['action'] = 'Get_Wood'
        stat['label'] = 'Добыть_Дерево'
        stat['value'] = amount(command)
        answer = player.get_wood(action_time, chat_info, amount(command))
    elif re.match(r'железо', command):
        stat['category'] = 'Get'
        stat['action'] = 'Get_Iron'
        stat['label'] = 'Добыть_Железо'
        stat['value'] = amount(command)
        count = amount(command)
        if count > 0:
            answer = player.get_iron(action_time, chat_info, count)
    elif re.match(r'кристал', command):
        stat['category'] = 'Get'
        stat['action'] = 'Get_Diamond'
        stat['label'] = 'Добыть_Кристалы'
        stat['value'] = amount(command)
        count = amount(command)
        if count > 0:
            answer = player.get_diamond(action_time, chat_info, count)

    # Крафт
    elif command == 'ковать':
        if player.build.forge:
            answer = "Укажите предмет для ковки!\nКирки - посмотреть доступные кирки для ковки."
        else:
            answer = "Сначала постройте Кузницу!"
    elif 'ковать каменн' in command:
        stat['category'] = 'Craft'
        stat['action'] = 'Craft_Stone_Pickaxe'
        stat['label'] = 'Ковать_Каменная_Кирка'
        answer = player.craft_stone_pickaxe(action_time)
    elif 'ковать железн' in command:
        stat['category'] = 'Craft'
        stat['action'] = 'Craft_Iron_Pickaxe'
        stat['label'] = 'Ковать_Железная_Кирка'
        answer = player.craft_iron_pickaxe(action_time)
    elif 'ковать кристальн' in command:
        stat['category'] = 'Craft'
        stat['action'] = 'Craft_Diamond_Pickaxe'
        stat['label'] = 'Ковать_Кристальная_Кирка'
        answer = player.craft_diamond_pickaxe(action_time)
    elif 'ковать костян' in command:
        stat['category'] = 'Craft'
        stat['action'] = 'Craft_Skull_Pickaxe'
        stat['label'] = 'Ковать_Костяная_Кирка'
        answer = player.craft_skull_pickaxe(action_time)

    # Локацииц

    elif command == 'cave':
        stat['category'] = 'Place'
        stat['action'] = 'Cave'
        stat['label'] = 'Подземелье'
        answer = player.cave()
    elif command == 'mine' or command == 'шахта':
        stat['category'] = 'Place'
        stat['action'] = 'Mine'
        stat['label'] = 'Шахта'
        answer = player.mine()
    elif command == 'кузница':
        stat['category'] = 'Place'
        stat['action'] = 'Forge'
        stat['label'] = 'Кузница'
        answer = player.forge()
    elif command == 'кирки':
        stat['category'] = 'Place'
        stat['action'] = 'Pickaxes'
        stat['label'] = 'Кирки'
        answer = player.forge_pickaxe()
    elif command == 'таверна':
        stat['category'] = 'Place'
        stat['action'] = 'Tavern'
        stat['label'] = 'Таверна'
        answer = player.tavern()
    elif command == 'land':
        stat['category'] = 'Place'
        stat['action'] = 'Land'
        stat['label'] = 'Земли'
        answer = player.land()
    elif command == 'цитадель':
        stat['category'] = 'Place'
        stat['action'] = 'Citadel'
        stat['label'] = 'Цитадель'
        answer = player.citadel(action_time)
    elif command == 'война':
        stat['category'] = 'Place'
        stat['action'] = 'War'
        stat['label'] = 'Война'
        answer = player.war_menu()
    elif command in ('найм', 'нанять'):
        stat['category'] = 'Place'
        stat['action'] = 'Buy'
        stat['label'] = 'Найм'
        answer = player.buy(action_time)

    # Армия

    elif re.match(r'воин', command):
        stat['category'] = 'Army'
        stat['action'] = 'Warrior'
        stat['label'] = 'Воин'
        stat['value'] = amount(command)
        answer = player.war.craft_warrior(player.build, action_time, amount(command))
    elif re.match(r'лучник', command):
        stat['category'] = 'Army'
        stat['action'] = 'Archer'
        stat['label'] = 'Лучник'
        stat['value'] = amount(command)
        answer = player.war.craft_archer(player.build, action_time, amount(command))
    elif re.match(r'маг', command):
        stat['category'] = 'Army'
        stat['action'] = 'Archer'
        stat['label'] = 'Лучник'
        stat['value'] = amount(command)
        answer = player.war.craft_wizard(player.build, action_time, amount(command))

    elif command == 'нанять макс':
        answer = player.war.craft_equally(action_time)

    # Охота

    elif command == 'охота':
        answer = player.hunt(action_time)
    elif re.match(r'охота воин', command):
        answer = player.hunting_war(action_time)
    elif re.match(r'охота лучник', command):
        answer = player.hunting_arch(action_time)
    elif re.match(r'охота маг', command):
        answer = player.hunting_wiz(action_time)

    # Война

    elif command == 'щит':
        stat['category'] = 'War'
        stat['action'] = 'Shield'
        stat['label'] = 'Щит'
        answer = player.war.shield_info(action_time)
    elif command == ('поиск' or 'искать'):
        stat['category'] = 'War'
        stat['action'] = 'Find'
        stat['label'] = 'Поиск'
        answer = player.war.find_enemy(player.lvl, action_time)
    elif command == 'разведка':
        answer = player.war.scouting(action_time)
    elif command == 'атака':
        stat['category'] = 'War'
        stat['action'] = 'Attack'
        stat['label'] = 'Атака'
        answer = player.war.attack(player, action_time, chat_info)
    elif command == 'армия':
        stat['category'] = 'War'
        stat['action'] = 'Army'
        stat['label'] = 'Армия'
        answer = player.war.army()

    elif re.match(r'открыть', command):
        stat['category'] = 'Chests'
        stat['action'] = 'Open'
        stat['label'] = 'Открыть'
        chest = get_chest_object(command)
        if chest:
            answer = open_trophy_chest(player, chest)
        else:
            answer = 'Такого сундука не существует!'

    elif re.match(r'репорт', command):
        stat['category'] = 'System'
        stat['action'] = 'Report'
        stat['label'] = 'Репорт'
        answer = Report.report(Report, player, command, chat_info)

    elif re.match(r'ответ', command) and player.user_id == 55811116:
        stat['category'] = 'System'
        stat['action'] = 'Answer_Report'
        stat['label'] = 'Ответ_Репорт'
        answer = Report.answer_report(Report, command)

    # Рынок

    # Отправка ресурсов

    elif command == "строить рынок"\
            or command == "строить торговый пост"\
            or command == "улучшить рынок"\
            or command == "улучшить торговый пост":
        answer = player.build.build_market(action_time)

    elif re.match(r'отправить', command):
        answer = player._send_res(command, action_time)

    # Торговля

    elif command == "рынок" or command == "купить" or command == "продать" or command == "торговый пост":
        answer = Product.info(player)
    elif command == "рынок дерево":
        answer = Product.market_res(player, 'wood')
    elif command == "рынок камень":
        answer = Product.market_res(player, 'stone')
    elif command == "рынок железо":
        answer = Product.market_res(player, 'iron')
    elif re.match(r'рынок кристал', command):
        answer = Product.market_res(player, 'diamond')
    elif re.match(r'рынок череп', command):
        answer = Product.market_res(player, 'skull')
    elif command == "мои лоты":
        answer = Product.my_lots(player)
    elif command == 'снять все':
        answer = Product.del_all_lots(player)
    elif re.match(r'снять', command):
        id = Product.get_id(command)
        if id:
            answer = Product.del_lot(player, id)
        else:
            answer = "Неверный ID лота!"
    elif re.match(r'продать дерево', command):
        count, price = Product.get_param(command)
        if count and price:
            answer = Product.sell(player, 'wood', count, price)
        else:
            answer = "Укажите цену лота!"
    elif re.match(r'продать камен', command):
        count, price = Product.get_param(command)
        if count and price:
            answer = Product.sell(player, 'stone', count, price)
        else:
            answer = "Укажите цену лота!"
    elif re.match(r'продать железо', command):
        count, price = Product.get_param(command)
        if count and price:
            answer = Product.sell(player, 'iron', count, price)
        else:
            answer = "Укажите цену лота!"
    elif re.match(r'продать кристал', command):
        count, price = Product.get_param(command)
        if count and price:
            answer = Product.sell(player, 'diamond', count, price)
        else:
            answer = "Укажите цену лота!"
    elif re.match(r'продать череп', command):
        count, price = Product.get_param(command)
        if count and price:
            answer = Product.sell(player, 'skull', count, price)
        else:
            answer = "Укажите цену лота!"
    elif re.match(r'купить', command):
        id = Product.get_id(command)
        if id:
            answer = Product.buy(player, id)
        else:
            answer = "Неверный ID лота!"

    # Админ
    elif command == 'online' and player.user_id == 55811116:
        day = 86400
        this_day = action_time - day
        this_week = action_time - day * 7
        this_month = action_time - day * 30
        count_day = Player.objects.filter(last_energy_action__gte=this_day).count()
        count_week = Player.objects.filter(last_energy_action__gte=this_week).count()
        count_month = Player.objects.filter(last_energy_action__gte=this_month).count()
        count_all = Player.objects.count()
        answer = '🌐 Онлайн 🌐\n'+  \
        'День: ' + str(count_day) + '\n' + \
        'Неделя: ' + str(count_week) + '\n' + \
        'Месяц: ' + str(count_month) + '\n' + \
        'Всего в базе: ' + str(count_all)
    elif command == 'all gold' and player.user_id == 55811116:
        stocks = Stock.objects.all()
        gold = 0
        for stock in stocks:
            gold += stock.gold
        answer = 'Всего золота: ' + str(gold) + icon('gold')
    elif command == 'all skull' and player.user_id == 55811116:
        stocks = Stock.objects.all()
        skull = 0
        for stock in stocks:
            skull += stock.skull
        answer = 'Всего черепов: ' + str(skull) + icon('skull')
    elif re.match(r'give', command) and player.user_id == 55811116:
        if re.match(r'give skull', command):
            answer = Player.give_skull(command)
        else:
            answer = Player.give_chests(command)
    elif command == 'gencave' and player.user_id == 55811116:
        try:
            CaveMap.objects.get().delete()
        except:
            pass
        cave = CaveMap.objects.create()
        cave.cave_map = cave.generate()
        cave.save()
    elif command == 'price' and player.user_id == 55811116:
        wood_avr = Product.get_average_price('wood')
        stone_avr = Product.get_average_price('stone')
        iron_avr = Product.get_average_price('iron')
        diamond_avr = Product.get_average_price('diamond')
        skull_avr = Product.get_average_price('skull')
        answer = 'Цены:\n' + \
                 'Дерево: ' + str(wood_avr) + '\n' \
                 'Камень: ' + str(stone_avr) + '\n' \
                 'Железо: ' + str(iron_avr) + '\n' \
                 'Кристаллы: ' + str(diamond_avr) + '\n' \
                 'Черепа: ' + str(skull_avr) + '\n'

    elif re.match(r'del_lot', command) and player.user_id == 55811116:
        id = Product.get_id(command)
        answer = Product.admin_del_lot(id)

    elif command == 'код двамесяца':
        try:
            code = PromoCode.objects.get(user_id=player.user_id, code='двамесяца')
            answer = 'Вы уже использовали этот код!'
        except PromoCode.DoesNotExist:
            code = PromoCode.objects.create(user_id=player.user_id, code='двамесяца')
            code.save()
            chest = get_chest('present_chest')
            add_chest(player, chest, 5)
            answer = 'Код активирован!\n' + \
                     'Получено 5 подарочных сундуков!\n'

    # Алтарь

    elif command == 'алтарь':
        answer = altar_info(player)
    elif re.match(r'алтарь', command):
        answer = altar(command, player, action_time, chat_info)

    # Эль

    elif command == 'всем эль!!!':
        if chat_info['peer_id'] != chat_info['user_id']:
            try:
                chat = Chat.objects.get(peer_id=chat_info['peer_id'])
                alco = chat.alco_on
            except Chat.DoesNotExist:
                alco = True
        else:
            alco = True
        if alco:
            answer = player.alcohol(chat_info, action_time)
        else:
            answer = 'Эль запрещен администратором беседы.'

    # Настройки бесед

    elif chat_info['peer_id'] != chat_info['user_id'] and command == '!команды' and is_admin(player.user_id, chat_info):
        answer = 'Управление беседой:\n' + \
                 '!кости - вкл/выкл кости\n' + \
                 '!эль - вкл/выкл эль\n' + \
                 '!рассылка - вкл/выкл рассылку в беседе\n'

    elif chat_info['peer_id'] != chat_info['user_id'] and command == '!кости' and is_admin(player.user_id, chat_info):
        try:
            chat = Chat.objects.get(peer_id=chat_info['peer_id'])
            answer = chat.bones_change()
        except Chat.DoesNotExist:
            answer = 'Вашей беседы нет в базе. Свяжитесь с админом через команду "репорт".'

    elif chat_info['peer_id'] != chat_info['user_id'] and command == '!эль' and is_admin(player.user_id, chat_info):
        try:
            chat = Chat.objects.get(peer_id=chat_info['peer_id'])
            answer = chat.alco_change()
        except Chat.DoesNotExist:
            answer = 'Вашей беседы нет в базе. Свяжитесь с админом через команду "репорт".'

    elif chat_info['peer_id'] != chat_info['user_id'] and command == '!рассылка' and is_admin(player.user_id, chat_info):
        try:
            chat = Chat.objects.get(peer_id=chat_info['peer_id'])
            answer = chat.distribution_change()
        except Chat.DoesNotExist:
            answer = 'Вашей беседы нет в базе. Свяжитесь с админом через команду "репорт".'

    # Беседы

    elif command == 'беседы':
        answer = chat_list()

    elif command == 'тест':
        answer = Product.del_all_lots(player)
    # Пещеры

    elif re.match(r'пещеры', command) or re.match(r'п', command):
        move_commands = (
            'пещеры', 
            'пещеры север', 
            'пещеры запад', 
            'пещеры восток', 
            'пещеры юг', 
            'п с', 
            'п в', 
            'п з', 
            'п ю', 
            'пещеры с', 
            'пещеры з', 
            'пещеры в', 
            'пещеры ю'
            )
        if not player.cave_progress:
            cave = CaveMap.objects.get()
            cave_progress = CaveProgress.objects.create(user_id=player.user_id, cave=cave)
            player.cave_progress = cave_progress
            player.save(update_fields=['cave_progress'])
        if command == 'пещеры':
            answer = '🕸 Пещеры 🕸 - представляют собой лабиринт.\n' + \
            'На каждом из уровней вы можете найти хорошее, плохое или проход на уровень дальше.\n' + \
            'Карта пещер для всех общая.\n' + \
            'Когда игрок добирается до сокровищ, происходит обвал, пещеры генерируются заново!\n\n' + \
            'Команды:\n' + \
            '- Пещеры войти - начать исследование пещер\n' + \
            '- Пещеры север - выбор пути\n' + \
            '- Пещеры восток - выбор пути\n' + \
            '- Пещеры запад - выбор пути\n' + \
            '- Пещеры юг - выбор пути\n' + \
            '- Пещеры вверх - вернуться на прошлый уровень\n' + \
            '- Пещеры вниз - спуститься на след. уровень\n'
        elif command == 'пещеры инфо':
            answer = player.cave_progress.info()
        elif command == 'пещеры войти':
            army = player.lvl * 3
            if player.war.sum_army() < army:
                answer = 'Для исследования пещер вам нужно минимум ' + str(army) + ' ⚔ армии!'
            else:
                cave_manager = CaveManager(player)
                answer = cave_manager.start(player, action_time)
        elif command in ('пещеры вниз', 'п вниз'):
            cave_manager = CaveManager(player)
            answer = cave_manager.go_down(player)
        elif command in ('пещеры вверх', 'п вверх'):
            cave_manager = CaveManager(player)
            answer = cave_manager.go_up(player)
        elif command in move_commands:
            cave_manager = CaveManager(player)
            answer = cave_manager.move(player, command)

    # Рассылка

    elif command == 'рассылка':
        if player.distribution:
            player.distribution = False
            player.save(update_fields=['distribution'])
            answer = '😢 Вы отключили рассылку! 😢\n' + \
                     'Чтобы первым узнавать об обновлениях и розыгрышах напишите "рассылка"'
        else:
            player.distribution = True
            player.save(update_fields=['distribution'])
            answer = '👍🏻 Вы включили рассылку! 👍🏻\nCпасибо, что вам интересен наш проект!'

    if hasattr(player, 'keyboard'):
        keyboard = player.keyboard
    else:
        keyboard = get_keyboard(player, action_time)

    alco_except = (
    'пещеры', 
    'пещеры войти', 
    'пещеры север', 
    'пещеры запад', 
    'пещеры восток', 
    'пещеры юг', 
    'п с', 
    'п в', 
    'п з', 
    'п ю', 
    'пещеры с', 
    'пещеры з', 
    'пещеры в', 
    'пещеры ю', 
    'пещеры вниз', 
    'пещеры вверх', 
    'п вниз', 
    'п вверх',
    'всем эль!!!',
    'беседы',
    'донат'
    )
    if command not in alco_except:
        if answer and player.user_id != 55811116:
            if chat_info['peer_id'] != chat_info['user_id']:
                answer = player.alcohol_mess(action_time, answer)

    threading.Thread(target=send, args=(chat_info, answer, keyboard)).start()

    # Обновление инфы из бесед, если была команда для бота
    if answer and chat_info['user_id'] != chat_info['peer_id']:
        Player.objects.filter(user_id=chat_info['user_id']).update(chat_id=chat_info['peer_id'])
        add_update_chat(chat_info)

    if answer:
        # Отправка статистики
        threading.Thread(target=track, args=(player.user_id, stat)).start()

def comments_action(comment):
    if comment['from_id'] == -176853872:
        return True

    try:
        player = Player.objects.get(user_id=comment['from_id'])
    except Player.DoesNotExist:
        player = False

    if player:
        if comment['text'].lower() in ('#играю', '#играть', '#крутить', '#крути', '#фортуна', '#удача', '#азино', '#поднятьбабла'):
            fortune = Fortune(player, comment)
            fortune.fortune()
    else:
        answer = 'Я вижу ты новенький!\nНачни играть и стань сильнейшим Лордом!\nvk.me/cave_world_bot'
        send_comment(comment['post_id'], comment['id'], answer)

    return True

