from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from decouple import config
import json


from .models import Player, Stock, Build, Forge, Army, War

from .function.build import *
from .function.place import *
from .function.action import *
from .function.menu import *
from .function.war import *

# Create your views here.

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
                player = check_models(player=player)
                if player.place == 'new':
                    player.place = 'reg'
                    player.save()
                    message = 'Добро пожаловать в Cave World!/n Введите свой ник:'
                    send(player=player, message=message)
                    return HttpResponse('ok', content_type="text/plain", status=200)
                else:
                    if player.place == 'reg':
                        nick = data['object']['text']
                        player.nickname = nick
                        player.place = 'cave'
                        player.save()
                        message = 'Ваш ник - ' + player.nickname
                        send(player=player, message=message)
                    elif 'payload' in data['object']:
                        payload = json.loads(data['object']['payload'])
                        action_time = data['object']['date']
                        info = str(action_time) + ' | ' + \
                               str(player.user_id) + ' | ' + \
                               payload['command'] + ' | ' + \
                               player.nickname + ' | ' + \
                               player.last_name + ' ' + player.first_name
                        print(info)
                        action(command=payload['command'], player=player, action_time=action_time)
                    else:
                        text = data['object']['text']
                        text = text.split()
                        if len(text):
                            s = text[0]
                            if s.lower() == 'ник':
                                player.nickname = text[1]
                                player.save()
                                message = 'Ваш ник - ' + player.nickname
                                send(player=player, message=message)
                            else:
                                message = 'Используйте кнопки для управления!'
                                send(player=player, message=message)
                    return HttpResponse('ok', content_type="text/plain", status=200)
            return HttpResponse('Ошибка - неверный type')
        else:
            return HttpResponse('Ошибка - неверный secret key')
    else:
        return HttpResponse('Сайт находится в разработке!')


def register(user_id):
    if not Player.objects.filter(user_id=user_id).exists():
        army = Army.objects.create(user_id=user_id)
        war = War.objects.create(user_id=user_id)
        forge = Forge.objects.create(user_id=user_id)
        stock = Stock.objects.create(user_id=user_id)
        build = Build.objects.create(user_id=user_id)
        player = Player.objects.create(user_id=user_id,
                                       stock=stock,
                                       build=build,
                                       forge=forge,
                                       army=army,
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


def check_models(player):
    if not player.forge:
        forge = Forge.objects.create(user_id=player.user_id)
        player.forge = forge
        player.forge.save()
    if not player.stock:
        stock = Stock.objects.create(user_id=player.user_id)
        player.stock = stock
        player.stock.save()
    if not player.build:
        build = Build.objects.create(user_id=player.user_id)
        player.build = build
        player.build.save()
    if not player.army:
        army = Army.objects.create(user_id=player.user_id)
        player.army = army
        player.army.save()
    if not player.war:
        war = War.objects.create(user_id=player.user_id)
        player.war = war
        player.war.save()
    return player


def action(command, player, action_time):

    # Инфо

    if command.lower() == 'profile':
        profile(player=player, action_time=action_time)
    elif command.lower() == 'bonus':
        bonus(player=player, action_time=action_time)
    elif command.lower() == 'stock':
        stock(player=player)
    elif command.lower() == 'army':
        army(player=player)

    # Подземелье

    elif command.lower() == 'cave':
        cave(player=player)
    elif command.lower() == 'cave_build':
        cave_build(player=player)
    elif command.lower() == 'build_forge':
        build_forge(player=player)
    elif command.lower() == 'build_tavern':
        build_tavern(player=player)
    elif command.lower() == 'build_stock':
        build_stock(player=player)
    elif command.lower() == 'build_citadel':
        build_citadel(player=player)

    # Кузница

    elif command.lower() == 'forge':
        forge(player=player)
    elif command.lower() == 'forge_pickaxe':
        forge_pickaxe(player=player)
    elif command.lower() == 'forge_pickaxe_info':
        forge_pickaxe_info(player=player)
    elif command.lower() == 'craft_pickaxe_stone':
        craft_pickaxe_stone(player=player, action_time=action_time)
    elif command.lower() == 'craft_pickaxe_iron':
        craft_pickaxe_iron(player=player, action_time=action_time)
    elif command.lower() == 'craft_pickaxe_diamond':
        craft_pickaxe_diamond(player=player, action_time=action_time)
    elif command.lower() == 'craft_pickaxe_skull':
        craft_pickaxe_skull(player=player, action_time=action_time)
    elif command.lower() == 'forge_kit':
        forge_kit(player=player)
    elif command.lower() == 'forge_kit_info':
        forge_kit_info(player=player)
    elif command.lower() == 'craft_sword':
        craft_sword(player=player)
    elif command.lower() == 'craft_bow':
        craft_bow(player=player)
    elif command.lower() == 'craft_orb':
        craft_orb(player=player)
    elif command.lower() == 'craft_bow_x10':
        craft_bow(player=player, amount=10)
    elif command.lower() == 'craft_sword_x10':
        craft_sword(player=player, amount=10)
    elif command.lower() == 'craft_orb_x10':
        craft_orb(player=player, amount=10)

    # Шахта

    elif command.lower() == 'mine':
        mine(player=player)
    elif command.lower() == 'dig_stone':
        dig_stone(player=player, action_time=action_time)
    elif command.lower() == 'dig_iron':
        dig_iron(player=player, action_time=action_time)
    elif command.lower() == 'dig_gold':
        dig_gold(player=player, action_time=action_time)
    elif command.lower() == 'dig_diamond':
        dig_diamond(player=player, action_time=action_time)

    # Таверна

    elif command.lower() == 'tavern':
        tavern(player=player)
    elif command.lower() == 'buy_warrior':
        buy_warrior(player=player)
    elif command.lower() == 'buy_archer':
        buy_archer(player=player)
    elif command.lower() == 'buy_wizard':
        buy_wizard(player=player)
    elif command.lower() == 'buy_warrior_x10':
        buy_warrior(player=player, amount=10)
    elif command.lower() == 'buy_archer_x10':
        buy_archer(player=player, amount=10)
    elif command.lower() == 'buy_wizard_x10':
        buy_wizard(player=player, amount=10)

    # Земли

    elif command.lower() == 'land':
        land(player=player)
    elif command.lower() == 'cut_wood':
        cut_wood(player=player, action_time=action_time)
    elif command.lower() == 'land_build':
        land_build(player=player)
    elif command.lower() == 'build_tower':
        build_tower(player=player)
    elif command.lower() == 'build_wall':
        build_wall(player=player)

    # Война
    elif command.lower() == 'war':
        war(player=player)
    elif command.lower() == 'find_enemy':
        find_enemy(player=player, action_time=action_time)
    elif command.lower() == 'attack':
        attack(player=player, action_time=action_time)
    elif command.lower() == 'shield_info':
        shield_info(player=player, action_time=action_time)
