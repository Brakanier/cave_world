from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import json
from decouple import config
from datetime import datetime

from .models.build import Build, Stock
from .models.player import Player
from .models.war import War
from .actions.functions import *

secret_token = config('SECRET_TOKEN')
confirmation_token = config('CONFIRMATION_TOKEN')


@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        if data['secret'] == secret_token:
            if data['type'] == 'confirmation':
                return HttpResponse(confirmation_token, content_type="text/plain", status=200)
            if data['type'] == 'message_new':
                user_id = data['object']['from_id']
                peer_id = data['object']['peer_id']
                player = register(user_id=user_id)
                if player.place == 'new':
                    player.place = 'reg'
                    player.save()
                    message = 'Добро пожаловать в Cave World!\n' \
                              'Введите свой ник:'
                    send(player=player, message=message)
                    return HttpResponse('ok', content_type="text/plain", status=200)
                else:
                    action_time = data['object']['date']
                    if player.place == 'reg':
                        nick = data['object']['text']
                        player.nickname = nick
                        player.place = 'cave'
                        Player.objects.filter(user_id=player.user_id).update(place=player.place)
                        message = 'Ваш ник - ' + player.nickname
                        send(player=player, message=message)
                    elif 'payload' in data['object']:
                        payload = json.loads(data['object']['payload'])
                        log(player, payload['command'], action_time)
                        action(command=payload['command'], player=player, action_time=action_time)
                    else:
                        text = data['object']['text']
                        if text:
                            log(player, text, action_time)
                            action(text.lower(), player, action_time)

                    return HttpResponse('ok', content_type="text/plain", status=200)
            return HttpResponse('Ошибка - неверный type')
        else:
            return HttpResponse('Ошибка - неверный secret key')
    else:
        return HttpResponse('Сайт находится в разработке!')


def register(user_id):
    if not Player.objects.filter(user_id=user_id).exists():
        war = War.objects.create(user_id=user_id)
        stock = Stock.objects.create(user_id=user_id)
        build = Build.objects.create(user_id=user_id, stock=stock)
        player = Player.objects.create(user_id=user_id,
                                       build=build,
                                       war=war,
                                       )
        vk = vk_connect()
        user = vk.users.get(user_ids=str(user_id))
        user = user[0]
        if user['first_name']:
            player.first_name = user['first_name']
        if user['last_name']:
            player.last_name = user['last_name']
        player.place = "new"
    else:
        player = Player.objects.get(user_id=user_id)
    return player


def log(player, command, action_time):
    time = datetime.fromtimestamp(int(action_time + (3600 * 3)))
    info = time.strftime('%Y-%m-%d %H:%M:%S') + ' | ' + \
           str(player.user_id) + ' | ' + \
           command + ' | ' + \
           player.nickname + ' | ' + \
           player.last_name + ' ' + player.first_name
    print(info)


def action(command, player, action_time, amount=1):
    answer = 'пусто'

    # Меню

    if command == '!команды':
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
        answer = player.build.stock.stock(action_time)
    elif command == 'строить подземелье':
        answer = player.cave_build()
    elif command == 'строить земли':
        answer = player.land_build()

    # Строительство

    elif command == 'строить склад':
        answer = player.build.build_stock()
    elif command == 'строить кузница':
        answer = player.build.build_forge()
    elif command == 'строить таверна':
        answer = player.build.build_tavern()
    elif command == 'строить цитадель':
        answer = player.build.build_citadel()
    elif command == 'строить башня':
        answer = player.build.build_tower()
    elif command == 'строить стена':
        answer = player.build.build_wall()

    # Добыча

    elif 'камень' in command:
        part = command.split()
        if len(part) > 1:
            amount = int(part[1])
        answer = player.get_stone(action_time, amount)
    elif 'дерево' in command:
        part = command.split()
        if len(part) > 1:
            amount = int(part[1])
        answer = player.get_wood(action_time, amount)
    elif 'железо' in command:
        part = command.split()
        if len(part) > 1:
            amount = int(part[1])
        answer = player.get_iron(action_time, amount)
    elif 'кристалы' in command:
        part = command.split()
        if len(part) > 1:
            amount = int(part[1])
        answer = player.get_diamond(action_time, amount)

    elif command == 'ковать каменная кирка':
        answer = player.craft_stone_pickaxe()
    elif command == 'ковать железная кирка':
        answer = player.craft_iron_pickaxe()
    elif command == 'ковать кристальная кирка':
        answer = player.craft_diamond_pickaxe()

    # Локации

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

    elif 'воин' in command:
        part = command.split()
        if len(part) > 1:
            amount = int(part[1])
        answer = player.war.craft_warrior(player.build.stock, player.build.barracks, amount)
    elif 'лучник' in command:
        part = command.split()
        if len(part) > 1:
            amount = int(part[1])
        answer = player.war.craft_archer(player.build.stock, player.build.archery, amount)
    elif 'маг' in command:
        part = command.split()
        if len(part) > 1:
            amount = int(part[1])
        answer = player.war.craft_wizard(player.build.stock, player.build.magic, amount)

    # Война

    elif command == 'здания':
        answer = player.build.war_info()
    elif command == 'щит':
        answer = player.war.shield_info(action_time)
    elif command == 'поиск':
        answer = player.war.find_enemy(player.lvl, action_time)
    elif command == 'атака':
        answer = player.war.attack(player, action_time)
    elif command == 'армия':
        answer = player.war.army()

    print(answer)
    send(player, answer, action_time)
