from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import re
import json
import logging
from decouple import config
from datetime import datetime

from .models.build import Build, Stock
from .models.player import Player
from .models.war import War
from .models.inventory import Inventory
from .actions.functions import *
from .actions.chests import *
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
            if data['type'] == 'message_new':
                from_id = data['object']['from_id']
                peer_id = data['object']['peer_id']
                if from_id == peer_id:
                    chat_info = {
                        'user_id': from_id,
                        'peer_id': from_id,
                        'chat_id': from_id
                    }
                    enter(chat_info, data)
                else:
                    chat_info = {
                        'user_id': from_id,
                        'peer_id': peer_id,
                        'chat_id': peer_id - 2000000000,
                        'nick': 'Новый игрок',
                    }
                    enter(chat_info, data)
                    Player.objects.filter(user_id=chat_info['user_id']).update(chat_id=chat_info['peer_id'])
                    if Chat.objects.filter(peer_id=chat_info['peer_id']).exists():
                        try:
                            count = count_users_chat(chat_info)
                            Chat.objects.filter(peer_id=chat_info['peer_id']).update(count_users=count)
                        except vk_api.ApiError:
                            print('У бота нет прав админа')
                    else:
                        try:
                            count = count_users_chat(chat_info)
                            Chat.objects.create(peer_id=chat_info['peer_id'], count_users=count)
                        except vk_api.ApiError:
                            print('У бота нет прав админа')
                return HttpResponse('ok', content_type="text/plain", status=200)
            return HttpResponse('Ошибка - неверный type')
        else:
            return HttpResponse('Ошибка - неверный secret key')
    else:
        return HttpResponse('Сайт находится в разработке!')


def register(chat_info, nick):
    print('регистрация')
    if not Player.objects.filter(user_id=chat_info['user_id']).exists() and not Player.objects.filter(nickname=nick).exists():
        print('cоздание пользователя')
        war = War.objects.create(user_id=chat_info['user_id'])
        stock = Stock.objects.create(user_id=chat_info['user_id'])
        build = Build.objects.create(user_id=chat_info['user_id'], stock=stock)
        inventory = Inventory.objects.create(user_id=chat_info['user_id'])
        player = Player.objects.create(user_id=chat_info['user_id'],
                                       nickname=nick,
                                       build=build,
                                       war=war,
                                       inventory=inventory,
                                       chat_id=chat_info['peer_id'],
                                       )
        vk = vk_connect()
        user = vk.users.get(user_ids=str(chat_info['user_id']))
        user = user[0]
        if user['first_name']:
            player.first_name = user['first_name']
        if user['last_name']:
            player.last_name = user['last_name']
        return player
    elif Player.objects.filter(user_id=chat_info['user_id']).exists():
        print('пользователь существует')
        player = Player.objects.get(user_id=chat_info['user_id'])
        return player
    else:
        print('ник занят')
        message = 'Ник уже занят!\n' + \
                  'Введите ник:'
        send(chat_info, message)
        return None


def enter(chat_info, data):
    if not Registration.objects.filter(user_id=chat_info['user_id']).exists():
        message = 'Добро пожаловать в Cave World!\n' \
                  'Введите свой ник:'
        send(chat_info, message)
        reg = Registration.objects.create(user_id=chat_info['user_id'])
        reg.save()
        print('Новый пользователь - Регистрация начата')
    elif Registration.objects.filter(user_id=chat_info['user_id']).exists():
        r = Registration.objects.get(user_id=chat_info['user_id'])
        if not r.reg:
            print('ветка регистрации')
            nick = data['object']['text']
            player = register(chat_info, nick)
            if player:
                player.place = 'cave'
                player.save()
                Registration.objects.filter(user_id=chat_info['user_id']).update(reg=True)
                message = 'Ваш ник - ' + player.nickname
                print('Новый пользователь - ' + player.nickname)
                chat_info['nick'] = player.nickname
                send(chat_info, message, get_keyboard(player))
        else:
            print('ветка команд')
            player = Player.objects.get(user_id=chat_info['user_id'])
            action_time = data['object']['date']
            if 'payload' in data['object']:
                print('payload')
                payload = json.loads(data['object']['payload'])
                log(player, payload['command'], action_time)
                action(payload['command'], player, action_time, chat_info)
            else:
                text = data['object']['text']
                if text:
                    print('текст')
                    log(player, text, action_time)
                    action(text.lower(), player, action_time, chat_info)


