from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import re
import json
from decouple import config
from datetime import datetime

from .models.build import Build, Stock
from .models.player import Player
from .models.war import War
from .models.inventory import Inventory
from .actions.functions import *
from system.models import Registration

secret_token = config('SECRET_TOKEN')
confirmation_token = 'f20f512c'


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
            print(player)
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

    # Меню

    if command == '!команды' or command == 'команды' or command == 'помощь' or command == '!помощь':
        answer = commands()
    elif command == 'бонус':
        answer = player.bonus(action_time)
    elif command == 'профиль':
        answer = player.profile(action_time)
    elif command == 'топ':
        answer = player.top()
    elif command == 'топ лвл':
        answer = player.top_lvl()
    elif command == 'склад':
        answer = player.build.stock.stock(player.build, action_time)
    elif command == 'строить подземелье':
        answer = player.cave_build()
    elif command == 'строить земли':
        answer = player.land_build()

    # Таверна

    elif re.match(r'кости', command):
        print('кости')
        if re.search(r'дерево', command):
            print('дерево')
            answer = player.build.tavern_bones(action_time, 'wood', amount(command))
        elif re.search(r'камень', command):
            answer = player.build.tavern_bones(action_time, 'stone', amount(command))
        elif re.search(r'железо', command):
            answer = player.build.tavern_bones(action_time, 'iron', amount(command))
        elif re.search(r'кристалы', command):
            answer = player.build.tavern_bones(action_time, 'diamond', amount(command))
        elif re.search(r'золото', command):
            answer = player.build.tavern_bones(action_time, 'gold', amount(command))

    # Строительство

    elif command == 'строить склад':
        answer = player.build.build_stock(action_time)
    elif command == 'строить кузница':
        answer = player.build.build_forge(action_time)
    elif command == 'строить таверна':
        answer = player.build.build_tavern(action_time)
    elif command == 'строить цитадель':
        answer = player.build.build_citadel(action_time)
    elif command == 'строить башня':
        answer = player.build.build_tower(action_time)
    elif command == 'строить стена':
        answer = player.build.build_wall(action_time)
    elif re.match(r'строить казарм', command):
        answer = player.build.build_barracks(action_time)
    elif re.match(r'строить стрельбищ', command):
        answer = player.build.build_archery(action_time)
    elif re.match(r'строить башня маг', command):
        answer = player.build.build_magic(action_time)
    elif command == 'строить лесопилка':
        answer = player.build.build_wood_mine(action_time)
    elif command == 'строить каменоломня':
        answer = player.build.build_stone_mine(action_time)
    elif command == 'строить рудник':
        answer = player.build.build_iron_mine(action_time)
    elif command == 'строить прииск':
        answer = player.build.build_diamond_mine(action_time)

    # Добыча

    elif re.match(r'камень', command):
        answer = player.get_stone(action_time, chat_info, amount(command))
    elif re.match(r'дерево', command):
        answer = player.get_wood(action_time, chat_info, amount(command))
    elif re.match(r'железо', command):
        answer = player.get_iron(action_time, chat_info, amount(command))
    elif re.match(r'кристалы', command):
        answer = player.get_diamond(action_time, chat_info, amount(command))

    elif command == 'ковать каменная кирка':
        answer = player.craft_stone_pickaxe(action_time)
    elif command == 'ковать железная кирка':
        answer = player.craft_iron_pickaxe(action_time)
    elif command == 'ковать кристальная кирка':
        answer = player.craft_diamond_pickaxe(action_time)

    # Локацииц

    elif command == 'подземелье':
        answer = player.cave()
    elif command == 'шахта':
        answer = player.mine()
    elif command == 'кузница':
        answer = player.forge()
    elif command == 'кирки':
        answer = player.forge_pickaxe()
    elif command == 'таверна':
        answer = player.tavern()
    elif command == 'земли':
        answer = player.land()
    elif command == 'война':
        answer = player.war_menu()
    elif command == 'нанять':
        answer = player.buy()

    # Армия

    elif re.match(r'воин', command):
        answer = player.war.craft_warrior(player.build, action_time, amount(command))
    elif re.match(r'лучник', command):
        answer = player.war.craft_archer(player.build, action_time, amount(command))
    elif re.match(r'маг', command):
        answer = player.war.craft_wizard(player.build, action_time, amount(command))

    # Война

    elif command == 'здания':
        answer = player.build.war_info()
    elif command == 'щит':
        answer = player.war.shield_info(action_time)
    elif command == 'поиск':
        answer = player.war.find_enemy(player.lvl, action_time)
    elif command == 'атака':
        answer = player.war.attack(player, action_time, chat_info)
    elif command == 'армия':
        answer = player.war.army()

    elif command == 'тест':
        test_models(player)

    send(chat_info, answer, get_keyboard(player, action_time))


def test_models(player):
    chests = player.inventory.inventorychest_set.get()
    print(chests.count)