def log(player, command, action_time):
    time = datetime.fromtimestamp(int(action_time + (3600 * 3)))
    info = time.strftime('%Y-%m-%d %H:%M:%S') + ' | ' + \
           str(player.user_id) + ' | ' + \
           command + ' | ' + \
           player.nickname + ' | ' + \
           player.last_name + ' ' + player.first_name
    print(info)


def action(command, player, action_time, chat_info):
    answer = 'пусто'
    chat_info['nick'] = player.nickname
    stat = {
        'category': '',
        'action': '',
        'label': '',
        'value': 1,
    }

    # Меню

    if command == '!команды' or command == 'команды' or command == 'помощь' or command == '!помощь':
        answer = commands()
        stat['category'] = 'Menu'
        stat['action'] = 'Help'
        stat['label'] = 'Помощь'
    elif command == 'бонус':
        answer = player.bonus(action_time)
        stat['category'] = 'Menu'
        stat['action'] = 'Bonus'
        stat['label'] = 'Бонус'
    elif command == 'профиль':
        answer = player.profile(action_time)
        stat['category'] = 'Menu'
        stat['action'] = 'Profile'
        stat['label'] = 'Профиль'
    elif command == 'инвентарь':
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
    elif command == 'топ лвл':
        answer = player.top_lvl()
        stat['category'] = 'Menu'
        stat['action'] = 'Top_Lvl'
        stat['label'] = 'Топ_Уровень'
    elif command == 'склад':
        answer = player.build.stock.stock(player.build, action_time)
        stat['category'] = 'Menu'
        stat['action'] = 'Stock'
        stat['label'] = 'Склад'
    elif command == 'строить подземелье':
        stat['category'] = 'Menu'
        stat['action'] = 'Build_Cave'
        stat['label'] = 'Строить_Подземелье'
        answer = player.cave_build()
    elif command == 'строить земли':
        answer = player.land_build()
        stat['category'] = 'Menu'
        stat['action'] = 'Build_Land'
        stat['label'] = 'Строить_Земли'

    # Таверна

    elif re.match(r'кости', command):
        if re.search(r'дерево', command):
            answer = player.build.tavern_bones(action_time, 'wood', amount(command))
            stat['action'] = 'Wood'
            stat['label'] = 'Кости_Дерево'
        elif re.search(r'камень', command):
            answer = player.build.tavern_bones(action_time, 'stone', amount(command))
            stat['action'] = 'Stone'
            stat['label'] = 'Кости_Камень'
        elif re.search(r'железо', command):
            answer = player.build.tavern_bones(action_time, 'iron', amount(command))
            stat['action'] = 'Iron'
            stat['label'] = 'Кости_Железо'
        elif re.search(r'кристаллы', command):
            answer = player.build.tavern_bones(action_time, 'diamond', amount(command))
            stat['action'] = 'Diamond'
            stat['label'] = 'Кости_Кристалы'
        elif re.search(r'золото', command):
            answer = player.build.tavern_bones(action_time, 'gold', amount(command))
            stat['action'] = 'Gold'
            stat['label'] = 'Кости_Золото'
        else:
            answer = player.bones()
        stat['category'] = 'Bones'

    # Строительство

    elif command == 'строить склад':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Stock'
        stat['label'] = 'Строить_Склад'
        answer = player.build.build_stock(action_time)
    elif command == 'строить кузница':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Forge'
        stat['label'] = 'Строить_Кузница'
        answer = player.build.build_forge(action_time)
    elif command == 'строить таверна':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Tavern'
        stat['label'] = 'Строить_Таверна'
        answer = player.build.build_tavern(action_time)
    elif command == 'строить цитадель':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Citadel'
        stat['label'] = 'Строить_Цитадель'
        answer = player.build.build_citadel(action_time)
    elif command == 'строить башня':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Tower'
        stat['label'] = 'Строить_Башня'
        answer = player.build.build_tower(action_time)
    elif command == 'строить стена':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Wall'
        stat['label'] = 'Строить_Стена'
        answer = player.build.build_wall(action_time)
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
    elif re.match(r'строить башня маг', command):
        stat['category'] = 'Build'
        stat['action'] = 'Build_Magic'
        stat['label'] = 'Строить_Магия'
        answer = player.build.build_magic(action_time)
    elif command == 'строить лесопилка':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Woodmine'
        stat['label'] = 'Строить_Лесопилка'
        answer = player.build.build_wood_mine(action_time, player.lvl)
    elif command == 'строить каменоломня':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Stonemine'
        stat['label'] = 'Строить_Каменоломня'
        answer = player.build.build_stone_mine(action_time, player.lvl)
    elif command == 'строить рудник':
        stat['category'] = 'Build'
        stat['action'] = 'Build_Ironmine'
        stat['label'] = 'Строить_Рудник'
        answer = player.build.build_iron_mine(action_time, player.lvl)
    elif command == 'строить прииск':
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
        answer = player.get_stone(action_time, chat_info, amount(command))
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
        answer = player.get_iron(action_time, chat_info, amount(command))
    elif re.match(r'кристаллы', command):
        stat['category'] = 'Get'
        stat['action'] = 'Get_Diamond'
        stat['label'] = 'Добыть_Кристалы'
        stat['value'] = amount(command)
        answer = player.get_diamond(action_time, chat_info, amount(command))

    # Крафт

    elif command == 'ковать каменная кирка':
        stat['category'] = 'Craft'
        stat['action'] = 'Craft_Stone_Pickaxe'
        stat['label'] = 'Ковать_Каменная_Кирка'
        answer = player.craft_stone_pickaxe(action_time)
    elif command == 'ковать железная кирка':
        stat['category'] = 'Craft'
        stat['action'] = 'Craft_Iron_Pickaxe'
        stat['label'] = 'Ковать_Железная_Кирка'
        answer = player.craft_iron_pickaxe(action_time)
    elif command == 'ковать кристальная кирка':
        stat['category'] = 'Craft'
        stat['action'] = 'Craft_Diamond_Pickaxe'
        stat['label'] = 'Ковать_Кристальная_Кирка'
        answer = player.craft_diamond_pickaxe(action_time)

    # Локацииц

    elif command == 'подземелье':
        stat['category'] = 'Place'
        stat['action'] = 'Cave'
        stat['label'] = 'Подземелье'
        answer = player.cave()
    elif command == 'шахта':
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
    elif command == 'земли':
        stat['category'] = 'Place'
        stat['action'] = 'Land'
        stat['label'] = 'Земли'
        answer = player.land()
    elif command == 'война':
        stat['category'] = 'Place'
        stat['action'] = 'War'
        stat['label'] = 'Война'
        answer = player.war_menu()
    elif command == 'нанять':
        stat['category'] = 'Place'
        stat['action'] = 'Buy'
        stat['label'] = 'Нанять'
        answer = player.buy()

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

    # Война

    elif command == 'здания':
        stat['category'] = 'War'
        stat['action'] = 'Builds'
        stat['label'] = 'Военные_Здания'
        answer = player.build.war_info()
    elif command == 'щит':
        stat['category'] = 'War'
        stat['action'] = 'Shield'
        stat['label'] = 'Щит'
        answer = player.war.shield_info(action_time)
    elif command == 'поиск':
        stat['category'] = 'War'
        stat['action'] = 'Find'
        stat['label'] = 'Поиск'
        answer = player.war.find_enemy(player.lvl, action_time)
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
        answer = Report.answer_report(Report, command, chat_info)

    '''
    elif re.match(r'дать', command):
        chest = get_chest_name(command)
        if chest:
            add_chest(player, chest)
        else:
            answer = 'Такого сундука не существует!'
    '''

    send(chat_info, answer, get_keyboard(player, action_time))
    track(player.user_id, stat)
